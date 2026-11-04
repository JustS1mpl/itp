# Папка сайта ИТП — для iPhone/iPad (и любого браузера): app/dist/web. Её целиком загружают на хостинг (Netlify,
# Cloudflare Pages и т. п., см. «ИТП <версия>/сайт для iPhone/КАК ВЫЛОЖИТЬ.md»). В Safari: «Поделиться» → «На экран
# „Домой“» — ИТП открывается на весь экран со своим значком и работает без интернета (sw.js хранит страницу).
#   index.html            — out5.html как есть
#   manifest.webmanifest  — название, значки, цвета, display: standalone (a_web.js подключает его только на сайте)
#   apple-touch-icon.png  — значок на экране «Домой» iPhone (180×180, без прозрачности: углы iOS скругляет сама)
#   icon-192/512.png, icon-maskable-512.png — значки для Android/Chrome
#   sw.js                 — хранит страницу и значки; новая версия сайта приходит при следующем запуске
#   _headers              — sw.js и index.html не кэшировать надолго (Netlify и Cloudflare Pages читают этот файл)
# Запуск из корня репозитория: python app/web/make_web.py   (нужен Pillow; перед этим — сборка out5.html)
import json, os, re, shutil
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'app', 'dist', 'web')
VER = re.search(r"^VER = '([^']+)'", open(os.path.join(ROOT, 'build5.py'), encoding='utf-8').read(), re.M).group(1)
logo = Image.open(os.path.join(ROOT, 'app', 'icons', 'logo.png')).convert('RGB')
BG = logo.getpixel((2, 2))

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copyfile(os.path.join(ROOT, 'out5.html'), os.path.join(OUT, 'index.html'))


def icon(n, pad=0.0):
    c = Image.new('RGB', (n, n), BG)
    k = round(n * (1 - 2 * pad))
    c.paste(logo.resize((k, k), Image.LANCZOS), ((n - k) // 2, (n - k) // 2))
    return c


icon(180).save(os.path.join(OUT, 'apple-touch-icon.png'))
icon(192).save(os.path.join(OUT, 'icon-192.png'))
icon(512).save(os.path.join(OUT, 'icon-512.png'))
icon(512, .1).save(os.path.join(OUT, 'icon-maskable-512.png'))   # у «маскируемого» значка мордочка в безопасной зоне
icon(48).save(os.path.join(OUT, 'favicon.png'))

json.dump({
    'name': 'ИТП — И так, программирование',
    'short_name': 'ИТП',
    'description': 'Бесплатный курс Python с нуля. Работает без интернета.',
    'lang': 'ru',
    'start_url': './',
    'scope': './',
    'display': 'standalone',
    'orientation': 'portrait',
    'background_color': '#FBF4F6',
    'theme_color': '#F7F4EE',
    'icons': [
        {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}, open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

SW = '''/* ИТП %(v)s: страница и значки хранятся на устройстве — с экрана «Домой» ИТП открывается и без интернета.
   Новая версия сайта (другой sw.js) скачивается в фоне и включается при следующем запуске. Библиотеки Python с CDN
   (numpy и др.) сюда не входят: их кэширует сам браузер. */
var C = 'itp-%(v)s', FILES = ['./', 'index.html', 'manifest.webmanifest', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'favicon.png'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(C).then(function (c) { return c.addAll(FILES) }).then(function () { return self.skipWaiting() }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k.indexOf('itp-') === 0 && k !== C }).map(function (k) { return caches.delete(k) }));
  }).then(function () { return self.clients.claim() }));
});
self.addEventListener('fetch', function (e) {
  var r = e.request;
  if (r.method !== 'GET' || new URL(r.url).origin !== location.origin) return;
  e.respondWith(caches.match(r, { ignoreSearch: true }).then(function (hit) {
    return hit || (r.mode === 'navigate' ? caches.match('index.html') : null) || fetch(r);
  }).then(function (x) { return x || fetch(r) }));
});
''' % {'v': VER}
open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write(SW)

open(os.path.join(OUT, '_headers'), 'w', encoding='utf-8').write(
    '/sw.js\n  Cache-Control: no-cache\n/index.html\n  Cache-Control: no-cache\n/\n  Cache-Control: no-cache\n'
    '/manifest.webmanifest\n  Content-Type: application/manifest+json\n')
print('сайт готов:', OUT, VER)
