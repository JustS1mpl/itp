"""Обход всех островков через настоящий интерфейс: теория, вопросы, код, проекты, задания ЕГЭ.

Запуск из корня репозитория (нужна сборка out5.html):
    python3 tests/crawl.py            # все темы (около 15 минут)
    python3 tests/crawl.py 1,5,15     # только темы с этими номерами
Печатает проблемы по островкам и итог. Код выхода 1, если что-то не прошло.
"""
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h import open_page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
only = {int(x) for x in sys.argv[1].split(',')} if len(sys.argv) > 1 else None

FLASH = """([i,j])=>{var q=IT(i,j).q,tx=document.querySelector('.q,h2'),t=tx?tx.textContent.trim():'',
  hit=q.find(function(x){return x.q.trim()===t})||q[0],want=String(hit.o[hit.a]).trim(),
  bs=[].slice.call(document.querySelectorAll('.opt')),b=bs.find(function(x){return x.textContent.trim()===want})||bs[0];
  b.click();document.getElementById('go').click()}"""
CODE = """([i,j,k,isTask])=>{var it=IT(i,j),sol=isTask?it.tasks[k].sol:it.sol,ed=document.getElementById('code');
  ed.value=sol;ed.dispatchEvent(new Event('input',{bubbles:true}));(document.getElementById('chk')||document.getElementById('pchk')).click()}"""
ANS = """([i,j,k])=>{var q=IT(i,j).tasks[k],ai=document.getElementById('ai');ai.value=q.a;
  document.getElementById('af').dispatchEvent(new Event('submit',{cancelable:true,bubbles:true}))}"""

problems = []
with sync_playwright() as p:
    b, ctx, pg, logs = open_page(p, ROOT + '/out5.html')
    pg.set_default_timeout(20000)
    pg.wait_for_timeout(1500)
    # откроем все островки, чтобы не зависеть от порядка прохождения
    pg.evaluate("()=>{S.nick='crawl';S.start=1;S.reg=day(new Date());save();isOpen=function(){return 1};home()}")
    info = pg.evaluate("TOPICS.map(t=>(t.items||[]).map(x=>({t:x.t,nq:(x.q||x.tasks||[]).length})))")
    for i, items in enumerate(info):
        if i == 0 or (only is not None and i not in only):
            continue
        for j, it in enumerate(items):
            n0 = len(logs)
            err = ''
            try:
                pg.evaluate(f"go({i},{j})")
                pg.wait_for_timeout(120)
                t = it['t']
                if t == 'theory':
                    pg.evaluate("document.querySelectorAll('.th .tm,.th [data-term]').forEach(b=>b.click())")
                    pg.wait_for_selector('#go', state='attached')
                    pg.evaluate("document.getElementById('go').click()")
                elif t == 'flash':
                    for _ in range(it['nq']):
                        pg.wait_for_selector('.opt', state='attached')
                        pg.evaluate(FLASH, [i, j])
                        pg.wait_for_timeout(60)
                        pg.evaluate("document.getElementById('go')&&document.getElementById('go').click()")
                        pg.wait_for_timeout(60)
                elif t in ('test', 'project'):
                    for k in range(it['nq'] if t == 'test' else 1):
                        pg.wait_for_selector('#code', state='attached')
                        pg.evaluate(CODE, [i, j, k, t == 'test'])
                        if t == 'project':
                            pg.wait_for_function("document.querySelector('.center #go')", timeout=30000)
                            pg.evaluate("document.getElementById('go').click()")
                        else:
                            pg.wait_for_function("document.getElementById('nx')", timeout=30000)
                            pg.evaluate("document.getElementById('nx').click()")
                        pg.wait_for_timeout(80)
                elif t == 'ans':
                    for k in range(it['nq']):
                        pg.wait_for_selector('#ai', state='attached')
                        pg.evaluate(ANS, [i, j, k])
                        pg.wait_for_selector('#nx', state='attached')
                        pg.evaluate("document.getElementById('nx').click()")
                        pg.wait_for_timeout(80)
            except Exception as e:  # noqa: BLE001
                err = str(e).split('\n')[0][:200]
            new = logs[n0:]
            if err or new:
                problems.append((i, j, it['t'], err, new[:3]))
                print('ПРОБЛЕМА', i, j, it['t'], err, new[:3], flush=True)
            pg.evaluate("home()")
        print('тема', i, 'пройдена, проблем всего:', len(problems), flush=True)
    b.close()
print('ИТОГО проблем:', len(problems))
sys.exit(1 if problems else 0)
