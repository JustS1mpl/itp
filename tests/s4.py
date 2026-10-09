from playwright.sync_api import sync_playwright
import h,t5
with sync_playwright() as p:
    for W in (320,360,390):
        b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,W,740,touch=True)
        pg.wait_for_timeout(1000)
        for th in ['light','dark']:
            pg.evaluate("document.documentElement.dataset.theme='%s'"%th)
            for n,js in [('home',"S.mode='py';save();home()"),('pr',"practice()"),('ed',"editor()"),('prof',"profile()"),('set',"settings()"),('exh',"S.mode='ex';save();home()"),('exm',"exMenu()"),('lesson',"S.mode='py';go(1,1)"),('test',"go(1,4)")]:
                pg.evaluate(js);pg.wait_for_timeout(250)
                o=pg.evaluate("[document.documentElement.scrollWidth,innerWidth,Array.from(document.querySelectorAll('.top *')).filter(e=>e.getBoundingClientRect().right>innerWidth+1).length]")
                if o[0]>o[1] or o[2]: print(W,th,n,o)
        b.close()
print('done')
