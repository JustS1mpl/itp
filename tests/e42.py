from playwright.sync_api import sync_playwright
import h,t5
with sync_playwright() as p:
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,420,860,touch=False)
    pg.wait_for_timeout(800)
    pg.evaluate("window.__s=[];Object.keys(SNDS).forEach(k=>{const f=SNDS[k];SNDS[k]=function(){__s.push(k+':'+(new Error().stack.split('\\n').slice(2,5).map(x=>x.trim().split(' ')[1]).join('<')));return f.apply(this,arguments)}})")
    for lab in ['mx','mx','mx']:
        pg.evaluate("__s.length=0");pg.click('[data-t="mx"]');pg.wait_for_timeout(600)
        print(lab,pg.evaluate("S.mode"),pg.evaluate("__s"))
    b.close()
