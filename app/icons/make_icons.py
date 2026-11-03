# Иконки ИТП из одного логотипа (app/icons/logo.png, мордочка кролика на светлом фоне):
#   Android — значок приложения (обычный, круглый, адаптивный), значок уведомлений, заставка при запуске;
#   Windows — icon.ico и icon.png.
# Запуск из папки app: python icons/make_icons.py  (нужен Pillow)
import os
from PIL import Image, ImageDraw

H = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(H, '..', 'android', 'app', 'src', 'main', 'res')
logo = Image.open(os.path.join(H, 'logo.png')).convert('RGBA')
BG = logo.getpixel((2, 2))[:3]           # светлый фон логотипа — им же заливается всё вокруг
APP_BG = (251, 247, 245)                 # фон приложения (#FBF7F5) — фон заставки
DPI = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}


def big(n):
    return logo.resize((n, n), Image.LANCZOS)


def masked(n, kind):
    """логотип в форме: 'r' — скруглённый квадрат, 'c' — круг"""
    k = 4
    m = Image.new('L', (n * k, n * k), 0)
    d = ImageDraw.Draw(m)
    if kind == 'c':
        d.ellipse((0, 0, n * k - 1, n * k - 1), fill=255)
    else:
        d.rounded_rectangle((0, 0, n * k - 1, n * k - 1), radius=int(n * k * .22), fill=255)
    m = m.resize((n, n), Image.LANCZOS)
    out = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    out.paste(big(n), (0, 0), m)
    return out


def save(im, *p):
    f = os.path.join(*p)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    im.save(f)


# --- Android: значок приложения
for q, s in DPI.items():
    save(masked(round(48 * s), 'r'), RES, 'mipmap-' + q, 'ic_launcher.png')
    save(masked(round(48 * s), 'c'), RES, 'mipmap-' + q, 'ic_launcher_round.png')
    # адаптивный (Android 8+): холст 108dp, видна середина ~72dp — мордочка занимает 80dp, чтобы глаза не обрезались
    n = round(108 * s)
    fg = Image.new('RGBA', (n, n), BG + (255,))
    f = round(80 * s)
    fg.paste(big(f), ((n - f) // 2, (n - f) // 2))
    save(fg, RES, 'mipmap-' + q, 'ic_launcher_foreground.png')
with open(os.path.join(RES, 'values', 'ic_launcher_background.xml'), 'w', encoding='utf-8') as fh:
    fh.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#%02X%02X%02X</color>\n</resources>\n' % BG)

# --- Android: значок уведомлений — белый силуэт кролика (Android сам красит его), 24dp
sil = Image.open(os.path.join(H, 'notify_silhouette.png')).convert('RGBA')
a = sil.getchannel('A')
sil = Image.new('RGBA', sil.size, (255, 255, 255, 255))
sil.putalpha(a)
sil = sil.crop(a.getbbox())
for q, s in DPI.items():
    n = round(24 * s)
    c = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    k = min((n - 2) / sil.width, (n - 2) / sil.height)
    t = sil.resize((max(1, round(sil.width * k)), max(1, round(sil.height * k))), Image.LANCZOS)
    c.paste(t, ((n - t.width) // 2, (n - t.height) // 2), t)
    save(c, RES, 'drawable-' + q, 'ic_stat_itp.png')

# --- Android: заставка — фон приложения и мордочка в скруглённом квадрате посередине (размеры как у шаблона)
for root, _, files in os.walk(RES):
    if 'splash.png' in files and os.path.basename(root).startswith('drawable'):
        f = os.path.join(root, 'splash.png')
        w, h = Image.open(f).size
        c = Image.new('RGB', (w, h), APP_BG)
        n = round(min(w, h) * .32)
        ic = masked(n, 'r')
        c.paste(ic, ((w - n) // 2, (h - n) // 2), ic)
        c.save(f)

# --- Windows
save(masked(512, 'r'), H, 'icon.png')
masked(256, 'r').save(os.path.join(H, 'icon.ico'), sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print('иконки готовы')
