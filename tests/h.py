import json, sys, os
from playwright.sync_api import sync_playwright
W=os.path.dirname(os.path.abspath(__file__))
SK=W+'/sk/'
def route(r):
    u=r.request.url
    if 'skulpt@1.2.0/dist/' in u:
        f=u.split('/dist/')[1]
        r.fulfill(path=SK+f, content_type='application/javascript')
    elif 'fonts.googleapis' in u or 'gstatic' in u:
        r.fulfill(status=200, body='', content_type='text/css')
    else:
        r.continue_()
def open_page(p, path, state=None, w=420, h=860, touch=False, **kw):
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome' if os.path.exists('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') else None, args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':w,'height':h}, has_touch=touch, is_mobile=touch, **kw)
    ctx.route('**/*', route)
    pg=ctx.new_page()
    logs=[]
    pg.on('console', lambda m: logs.append(m.type+': '+m.text))
    pg.on('pageerror', lambda e: logs.append('PAGEERROR: '+str(e)))
    if state is not None:
        ctx.add_init_script("if(!sessionStorage.__seeded){sessionStorage.__seeded=1;localStorage.setItem('pyshag2',%s)}"%json.dumps(json.dumps(state)))
    pg.goto('file://'+path)
    return b,ctx,pg,logs
