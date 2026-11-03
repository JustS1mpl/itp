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

# --- Windows: картинки установщика в духе Windows 98 (как окно соглашения в ИТП): синяя полоса заголовка 98-го,
#     серый #C0C0C0, объёмная рамка «кнопки» вокруг мордочки. Боковая — на первой и последней страницах, шапка — на остальных
from PIL import ImageFont
FD = 'C:/Windows/Fonts/'
def fnt(n, s):
    for f in (n, 'tahomabd.ttf', 'arialbd.ttf'):
        try:
            return ImageFont.truetype(FD + f, s)
        except OSError:
            pass
    return ImageFont.load_default()
def bevel(d, x0, y0, x1, y1):
    # рамка 98-го: светлый край сверху-слева, тёмный снизу-справа, в два ряда
    d.line([(x0, y1), (x0, y0), (x1, y0)], fill=(255, 255, 255)); d.line([(x0 + 1, y1 - 1), (x0 + 1, y0 + 1), (x1 - 1, y0 + 1)], fill=(223, 223, 223))
    d.line([(x0, y1), (x1, y1), (x1, y0)], fill=(0, 0, 0)); d.line([(x0 + 1, y1 - 1), (x1 - 1, y1 - 1), (x1 - 1, y0 + 1)], fill=(128, 128, 128))
W, Hh = 164, 314
sb = Image.new('RGB', (W, Hh))
for y in range(Hh):                       # градиент заголовка 98-го: тёмно-синий → голубой
    t = y / (Hh - 1); c = tuple(round(a + (b - a) * t) for a, b in zip((0, 0, 128), (16, 132, 208)))
    ImageDraw.Draw(sb).line([(0, y), (W, y)], fill=c)
d = ImageDraw.Draw(sb)
n = 100; x0 = (W - n) // 2 - 3; y0 = 34
d.rectangle((x0, y0, x0 + n + 6, y0 + n + 6), fill=(192, 192, 192)); bevel(d, x0, y0, x0 + n + 6, y0 + n + 6)
sb.paste(big(n).convert('RGB'), (x0 + 3, y0 + 3))
d.text((W // 2, y0 + n + 30), 'ИТП', font=fnt('tahomabd.ttf', 34), fill=(255, 255, 255), anchor='mm')
d.text((W // 2, y0 + n + 58), 'И так,', font=fnt('tahoma.ttf', 13), fill=(220, 232, 255), anchor='mm')
d.text((W // 2, y0 + n + 74), 'программирование', font=fnt('tahoma.ttf', 13), fill=(220, 232, 255), anchor='mm')
d.text((W // 2, Hh - 22), 'Python с нуля', font=fnt('tahoma.ttf', 11), fill=(170, 200, 240), anchor='mm')
sb.save(os.path.join(H, 'installerSidebar.bmp'))
hd = Image.new('RGB', (150, 57), (192, 192, 192)); d = ImageDraw.Draw(hd)
n = 45; x0 = 150 - n - 12; y0 = (57 - n - 6) // 2
bevel(d, x0, y0, x0 + n + 6, y0 + n + 6); hd.paste(big(n).convert('RGB'), (x0 + 3, y0 + 3))
hd.save(os.path.join(H, 'installerHeader.bmp'))
print('картинки установщика готовы')
