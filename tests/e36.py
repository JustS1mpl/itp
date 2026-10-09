from playwright.sync_api import sync_playwright
import h,t5
with sync_playwright() as p:
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,420,860,touch=False)
    pg.wait_for_timeout(1000)
    ti=pg.evaluate("TOPICS.findIndex(function(x){return /^Задание 3\\./.test(x.n)})")
    pg.evaluate("S.mode='ex';save()")
    AI=pg.evaluate("TOPICS[%d].items.findIndex(function(x){return x.t==='ans'})"%ti)
    pg.evaluate("for(var u=0;u<%d;u++)S.d['%d-'+u]=1;save();go(%d,%d)"%(AI,ti,ti,AI)); pg.wait_for_timeout(400)
    Q=pg.evaluate("IT(%d,%d).tasks[0].query"%(ti,AI));A=pg.evaluate("IT(%d,%d).tasks[0].a"%(ti,AI));print(Q,A)
    pg.click('#exbs');pg.wait_for_timeout(300)
    pg.screenshot(path='f3_sheet0.png',full_page=True)
    def cell(r,c): return pg.locator('.exxtab td[data-r="%d"][data-c="%d"]'%(r,c))
    def typ(r,c,t):
        cell(r,c).click();pg.fill('#xin',t);pg.press('#xin','Enter');pg.wait_for_timeout(60)
    n=pg.evaluate("IT(%d,%d).tasks[0].db[0].r.length"%(ti,AI));ns=pg.evaluate("IT(%d,%d).tasks[0].db[2].r.length"%(ti,AI));np_=pg.evaluate("IT(%d,%d).tasks[0].db[1].r.length"%(ti,AI))
    typ(0,6,'Район'); typ(1,6,'=ВПР(C2;Магазин!$A$2:$C$%d;2;ЛОЖЬ)'%(ns+1))
    cell(1,6).click();pg.click('#xfd');pg.wait_for_timeout(100)
    typ(0,7,'Наим');typ(1,7,'=ВПР(D2;Товар!$A$2:$F$%d;3;ЛОЖЬ)'%(np_+1));cell(1,7).click();pg.click('#xfd')
    print('G3 shows',cell(2,6).inner_text(),'H3',cell(2,7).inner_text(), 'last',cell(n,6).inner_text())
    # фильтр
    pg.click('#xfo');pg.wait_for_timeout(100)
    pg.select_option('#xfc','5');pg.select_option('#xfp','eq');pg.fill('#xf1',Q.get('op','Продажа') if Q.get('op') else 'Продажа');pg.click('#xfa');pg.wait_for_timeout(100)
    print('visible rows',pg.evaluate("document.querySelectorAll('.exxtab tr').length"),pg.inner_text('.exxfl'))
    pg.click('.exxtab th.ch[data-c="4"]');pg.wait_for_timeout(100);print('status',pg.inner_text('.exxst'))
    pg.screenshot(path='f3_sheet1.png',full_page=True)
    print('logs',logs[:3]);b.close()
