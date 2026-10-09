"""Упрощённый модуль turtle для «И так Пайтон»: считает всё в Python, рисует окно приложения."""
import math as _m
import json as _json

__all__ = ['Turtle', 'Pen', 'RawTurtle', 'Screen', 'Vec2D', 'TurtleScreen', 'Terminator', 'TurtleGraphicsError',
           'forward', 'fd', 'backward', 'bk', 'back', 'left', 'lt', 'right', 'rt', 'goto', 'setpos', 'setposition',
           'setx', 'sety', 'setheading', 'seth', 'home', 'circle', 'dot', 'stamp', 'clearstamps', 'speed',
           'penup', 'pu', 'up', 'pendown', 'pd', 'down', 'pensize', 'width', 'isdown', 'pen',
           'color', 'pencolor', 'fillcolor', 'filling', 'begin_fill', 'end_fill', 'reset', 'clear', 'write',
           'showturtle', 'st', 'hideturtle', 'ht', 'isvisible', 'shape', 'shapesize', 'turtlesize', 'resizemode',
           'pos', 'position', 'xcor', 'ycor', 'heading', 'distance', 'towards', 'degrees', 'radians',
           'tracer', 'update', 'delay', 'bgcolor', 'setup', 'title', 'screensize', 'mainloop', 'done', 'exitonclick',
           'colormode', 'mode', 'setworldcoordinates', 'getscreen', 'listen', 'onkey', 'onkeypress', 'onkeyrelease',
           'onclick', 'onscreenclick', 'ontimer', 'bye', 'clearscreen', 'resetscreen', 'window_width', 'window_height',
           'textinput', 'numinput', 'undo', 'clone', 'getturtle', 'getpen', 'onrelease', 'ondrag', 'write_docstringdict',
           'bgpic', 'register_shape', 'addshape', 'tracer', 'getcanvas', 'teleport']

_LOG = []
_TUR = []
_VIEW = {'bg': '#ffffff', 'w': None, 'title': ''}
_CAP = 120000
_STATE = {'cut': 0, 'colormode': 1.0, 'tracer': 1}
_NAMES = {'red': '#ff0000', 'green': '#008000', 'blue': '#0000ff', 'black': '#000000', 'white': '#ffffff',
          'yellow': '#ffff00', 'orange': '#ffa500', 'purple': '#800080', 'pink': '#ffc0cb', 'brown': '#a52a2a',
          'gray': '#808080', 'grey': '#808080', 'cyan': '#00ffff', 'magenta': '#ff00ff', 'gold': '#ffd700'}


class TurtleGraphicsError(Exception):
    pass


class Terminator(Exception):
    pass


class Vec2D(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, o):
        return Vec2D(self[0] + o[0], self[1] + o[1])

    def __sub__(self, o):
        return Vec2D(self[0] - o[0], self[1] - o[1])

    def __mul__(self, o):
        if isinstance(o, (int, float)):
            return Vec2D(self[0] * o, self[1] * o)
        return self[0] * o[0] + self[1] * o[1]

    def __rmul__(self, o):
        if isinstance(o, (int, float)):
            return Vec2D(self[0] * o, self[1] * o)
        return NotImplemented

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return (self[0] ** 2 + self[1] ** 2) ** 0.5

    def rotate(self, angle):
        a = _m.radians(angle)
        c, s = _m.cos(a), _m.sin(a)
        return Vec2D(self[0] * c - self[1] * s, self[0] * s + self[1] * c)

    def __repr__(self):
        return '(%.2f,%.2f)' % self


def _col(args, who='color'):
    if len(args) == 1:
        a = args[0]
        if isinstance(a, str):
            a = a.strip()
            if a.startswith('#'):
                if len(a) in (4, 7) and all(c in '0123456789abcdefABCDEF' for c in a[1:]):
                    return a.lower()
                raise TurtleGraphicsError('bad color string: %s' % a)
            if a.isalpha():
                return _NAMES.get(a.lower(), a.lower())
            raise TurtleGraphicsError('bad color string: %s' % a)
        if isinstance(a, (tuple, list)) and len(a) == 3:
            args = tuple(a)
        else:
            raise TurtleGraphicsError('bad color arguments: %r' % (args,))
    if len(args) == 3:
        k = _STATE['colormode']
        v = []
        for x in args:
            if not 0 <= x <= k:
                raise TurtleGraphicsError('bad color sequence: %r' % (args,))
            v.append(int(round(x * 255.0 / k)))
        return '#%02x%02x%02x' % tuple(v)
    raise TurtleGraphicsError('bad color arguments: %r' % (args,))


def _r(v):
    return round(v + 0.0, 4)


def _add(op):
    if len(_LOG) >= _CAP:
        _STATE['cut'] = 1
        return -1
    _LOG.append(op)
    return len(_LOG) - 1


class Turtle(object):
    def __init__(self, shape='classic', undobuffersize=1000, visible=True):
        self._x = 0.0
        self._y = 0.0
        self._h = 0.0
        self._full = 360.0
        self._down = True
        self._ps = 1
        self._pc = '#000000'
        self._fc = '#000000'
        self._vis = visible
        self._fill = None
        self._fi = -1
        self._spd = 3
        self._rm = 'noresize'
        _TUR.append(self)

    # ---- движение
    def _go(self, nx, ny):
        nx = round(nx, 10) + 0.0
        ny = round(ny, 10) + 0.0
        d = 1 if self._down else 0
        _add([0, _r(self._x), _r(self._y), _r(nx), _r(ny), d, self._pc, self._ps])
        self._x, self._y = nx, ny
        if self._fill is not None:
            self._fill.append((nx, ny))

    def forward(self, distance):
        a = _m.radians(self._h * 360.0 / self._full)
        self._go(self._x + distance * _m.cos(a), self._y + distance * _m.sin(a))

    def backward(self, distance):
        self.forward(-distance)

    def left(self, angle):
        self._h = (self._h + angle) % self._full

    def right(self, angle):
        self.left(-angle)

    def goto(self, x, y=None):
        if y is None:
            x, y = x
        self._go(float(x), float(y))

    def setx(self, x):
        self._go(float(x), self._y)

    def sety(self, y):
        self._go(self._x, float(y))

    def setheading(self, to_angle):
        self._h = to_angle % self._full

    def home(self):
        self.goto(0, 0)
        self.setheading(0)

    def circle(self, radius, extent=None, steps=None):
        if extent is None:
            extent = self._full
        frac = abs(extent) / self._full
        if steps is None:
            steps = 1 + int(min(11 + abs(radius) / 6.0, 59.0) * frac)
        w = 1.0 * extent / steps
        w2 = 0.5 * w
        l = 2.0 * radius * _m.sin(_m.radians(w2 * 360.0 / self._full))
        if radius < 0:
            l, w, w2 = -l, -w, -w2
        self.left(w2)
        for _ in range(steps):
            self.forward(l)
            self.left(w)
        self.right(w2)

    def dot(self, size=None, *color):
        if not color:
            c = self._pc
            if isinstance(size, (str, tuple)):
                c, size = _col((size,)), None
        else:
            c = _col(color if len(color) != 1 else color)
        if size is None:
            size = max(self._ps + 4, 2 * self._ps)
        _add([1, _r(self._x), _r(self._y), size, c])

    def stamp(self):
        _add([4, _r(self._x), _r(self._y), _r(self._h * 360.0 / self._full), self._pc, self._fc])
        return len(_LOG)

    def clearstamps(self, n=None):
        pass

    def write(self, arg, move=False, align='left', font=('Arial', 8, 'normal')):
        sz = 8
        try:
            sz = int(font[1])
        except Exception:
            pass
        _add([2, _r(self._x), _r(self._y), str(arg), self._pc, sz, align])

    def undo(self):
        pass

    # ---- перо
    def penup(self):
        self._down = False

    def pendown(self):
        self._down = True

    def isdown(self):
        return self._down

    def pensize(self, width=None):
        if width is None:
            return self._ps
        self._ps = width

    def pencolor(self, *args):
        if not args:
            return self._pc
        self._pc = _col(args)

    def fillcolor(self, *args):
        if not args:
            return self._fc
        self._fc = _col(args)

    def color(self, *args):
        if not args:
            return (self._pc, self._fc)
        if len(args) == 2:
            self._pc, self._fc = _col((args[0],)), _col((args[1],))
        else:
            self._pc = self._fc = _col(args)

    def begin_fill(self):
        self._fill = [(self._x, self._y)]
        self._fi = _add([3, [], self._fc])

    def end_fill(self):
        if self._fill is not None and self._fi >= 0:
            _LOG[self._fi] = [3, [[_r(a), _r(b)] for a, b in self._fill], self._fc]
        self._fill = None
        self._fi = -1

    def filling(self):
        return self._fill is not None

    def pen(self, pen=None, **pd):
        d = {'shown': self._vis, 'pendown': self._down, 'pencolor': self._pc, 'fillcolor': self._fc,
             'pensize': self._ps, 'speed': self._spd}
        if pen is None and not pd:
            return d
        if pen:
            pd.update(pen)
        if 'pendown' in pd:
            self._down = bool(pd['pendown'])
        if 'pencolor' in pd:
            self.pencolor(pd['pencolor'])
        if 'fillcolor' in pd:
            self.fillcolor(pd['fillcolor'])
        if 'pensize' in pd:
            self._ps = pd['pensize']
        if 'shown' in pd:
            self._vis = bool(pd['shown'])

    def speed(self, speed=None):
        if speed is None:
            return self._spd
        if isinstance(speed, str):
            speed = {'fastest': 0, 'fast': 10, 'normal': 6, 'slow': 3, 'slowest': 1}.get(speed, 3)
        self._spd = speed

    def showturtle(self):
        self._vis = True

    def hideturtle(self):
        self._vis = False

    def isvisible(self):
        return self._vis

    def shape(self, name=None):
        return 'classic' if name is None else None

    def shapesize(self, *a, **k):
        pass

    def resizemode(self, *a):
        pass

    def reset(self):
        self.clear()
        self._x = self._y = 0.0
        self._h = 0.0
        self._down = True
        self._ps = 1
        self._pc = self._fc = '#000000'

    def clear(self):
        del _LOG[:]

    # ---- узнать
    def position(self):
        return Vec2D(self._x, self._y)

    def xcor(self):
        return self._x

    def ycor(self):
        return self._y

    def heading(self):
        return self._h

    def distance(self, x, y=None):
        if y is None:
            x, y = x
        return ((x - self._x) ** 2 + (y - self._y) ** 2) ** 0.5

    def towards(self, x, y=None):
        if y is None:
            x, y = x
        a = _m.degrees(_m.atan2(y - self._y, x - self._x))
        return (a * self._full / 360.0) % self._full

    def degrees(self, fullcircle=360.0):
        self._h = self._h * fullcircle / self._full
        self._full = float(fullcircle)

    def radians(self):
        self.degrees(2 * _m.pi)

    def clone(self):
        t = Turtle()
        for k in ('_x', '_y', '_h', '_full', '_down', '_ps', '_pc', '_fc', '_vis', '_spd'):
            setattr(t, k, getattr(self, k))
        return t

    def getscreen(self):
        return _SCR

    def onclick(self, *a, **k):
        pass

    onrelease = ondrag = onclick

    def getturtle(self):
        return self

    getpen = getturtle

    def teleport(self, x=None, y=None, **k):
        if x is not None:
            self._x = float(x)
        if y is not None:
            self._y = float(y)

    fd = forward
    bk = back = backward
    lt = left
    rt = right
    setpos = setposition = goto
    seth = setheading
    pu = up = penup
    pd = down = pendown
    width = pensize
    ht = hideturtle
    st = showturtle
    pos = position
    turtlesize = shapesize


RawTurtle = Pen = Turtle


class TurtleScreen(object):
    def tracer(self, n=None, delay=None):
        if n is None:
            return _STATE['tracer']
        _STATE['tracer'] = n

    def update(self):
        pass

    def delay(self, d=None):
        return 10 if d is None else None

    def bgcolor(self, *args):
        if not args:
            return _VIEW['bg']
        _VIEW['bg'] = _col(args)

    def setup(self, width=0.5, height=0.5, startx=None, starty=None):
        pass

    def title(self, t):
        _VIEW['title'] = str(t)

    def screensize(self, canvwidth=None, canvheight=None, bg=None):
        if canvwidth is None and canvheight is None and bg is None:
            return (400, 300)
        if bg:
            self.bgcolor(bg)

    def mainloop(self):
        pass

    done = exitonclick = bye = mainloop

    def colormode(self, cmode=None):
        if cmode is None:
            return _STATE['colormode']
        _STATE['colormode'] = float(cmode)

    def mode(self, mode=None):
        return 'standard' if mode is None else None

    def setworldcoordinates(self, llx, lly, urx, ury):
        _VIEW['w'] = [llx, lly, urx, ury]

    def window_width(self):
        return 400

    def window_height(self):
        return 300

    def listen(self, *a, **k):
        pass

    onkey = onkeypress = onkeyrelease = onclick = onscreenclick = listen

    def ontimer(self, fun, t=0):
        pass

    def clearscreen(self):
        del _LOG[:]

    clear = clearscreen

    def resetscreen(self):
        pass

    reset = resetscreen

    def textinput(self, title, prompt):
        return None

    numinput = textinput

    def bgpic(self, *a):
        pass

    def register_shape(self, *a):
        pass

    addshape = register_shape

    def getcanvas(self):
        return None

    def write_docstringdict(self, *a):
        pass


_SCR = TurtleScreen()


def Screen():
    return _SCR


_T = [None]


def _def():
    if _T[0] is None:
        _T[0] = Turtle()
    return _T[0]


def _mk(n):
    def f(*a, **k):
        return getattr(_def(), n)(*a, **k)
    f.__name__ = n
    return f


for _n in ('forward fd backward bk back left lt right rt goto setpos setposition setx sety setheading seth home circle dot '
           'stamp clearstamps speed penup pu up pendown pd down pensize width isdown pen color pencolor fillcolor filling '
           'begin_fill end_fill reset clear write showturtle st hideturtle ht isvisible shape shapesize turtlesize resizemode '
           'pos position xcor ycor heading distance towards degrees radians undo teleport').split():
    globals()[_n] = _mk(_n)


def _mks(n):
    def f(*a, **k):
        return getattr(_SCR, n)(*a, **k)
    f.__name__ = n
    return f


for _n in ('tracer update delay bgcolor setup title screensize mainloop done exitonclick colormode mode '
           'setworldcoordinates listen onkey onkeypress onkeyrelease onscreenclick ontimer bye clearscreen resetscreen '
           'window_width window_height textinput numinput bgpic register_shape addshape getcanvas').split():
    globals()[_n] = _mks(_n)


def onclick(*a, **k):
    pass


def getscreen():
    return _SCR


def getturtle():
    return _def()


getpen = getturtle


def _dump():
    if not _LOG and not _TUR:
        return None
    ts = [[_r(t._x), _r(t._y), _r(t._h * 360.0 / t._full), 1 if t._vis else 0, t._pc, t._fc] for t in _TUR[:20]]
    if not _LOG and not any(t[3] for t in ts):
        return None
    return _json.dumps({'ops': _LOG, 'tur': ts, 'bg': _VIEW['bg'], 'w': _VIEW['w'], 'title': _VIEW['title'],
                        'cut': _STATE['cut']}, separators=(',', ':'))


__all__ = [n for n in __all__ if n in globals()]
