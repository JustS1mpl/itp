"""Учебный модуль requests для ИТП.

В браузере у программы нет выхода в интернет и нет локальных серверов, поэтому настоящий requests тут не работает.
Этот модуль повторяет его основной интерфейс (get, post, put, patch, delete, head, Session, Response, исключения),
а запросы обслуживают ВИРТУАЛЬНЫЕ серверы, которые живут прямо в программе:

* учебный сервер ИТП по адресу 127.0.0.1:5000 есть всегда (см. DEMO ниже);
* задачи могут добавлять свои серверы через файл _itp_servers.json (его кладёт проверяющая система);
* любой другой адрес даёт ConnectionError, как будто сети нет.
"""
import json as _json
import os as _os
import sys as _sys
import types as _types
from urllib.parse import urlsplit as _urlsplit, urlencode as _urlencode, parse_qsl as _parse_qsl, unquote as _unquote

__version__ = '2.32.3-itp'
__path__ = []

# ---------------------------------------------------------------- исключения
exceptions = _types.ModuleType('requests.exceptions')
_sys.modules['requests.exceptions'] = exceptions


class RequestException(IOError):
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        self.request = kwargs.pop('request', None)
        super().__init__(*args)


class ConnectionError(RequestException):
    pass


class Timeout(RequestException):
    pass


class HTTPError(RequestException):
    pass


class InvalidURL(RequestException, ValueError):
    pass


class MissingSchema(RequestException, ValueError):
    pass


class JSONDecodeError(RequestException, ValueError):
    pass


for _c in (RequestException, ConnectionError, Timeout, HTTPError, InvalidURL, MissingSchema, JSONDecodeError):
    setattr(exceptions, _c.__name__, _c)
    _c.__module__ = 'requests.exceptions'

# ---------------------------------------------------------------- коды ответов
_REASONS = {200: 'OK', 201: 'Created', 202: 'Accepted', 204: 'No Content', 301: 'Moved Permanently', 302: 'Found',
            400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found', 405: 'Method Not Allowed',
            409: 'Conflict', 422: 'Unprocessable Entity', 500: 'Internal Server Error', 503: 'Service Unavailable'}
codes = _types.SimpleNamespace(ok=200, created=201, accepted=202, no_content=204, bad_request=400, unauthorized=401,
                               forbidden=403, not_found=404, method_not_allowed=405, internal_server_error=500)


class _Headers(dict):
    """Заголовки: имена не зависят от регистра."""

    def _k(self, k):
        for x in self:
            if x.lower() == str(k).lower():
                return x
        return k

    def __getitem__(self, k):
        return dict.__getitem__(self, self._k(k))

    def __setitem__(self, k, v):
        dict.__setitem__(self, self._k(k), v)

    def __contains__(self, k):
        return dict.__contains__(self, self._k(k))

    def get(self, k, default=None):
        return dict.get(self, self._k(k), default)


class Response:
    def __init__(self, status_code, content=b'', headers=None, url=''):
        self.status_code = status_code
        self._content = content
        self.headers = _Headers(headers or {})
        self.url = url
        self.encoding = 'utf-8'
        self.reason = _REASONS.get(status_code, '')
        self.history = []
        self.request = None

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        return self._content.decode(self.encoding or 'utf-8', 'replace')

    @property
    def ok(self):
        return self.status_code < 400

    def json(self, **kw):
        try:
            return _json.loads(self._content.decode('utf-8'), **kw)
        except ValueError as e:
            raise JSONDecodeError('Expecting value: сервер вернул не JSON') from e

    def raise_for_status(self):
        if 400 <= self.status_code < 500:
            kind = 'Client Error'
        elif 500 <= self.status_code < 600:
            kind = 'Server Error'
        else:
            return
        raise HTTPError('%d %s: %s for url: %s' % (self.status_code, kind, self.reason, self.url), response=self)

    def iter_lines(self, **kw):
        for line in self.text.splitlines():
            yield line.encode('utf-8')

    def __bool__(self):
        return self.ok

    def __repr__(self):
        return '<Response [%d]>' % self.status_code


# ---------------------------------------------------------------- виртуальные серверы
def _body(spec, state, key, query=()):
    # 7.0: "status" — свой код ответа (для задач про ошибки); "param" + "variants" — ответ зависит от параметра запроса:
    # {"param": "city", "variants": {"Омск": {...}}} — значения нет среди вариантов → 404 {"error": "not found"}
    code = spec.get('status', 200)
    if 'key' in spec and dict(query).get('key') != spec['key']:  # 7.0: API с ключом в параметре key
        return 401, _json.dumps({'error': 'invalid api key'}, ensure_ascii=False).encode('utf-8'), 'application/json'
    if 'statuses' in spec:  # коды по очереди на каждый запрос, последний повторяется: [503, 503, 200]
        n = state.get(key + '#', 0)
        state[key + '#'] = n + 1
        code = spec['statuses'][min(n, len(spec['statuses']) - 1)]
    if 'param' in spec:
        v = dict(query).get(spec['param'])
        if v not in spec['variants']:
            return 404, _json.dumps({'error': 'not found'}, ensure_ascii=False).encode('utf-8'), 'application/json'
        return code, _json.dumps(spec['variants'][v], ensure_ascii=False).encode('utf-8'), 'application/json'
    if 'json' in spec:
        return code, _json.dumps(spec['json'], ensure_ascii=False).encode('utf-8'), 'application/json'
    if 'seq' in spec:
        n = state.get(key, 0)
        state[key] = n + 1
        return code, str(spec['seq'][n % len(spec['seq'])]).encode('utf-8'), 'text/plain; charset=utf-8'
    return code, str(spec.get('text', '')).encode('utf-8'), 'text/plain; charset=utf-8'


class _Server:
    """routes: {"/путь": {"text": ...} | {"json": ...} | {"seq": [...]}}; users: список JSON-объектов (ресурс /users,
    или /<collection>, если в описании сервера есть "collection": "notes")."""

    def __init__(self, spec):
        self.routes = dict(spec.get('routes', {}))
        self.users = _json.loads(_json.dumps(spec['users'])) if 'users' in spec else None
        self.coll = '/' + spec.get('collection', 'users')
        # 7.0: учебный мессенджер для ботов (как Telegram): {"bot": {"token": …, "updates": [{"update_id": 1, "message": {…}}]}}
        self.bot = _json.loads(_json.dumps(spec['bot'])) if 'bot' in spec else None
        self.sent = []
        # 7.0: учебная языковая модель: {"llm": {"key": "demo", "model": "itp-mini", "rules": [{"if": ["слово", …], "say": ответ}], "default": …}}
        self.llm = spec.get('llm')
        self.token = spec.get('token')
        self.state = {}

    def _json(self, code, obj):
        return code, _json.dumps(obj, ensure_ascii=False).encode('utf-8'), 'application/json'

    def handle(self, method, path, query, body, headers):
        p = path if path == '/' else path.rstrip('/')
        if p == '/secret' and self.token is not None:
            if headers.get('Authorization') != 'OAuth ' + self.token:
                return self._json(401, {'error': 'Unauthorized'})
            return self._json(200, {'message': 'Секретные данные для владельца токена'})
        if p == '/echo':
            return self._json(200, {'method': method, 'args': dict(query), 'json': body})
        if self.bot is not None and p in ('/getUpdates', '/sendMessage'):
            return self._bot(p, dict(query), body)
        if self.llm is not None and p == '/v1/chat':
            return self._llm(method, body, headers)
        if self.users is not None and (p == self.coll or p.startswith(self.coll + '/')):
            return self._users(method, p, body)
        spec = self.routes.get(p)
        if spec is None:
            return 404, b'Not Found', 'text/plain; charset=utf-8'
        if method not in spec.get('methods', ['GET']):
            return 405, b'Method Not Allowed', 'text/plain; charset=utf-8'
        return _body(spec, self.state, p, query)

    def _bot(self, p, query, body):
        if query.get('token') != self.bot['token']:
            return self._json(401, {'ok': False, 'error': 'Unauthorized'})
        if p == '/getUpdates':
            try:
                offset = int(query.get('offset', 0))
            except ValueError:
                offset = 0
            return self._json(200, {'ok': True, 'result': [u for u in self.bot['updates'] if u['update_id'] >= offset]})
        if not isinstance(body, dict) or 'chat_id' not in body or not str(body.get('text', '')).strip():
            return self._json(400, {'ok': False, 'error': 'Нужны chat_id и непустой text'})
        msg = {'message_id': len(self.sent) + 1, 'chat_id': body['chat_id'], 'text': str(body['text'])}
        self.sent.append(msg)
        return self._json(200, {'ok': True, 'result': msg})

    def _llm(self, method, body, headers):
        """POST /v1/chat, заголовок Authorization: Bearer КЛЮЧ, json {"messages": [{"role", "content"}], "max_tokens"?}.
        Ответ детерминированный: первое правило, все слова "if" которого есть в последнем сообщении user (без учёта регистра);
        "sys" — правило работает, только если эта строка есть в сообщении system; "ctx" — слова, которые должны быть в более ранних
        сообщениях (модель «помнит» только присланную историю). Токены считаются по словам."""
        spec = self.llm
        if method != 'POST':
            return 405, b'Method Not Allowed', 'text/plain; charset=utf-8'
        if headers.get('Authorization') != 'Bearer ' + spec.get('key', 'demo'):
            return self._json(401, {'error': {'type': 'auth', 'message': 'invalid api key'}})
        if 'statuses' in spec:
            n = self.state.get('llm#', 0)
            self.state['llm#'] = n + 1
            code = spec['statuses'][min(n, len(spec['statuses']) - 1)]
            if code != 200:
                return self._json(code, {'error': {'type': 'rate_limit' if code == 429 else 'overloaded', 'message': 'too many requests' if code == 429 else 'try later'}})
        msgs = body.get('messages') if isinstance(body, dict) else None
        if not isinstance(msgs, list) or not msgs or not all(isinstance(m, dict) and m.get('role') in ('system', 'user', 'assistant')
                                                              and isinstance(m.get('content'), str) for m in msgs) or msgs[-1]['role'] != 'user':
            return self._json(400, {'error': {'type': 'bad_request', 'message': 'messages: список {role, content}, последнее — от user'}})
        system = ' '.join(m['content'] for m in msgs if m['role'] == 'system').lower()
        last = msgs[-1]['content'].lower()
        before = ' '.join(m['content'] for m in msgs[:-1]).lower()
        answer = spec.get('default', 'Не знаю.')
        for rule in spec.get('rules', []):
            if all(w.lower() in last for w in rule.get('if', [])) and rule.get('sys', '').lower() in system \
                    and all(w.lower() in before for w in rule.get('ctx', [])):
                answer = rule['say']
                break
        if not isinstance(answer, str):
            answer = _json.dumps(answer, ensure_ascii=False)
        words = answer.split(' ')
        finish = 'stop'
        mt = body.get('max_tokens')
        if isinstance(mt, int) and 0 < mt < len(words):
            answer, finish = ' '.join(words[:mt]), 'length'
        used = sum(len(m['content'].split()) for m in msgs)
        return self._json(200, {'model': spec.get('model', 'itp-mini'), 'message': {'role': 'assistant', 'content': answer},
                                'finish_reason': finish, 'usage': {'prompt_tokens': used, 'completion_tokens': len(answer.split())}})

    def _users(self, method, p, body):
        rest = p[len(self.coll):].strip('/')
        if rest == '':
            if method == 'GET':
                return self._json(200, self.users)
            if method == 'POST':
                if not isinstance(body, dict):
                    return self._json(400, {'error': 'Нужен JSON-объект'})
                user = dict(body)
                user['id'] = max([u['id'] for u in self.users] + [0]) + 1
                self.users.append(user)
                return self._json(201, user)
            return 405, b'Method Not Allowed', 'text/plain; charset=utf-8'
        try:
            uid = int(rest)
        except ValueError:
            return self._json(404, {'error': 'Not found'})
        found = [u for u in self.users if u['id'] == uid]
        if not found:
            return self._json(404, {'error': 'Not found'})
        user = found[0]
        if method == 'GET':
            return self._json(200, user)
        if method in ('PUT', 'PATCH'):
            if not isinstance(body, dict):
                return self._json(400, {'error': 'Нужен JSON-объект'})
            user.update({k: v for k, v in body.items() if k != 'id'})
            return self._json(200, user)
        if method == 'DELETE':
            self.users.remove(user)
            return 204, b'', 'text/plain; charset=utf-8'
        return 405, b'Method Not Allowed', 'text/plain; charset=utf-8'


# Учебный сервер ИТП: есть всегда, на нём можно пробовать всё из темы.
DEMO = {
    'routes': {
        '/': {'text': 'Привет от учебного сервера ИТП!'},
        '/numbers': {'json': [3, 1, 4, 1, 5]},
        '/city': {'json': {'name': 'Тюмень', 'population': 855000}},
        '/count': {'seq': ['1', '2', '3', '0']},
    },
    'users': [
        {'id': 1, 'username': 'first', 'last_name': 'Петрова', 'first_name': 'Елизавета', 'email': 'e.petrova@server.none'},
        {'id': 2, 'username': 'second', 'last_name': 'Иванов', 'first_name': 'Василий', 'email': 'vas.ivanov@server.none'},
    ],
    'token': 'demo-token',
}
_SERVERS = None
_LAST = [None]


def _servers():
    global _SERVERS
    if _SERVERS is None:
        _SERVERS = {'127.0.0.1:5000': _Server(DEMO)}
        try:
            with open('_itp_servers.json', encoding='utf-8') as f:
                for addr, spec in _json.load(f).items():
                    _SERVERS[addr] = _Server(spec)
        except (OSError, ValueError):
            pass
    return _SERVERS


def _dump(address=None):
    """Для проверяющей системы: состояние списка users последнего сервера, к которому обращалась программа."""
    srv = _servers().get(address or _LAST[0])
    print(_json.dumps(srv.users, ensure_ascii=False, indent=4))


# ---------------------------------------------------------------- запросы
def request(method, url, params=None, data=None, json=None, headers=None, files=None, timeout=None, **kw):
    method = method.upper()
    url = str(url)
    parts = _urlsplit(url)
    if not parts.scheme:
        raise MissingSchema("Invalid URL '%s': No scheme supplied. Perhaps you meant https://%s?" % (url, url))
    if parts.scheme not in ('http', 'https'):
        raise InvalidURL('No connection adapters were found for %r' % url)
    if not parts.netloc:
        raise InvalidURL("Invalid URL '%s': No host supplied" % url)
    q = _parse_qsl(parts.query, keep_blank_values=True)
    if params:
        q += [(str(k), str(v)) for k, v in (params.items() if hasattr(params, 'items') else params)]
    full = '%s://%s%s' % (parts.scheme, parts.netloc, parts.path or '/')
    if q:
        full += '?' + _urlencode(q)
    srv = _servers().get(parts.netloc.lower())
    if srv is None:
        host, _, port = parts.netloc.partition(':')
        raise ConnectionError("HTTPConnectionPool(host='%s', port=%s): Max retries exceeded with url: %s "
                              "(Failed to establish a new connection: в ИТП программы работают без интернета, доступны только учебные серверы)"
                              % (host, port or (443 if parts.scheme == 'https' else 80), parts.path or '/'))
    _LAST[0] = parts.netloc.lower()
    hd = _Headers({'Accept': '*/*', 'User-Agent': 'python-requests/' + __version__})
    hd.update(headers or {})
    body = None
    if json is not None:
        body = _json.loads(_json.dumps(json))
        hd['Content-Type'] = 'application/json'
    elif isinstance(data, (str, bytes)):
        try:
            body = _json.loads(data)
        except ValueError:
            body = None
    elif isinstance(data, dict):
        body = dict(data)
    code, content, ctype = srv.handle(method, _unquote(parts.path or '/'), q, body, hd)
    r = Response(code, content if method != 'HEAD' else b'', {'Content-Type': ctype, 'Content-Length': str(len(content))}, full)
    return r


def get(url, params=None, **kw):
    return request('GET', url, params=params, **kw)


def post(url, data=None, json=None, **kw):
    return request('POST', url, data=data, json=json, **kw)


def put(url, data=None, **kw):
    return request('PUT', url, data=data, **kw)


def patch(url, data=None, **kw):
    return request('PATCH', url, data=data, **kw)


def delete(url, **kw):
    return request('DELETE', url, **kw)


def head(url, **kw):
    return request('HEAD', url, **kw)


class Session:
    def __init__(self):
        self.headers = _Headers()
        self.params = {}

    def request(self, method, url, headers=None, params=None, **kw):
        h = dict(self.headers)
        h.update(headers or {})
        p = dict(self.params)
        p.update(params or {})
        return request(method, url, params=p or None, headers=h, **kw)

    def get(self, url, **kw):
        return self.request('GET', url, **kw)

    def post(self, url, **kw):
        return self.request('POST', url, **kw)

    def put(self, url, **kw):
        return self.request('PUT', url, **kw)

    def delete(self, url, **kw):
        return self.request('DELETE', url, **kw)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
