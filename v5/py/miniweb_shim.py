"""Учебный веб-фреймворк ИТП: miniweb.

Настоящий сервер (Flask, FastAPI) слушает порт и ждёт запросов из сети. В браузере сети нет, поэтому miniweb
устроен как их ядро без сети: маршруты регистрируются декораторами, запрос обрабатывает app.handle,
а проверить сервер можно тест-клиентом (app.test_client(), как во Flask) или учебным requests (app.serve("адрес")).

    from miniweb import App
    app = App()

    @app.get("/hello/<name>")
    def hello(req, name):
        return {"text": "Привет, " + name}

    client = app.test_client()
    print(client.get("/hello/Аня").json())

Обработчик получает объект запроса и параметры пути. Возвращает:
словарь или список → JSON с кодом 200; строку → текст; (тело, код) → свой код ответа.
Мидлвары: @app.before — функция(req), вызывается до обработчика (вернула ответ — обработчик не вызывается);
@app.after — функция(req, resp), может поменять ответ.
"""
import json as _json
from urllib.parse import urlsplit as _urlsplit, parse_qsl as _parse_qsl, urlencode as _urlencode

__all__ = ['App', 'Request', 'Response']

_REASONS = {200: 'OK', 201: 'Created', 204: 'No Content', 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden',
            404: 'Not Found', 405: 'Method Not Allowed', 409: 'Conflict', 422: 'Unprocessable Entity', 429: 'Too Many Requests',
            500: 'Internal Server Error'}


class Request:
    """Запрос к серверу: method, path, args (параметры после ?), json (тело), headers, state (словарь для мидлвар)."""

    def __init__(self, method, path, args=None, json=None, headers=None):
        self.method = method.upper()
        self.path = path
        self.args = dict(args or {})
        self.json = json
        self.headers = {str(k).lower(): str(v) for k, v in (headers or {}).items()}
        self.state = {}

    def header(self, name, default=None):
        return self.headers.get(name.lower(), default)

    def __repr__(self):
        return '<Request %s %s>' % (self.method, self.path)


class Response:
    """Ответ сервера: status_code, headers, тело. json() — тело как JSON, text — как строка."""

    def __init__(self, body=None, status_code=200, headers=None):
        self.status_code = status_code
        self.headers = dict(headers or {})
        if isinstance(body, (dict, list)):
            self.text = _json.dumps(body, ensure_ascii=False)
            self.headers.setdefault('Content-Type', 'application/json')
        else:
            self.text = '' if body is None else str(body)
            self.headers.setdefault('Content-Type', 'text/plain; charset=utf-8')
        self.reason = _REASONS.get(status_code, '')

    @property
    def ok(self):
        return self.status_code < 400

    def json(self):
        return _json.loads(self.text)

    def __repr__(self):
        return '<Response [%d]>' % self.status_code


def _make(rv):
    if isinstance(rv, Response):
        return rv
    if isinstance(rv, tuple):
        body, code = rv[0], rv[1]
        return Response(body, code, rv[2] if len(rv) > 2 else None)
    return Response(rv)


def _parse(rule):
    """«/notes/<int:id>» → список частей: строка или (имя, тип)"""
    parts = []
    for p in rule.strip('/').split('/'):
        if p.startswith('<') and p.endswith('>'):
            kind, _, name = p[1:-1].rpartition(':')
            parts.append((name, kind or 'str'))
        else:
            parts.append(p)
    return parts


def _match(parts, path):
    got = path.strip('/').split('/')
    if len(got) != len(parts):
        return None
    params = {}
    for want, x in zip(parts, got):
        if isinstance(want, tuple):
            name, kind = want
            if kind == 'int':
                if not x.lstrip('-').isdigit():
                    return None
                x = int(x)
            elif x == '':
                return None
            params[name] = x
        elif want != x:
            return None
    return params


class App:
    def __init__(self, name='app'):
        self.name = name
        self.routes = []          # (метод, правило, части, функция)
        self._before = []
        self._after = []

    # ---------- маршруты ----------
    def route(self, rule, methods=('GET',)):
        def deco(f):
            for m in methods:
                self.routes.append((m.upper(), rule, _parse(rule), f))
            return f
        return deco

    def get(self, rule):
        return self.route(rule, ['GET'])

    def post(self, rule):
        return self.route(rule, ['POST'])

    def put(self, rule):
        return self.route(rule, ['PUT'])

    def delete(self, rule):
        return self.route(rule, ['DELETE'])

    # ---------- мидлвары ----------
    def before(self, f):
        self._before.append(f)
        return f

    def after(self, f):
        self._after.append(f)
        return f

    # ---------- обработка ----------
    def handle(self, req):
        resp = None
        for f in self._before:
            rv = f(req)
            if rv is not None:
                resp = _make(rv)
                break
        if resp is None:
            resp = self._dispatch(req)
        for f in self._after:
            rv = f(req, resp)
            if rv is not None:
                resp = _make(rv)
        return resp

    def _dispatch(self, req):
        allowed = False
        for method, rule, parts, f in self.routes:
            params = _match(parts, req.path)
            if params is None:
                continue
            if method != req.method:
                allowed = True
                continue
            try:
                return _make(f(req, **params))
            except Exception as e:
                return Response({'error': '%s: %s' % (type(e).__name__, e)}, 500)
        if allowed:
            return Response({'error': 'method not allowed'}, 405)
        return Response({'error': 'not found'}, 404)

    def test_client(self):
        return TestClient(self)

    def serve(self, address):
        """Подключить приложение к учебному requests: запросы на http://address/… обработает это приложение."""
        import requests
        requests._servers()[address.lower()] = _Adapter(self)
        print(' * miniweb: приложение %s слушает http://%s' % (self.name, address))


class TestClient:
    """Тест-клиент: запросы прямо в приложение, без сети."""

    def __init__(self, app):
        self.app = app

    def request(self, method, path, params=None, json=None, headers=None):
        parts = _urlsplit(path)
        args = dict(_parse_qsl(parts.query, keep_blank_values=True))
        args.update({str(k): str(v) for k, v in (params or {}).items()})
        body = _json.loads(_json.dumps(json)) if json is not None else None
        return self.app.handle(Request(method, parts.path or '/', args, body, headers))

    def get(self, path, **kw):
        return self.request('GET', path, **kw)

    def post(self, path, **kw):
        return self.request('POST', path, **kw)

    def put(self, path, **kw):
        return self.request('PUT', path, **kw)

    def delete(self, path, **kw):
        return self.request('DELETE', path, **kw)


class _Adapter:
    """Сервер для учебного requests (тот же интерфейс, что у его виртуальных серверов)."""

    def __init__(self, app):
        self.app = app

    def handle(self, method, path, query, body, headers):
        r = self.app.handle(Request(method, path, dict(query), body, headers))
        return r.status_code, r.text.encode('utf-8'), r.headers.get('Content-Type', 'text/plain; charset=utf-8')
