from playwright.sync_api import sync_playwright
import h,t5,sys
touch = len(sys.argv)>1
with sync_playwright() as p:
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,390,1500,touch=touch)
    pg.wait_for_timeout(1000)
    ti=pg.evaluate("TOPICS.findIndex(function(x){return /^Задание 3\\./.test(x.n)})")
    pg.evaluate("S.mode='ex';save()")
    AI=pg.evaluate("TOPICS[%d].items.findIndex(function(x){return x.t==='ans'})"%ti)
    pg.evaluate("for(var u=0;u<%d;u++)S.d['%d-'+u]=1;save();go(%d,%d)"%(AI,ti,ti,AI)); pg.wait_for_timeout(400)
    pg.click('#exbs');pg.wait_for_timeout(200)
    def cell(r,c): return pg.locator('.exxtab td[data-r="%d"][data-c="%d"]'%(r,c))
    def tap(loc):
        if touch: loc.tap()
        else: loc.click()
    ok=True
    def chk(n,c):
        global ok
        print(('OK  ' if c else 'FAIL'),n); ok=ok and c
    tap(cell(1,6)); pg.wait_for_timeout(100)
    pg.focus('#xin'); pg.keyboard.type('=ВП'); pg.wait_for_timeout(100)
    chk('hint list shows ВПР', 'ВПР' in pg.inner_text('#xhint') and not pg.is_hidden('#xhint'))
    pg.locator('.exxs').first.click(); pg.wait_for_timeout(100)
    chk('inserted ВПР(', pg.input_value('#xin')=='=ВПР(')
    chk('signature shown', 'что_искать' in pg.inner_text('#xhint'))
    tap(cell(1,2)); pg.wait_for_timeout(100)
    chk('tap inserts C2', pg.input_value('#xin')=='=ВПР(C2')
    tap(cell(2,2)); pg.wait_for_timeout(100)
    chk('second tap replaces ref', pg.input_value('#xin')=='=ВПР(C3')
    tap(cell(1,2)); pg.keyboard.type(';'); pg.wait_for_timeout(100)
    chk('typed ;', pg.input_value('#xin')=='=ВПР(C2;')
    chk('arg 2 highlighted', '<u>таблица</u>' in pg.inner_html('#xhint'))
    pg.click('.exxt >> text=Магазин'); pg.wait_for_timeout(150)
    chk('editing kept after tab switch', pg.input_value('#xin')=='=ВПР(C2;')
    if touch:
        tap(cell(1,0)); pg.wait_for_timeout(100); 
        # drag handle to C7
        box=pg.locator('#xhd').bounding_box(); t=cell(6,2).bounding_box()
        pg.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2); pg.mouse.down(); pg.mouse.move(t['x']+t['width']/2,t['y']+t['height']/2,steps=8); pg.mouse.up()
    else:
        a=cell(1,0).bounding_box(); z=cell(6,2).bounding_box()
        pg.mouse.move(a['x']+10,a['y']+10);pg.mouse.down();pg.mouse.move(z['x']+10,z['y']+10,steps=8);pg.mouse.up()
    pg.wait_for_timeout(150)
    v=pg.input_value('#xin'); print(v)
    chk('range from other sheet', v=='=ВПР(C2;Магазин!A2:C7')
    pg.click('#xab'); pg.wait_for_timeout(100)
    v=pg.input_value('#xin'); print(v); chk('abs toggle', v=='=ВПР(C2;Магазин!$A$2:$C$7')
    pg.focus('#xin'); pg.keyboard.press('End'); pg.keyboard.type(';2;ЛОЖЬ'); pg.wait_for_timeout(50)
    pg.click('#xok'); pg.wait_for_timeout(200)
    f=pg.evaluate("EXSH_PROBE")if False else None
    chk('back on sheet 1 and value', pg.evaluate("document.querySelector('.exxt.on').textContent")=='Движение товаров')
    print('G2 shows',cell(1,6).inner_text())
    chk('G2 has district', cell(1,6).inner_text() in ('Северный','Заречный','Прибрежный','Восточный'))
    tap(cell(1,6)); pg.wait_for_timeout(100)
    chk('input shows formula with $', pg.input_value('#xin')=='=ВПР(C2;Магазин!$A$2:$C$7;2;ЛОЖЬ)')
    box=pg.locator('#xhd').bounding_box(); t=cell(8,6).bounding_box()
    pg.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2); pg.mouse.down(); pg.mouse.move(t['x']+t['width']/2,t['y']+t['height']/2,steps=10); pg.mouse.up(); pg.wait_for_timeout(200)
    print('G9 shows',cell(8,6).inner_text())
    chk('fill by handle', cell(8,6).inner_text() in ('Северный','Заречный','Прибрежный','Восточный'))
    tap(cell(8,6)); chk('G9 formula shifted', pg.input_value('#xin')=='=ВПР(C9;Магазин!$A$2:$C$7;2;ЛОЖЬ)')
    # column select + write to all
    tap(pg.locator('.exxtab th.ch[data-c="7"]')); pg.wait_for_timeout(100)
    pg.focus('#xin'); pg.keyboard.type('=E2*2'); pg.wait_for_timeout(100)
    chk('xall visible', not pg.is_hidden('#xall'))
    pg.click('#xall'); pg.wait_for_timeout(250)
    n=pg.evaluate("document.querySelectorAll('.exxtab td[data-c=\"7\"]').length")
    vals=[cell(r,7).inner_text() for r in (1,2,5)]; print(vals)
    chk('column filled', all(x!='' for x in vals))
    tap(cell(5,7)); chk('relative formula', pg.input_value('#xin')=='=E6*2')
    pg.screenshot(path='e43.png')
    print('logs',logs[:5]); print('ALL OK' if ok else 'SOME FAIL'); b.close()
