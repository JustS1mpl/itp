from playwright.sync_api import sync_playwright
import h,t5,sys
with sync_playwright() as p:
  for W,theme in [(390,'dark'),(360,'light')]:
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,W,860)
    pg.wait_for_timeout(800)
    if theme=='light': pg.evaluate("S.theme='light';save();applyTheme&&applyTheme()") if False else None
    ti=pg.evaluate("TOPICS.findIndex(function(x){return /^Задание 5\\./.test(x.n)})")
    print(W,'topic idx',ti)
    pg.evaluate("S.mode='ex';save()")
    J=pg.evaluate("TOPICS[%d].items.map(function(x,i){return i+':'+x.t+':'+x.n+':'+x.g})"%ti)
    print(len(J),J[:4])
    pg.evaluate("for(var u=0;u<60;u++)S.d['%d-'+u]=1;save();go(%d,0)"%(ti,ti)); pg.wait_for_timeout(500)
    pg.screenshot(path='n5_t1_%d.png'%W)
    AI=pg.evaluate("TOPICS[%d].items.findIndex(function(x){return x.t==='ans'})"%ti)
    pg.evaluate("go(%d,%d)"%(ti,AI)); pg.wait_for_timeout(500)
    print('statement:',pg.inner_text('.exst')[:400].replace('\n',' | '))
    print('tools',pg.locator('.extl button').count(),'tu btn',pg.locator('#exbt').count(),'details',pg.locator('.exdt').count())
    pg.screenshot(path='n5_a1_%d.png'%W)
    pg.click('#exbc'); pg.wait_for_timeout(300)
    print('starter:',pg.input_value('#code')[:160].replace('\n',' / '))
    ans=pg.evaluate("TOPICS[%d].items[%d].tasks[0].a"%(ti,AI)); print('ans',ans)
    pg.fill('#ai',ans); pg.click('#ac'); pg.wait_for_timeout(500); print('feedback:',pg.inner_text('#fb')[:120].replace('\n',' | '))
    pg.screenshot(path='n5_a2_%d.png'%W)
    for t in ['5.1','5.2','5.3','5.4','5.5','5.6','5.7','any']:
        pg.evaluate("EXST={ok:0,all:0};exTrain(5,'%s')"%t); pg.wait_for_timeout(250)
        print(t,pg.inner_text('.exst')[:150].replace('\n',' | '))
    pg.screenshot(path='n5_tr_%d.png'%W)
    ov=pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
    print('overflow',ov,[l for l in logs if 'rror' in l][:6])
    b.close()
