# Выложить ИТП на Яндекс одной командой (из корня репозитория):
#   python app/web/upload_yandex.py          — сайт: app/dist/web → бакет Object Storage (itpcode.website.yandexcloud.net)
#   python app/web/upload_yandex.py --disk "ИТП 7.2.0"  — ещё и файлы выпуска в папку на Яндекс Диске
# Ключи — в файле ../itp-tools/yandex.txt (вне репозитория, никому не показывать), строки вида ИМЯ=значение:
#   S3_KEY_ID, S3_SECRET — статический ключ сервисного аккаунта с ролью storage.editor (Object Storage)
#   BUCKET               — имя бакета (itpcode)
#   DISK_LOGIN, DISK_PASSWORD — логин Яндекса и пароль приложения «Файлы (WebDAV)» (не основной пароль!)
#   DISK_DIR             — папка на Диске, куда класть выпуски (ИТП Установка — по ней публичная ссылка)
# Нужны boto3 и requests.
import os, sys, mimetypes
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
KEYS = os.environ.get('ITP_YANDEX_KEYS', os.path.join(ROOT, '..', 'itp-tools', 'yandex.txt'))
K = dict(l.split('=', 1) for l in open(KEYS, encoding='utf-8').read().split('\n') if '=' in l and not l.startswith('#'))
K = {k.strip(): v.strip() for k, v in K.items()}
TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
         '.webmanifest': 'application/manifest+json', '.png': 'image/png'}


def site():
    import boto3
    s3 = boto3.client('s3', endpoint_url='https://storage.yandexcloud.net', region_name='ru-central1',
                      aws_access_key_id=K['S3_KEY_ID'], aws_secret_access_key=K['S3_SECRET'])
    web = os.path.join(ROOT, 'app', 'dist', 'web')
    # index.html — последним: пока он старый, старый sw.js не встретит новую страницу наполовину
    names = sorted((n for n in os.listdir(web) if n != '_headers'), key=lambda n: n == 'index.html')
    for n in names:
        ext = os.path.splitext(n)[1]
        extra = {'ContentType': TYPES.get(ext) or mimetypes.guess_type(n)[0] or 'application/octet-stream'}
        if n in ('index.html', 'sw.js', 'manifest.webmanifest'):
            extra['CacheControl'] = 'no-cache'
        s3.upload_file(os.path.join(web, n), K.get('BUCKET', 'itpcode'), n, ExtraArgs=extra)
        print('сайт:', n)


def disk(folder):
    import requests
    from urllib.parse import quote
    auth = (K['DISK_LOGIN'], K['DISK_PASSWORD'])
    base = 'https://webdav.yandex.ru/' + quote(K.get('DISK_DIR', 'ИТП').strip('/'))
    src = os.path.join(ROOT, folder)
    dst = base                                  # файлы кладутся прямо в папку, рядом с прошлыми версиями
    r = requests.request('MKCOL', dst, auth=auth)
    if r.status_code not in (201, 405):         # 405 — папка уже есть
        sys.exit('Диск: не создать папку %s: %s' % (dst, r.status_code))
    for n in sorted(os.listdir(src)):           # только файлы верхнего уровня: HTML, APK, EXE, ПРОЧИТАЙ
        p = os.path.join(src, n)
        if os.path.isfile(p):
            with open(p, 'rb') as f:
                r = requests.put(dst + '/' + quote(n), data=f, auth=auth)
            print('диск:', n, r.status_code)
            if r.status_code not in (200, 201, 204):
                sys.exit('Диск: ошибка загрузки')


site()
if '--disk' in sys.argv:
    disk(sys.argv[sys.argv.index('--disk') + 1])
