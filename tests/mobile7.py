# 7.0, фаза 4: удобство на телефоне. Запуск: python tests/mobile7.py [out5.html] [папка для снимков]
# Проверяет на пяти размерах: нет горизонтальной прокрутки на экранах заданий, вопросов и проекта;
# полоска символов появляется при фокусе в редакторе и прячет нижнюю панель; кнопки полоски вставляют
# то, что нужно; «вернуть начальный код» спрашивает и возвращает шаблон; строка с курсором не уходит под полоску.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from h import open_page

PAGE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else 'out5.html')
SHOTS = sys.argv[2] if len(sys.argv) > 2 else ''
SIZES = [(360, 640), (390, 844), (412, 915), (768, 1024), (844, 390)]
bad = []

def chk(ok, msg):
    if not ok:
        bad.append(msg)
        print('  FAIL', msg)

def settle(pg):
    pg.wait_for_timeout(500)
    pg.evaluate("document.getAnimations().forEach(a=>{try{a.finish()}catch(e){}})")

FIND = """(re)=>{for(let i=0;i<TOPICS.length;i++)for(let j=0;j<TOPICS[i].items.length;j++){const it=TOPICS[i].items[j];
  if(it.t==='test')for(let k=0;k<it.tasks.length;k++)if(new RegExp(re).test(it.tasks[k].q))return [i,j,k]}}"""
PROJ = """(re)=>{for(let i=0;i<TOPICS.length;i++)for(let j=0;j<TOPICS[i].items.length;j++){const it=TOPICS[i].items[j];
  if(it.t==='project'&&new RegExp(re).test(it.n))return [i,j]}}"""
QUIZ = """()=>{for(let i=0;i<TOPICS.length;i++)for(let j=0;j<TOPICS[i].items.length;j++)if(TOPICS[i].items[j].t==='flash')return [i,j]}"""
WIDE = "document.documentElement.scrollWidth<=innerWidth"

with sync_playwright() as p:
    for w, hgt in SIZES:
        tag = f'{w}x{hgt}'
        print(tag)
        b, c, pg, logs = open_page(p, PAGE, w=w, h=hgt, touch=True)
        pg.wait_for_timeout(2000)
        pg.evaluate("S.nick='Тест';S.start=0;save()"); pg.reload(); pg.wait_for_timeout(2000)

        i, j = pg.evaluate(QUIZ)
        pg.evaluate(f"quiz({i},{j})"); settle(pg)
        chk(pg.evaluate(WIDE), f'{tag}: вопрос шире экрана')

        i, j, k = pg.evaluate(FIND, 'Склеить')
        pg.evaluate(f"task({i},{j},{k})"); settle(pg)
        chk(pg.evaluate(WIDE), f'{tag}: задание шире экрана')
        chk(pg.evaluate("!document.getElementById('edk')"), f'{tag}: подсказка про Ctrl + Enter на сенсорном экране')
        tpl = pg.evaluate("document.querySelector('.rsb').dataset.tpl")
        chk(pg.evaluate("document.getElementById('code').value") == tpl, f'{tag}: в редакторе не шаблон')

        pg.locator('#code').tap(); pg.wait_for_timeout(500)
        chk(pg.evaluate("!document.querySelector('.kbar').hidden"), f'{tag}: полоска не появилась')
        chk(pg.evaluate("getComputedStyle(document.querySelector('.dock')).visibility==='hidden'"), f'{tag}: нижняя панель не спряталась')
        bw = pg.evaluate("[document.querySelector('.kbar').scrollWidth>document.querySelector('.kbar').clientWidth||innerWidth>=900, "+WIDE+"]")
        chk(bw[1], f'{tag}: с полоской страница шире экрана')

        def key(k):
            pg.evaluate("(k)=>[...document.querySelectorAll('.kbar button')].find(b=>b.dataset.k===k).click()", k)
        pg.evaluate("c=document.getElementById('code');c.value='';c.dispatchEvent(new Event('input'))")
        for k in ['⇥', 'p', '(', '"', 'x', '"', ')', ':']:
            if k == 'p':
                pg.keyboard.type('print')
            elif k == 'x':
                pg.keyboard.type('x')
            else:
                key(k)
        v = pg.evaluate("document.getElementById('code').value")
        chk(v == '    print("x"):', f'{tag}: полоска вставила {v!r}')
        key('⇤')
        v = pg.evaluate("document.getElementById('code').value")
        chk(v == 'print("x"):', f'{tag}: «убрать отступ» дал {v!r}')
        key('←'); key('←')
        chk(pg.evaluate("document.getElementById('code').selectionStart") == len(v) - 2, f'{tag}: стрелка влево')
        chk(pg.evaluate("document.activeElement.id") == 'code', f'{tag}: полоска забрала фокус')

        # длинный код: строка с курсором должна оставаться над полоской
        pg.evaluate("c=document.getElementById('code');c.setSelectionRange(c.value.length,c.value.length)")
        for n in range(30):
            pg.keyboard.press('Enter'); pg.keyboard.type(f'x{n} = {n}')
        pg.wait_for_timeout(300)
        r = pg.evaluate("""(()=>{const c=document.getElementById('code'),cs=getComputedStyle(c),lh=parseFloat(cs.lineHeight),
          ln=c.value.slice(0,c.selectionEnd).split('\\n').length-1,y=c.getBoundingClientRect().top+parseFloat(cs.paddingTop)+ln*lh;
          return [y+lh, document.querySelector('.kbar').getBoundingClientRect().top]})()""")
        chk(r[0] <= r[1] + 1, f'{tag}: курсор под полоской {r}')
        if SHOTS:
            pg.screenshot(path=os.path.join(SHOTS, f'kbar_{tag}.png'))

        # сброс к шаблону
        pg.evaluate("document.activeElement.blur()"); pg.wait_for_timeout(300)
        chk(pg.evaluate("document.querySelector('.kbar').hidden"), f'{tag}: полоска не спряталась после выхода из редактора')
        pg.locator('.rsb').tap(); pg.wait_for_timeout(400)
        pg.locator('.modal button, [role=dialog] button').filter(has_text='Вернуть').first.tap(); pg.wait_for_timeout(400)
        chk(pg.evaluate("document.getElementById('code').value") == tpl, f'{tag}: сброс не вернул шаблон')

        i, j = pg.evaluate(PROJ, 'Дневник')
        pg.evaluate(f"project({i},{j})"); settle(pg)
        chk(pg.evaluate(WIDE), f'{tag}: проект шире экрана')
        if SHOTS:
            pg.screenshot(path=os.path.join(SHOTS, f'proj7_{tag}.png'))

        errs = [l for l in logs if l.startswith('PAGEERROR') or l.startswith('error')]
        chk(not errs, f'{tag}: ошибки в консоли {errs[:3]}')
        b.close()

print('bad', len(bad))
sys.exit(1 if bad else 0)
