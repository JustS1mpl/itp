"""Фазз генераторов заданий ЕГЭ (бесконечный тренажёр): по 300 заданий каждого типа.

Запуск из корня репозитория после сборки: python3 tests/gen_fuzz.py
Ищет исключения, пустые ответы, undefined/NaN в тексте и типы, которые часто не удаётся создать
(тренажёр пробует до 30 раз, поэтому допустима доля неудач до 60%).
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h import open_page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = """async()=>{
 const rep=[],BAD=/undefined|NaN|Infinity|\\[object|null|\\{\\{/;
 for(const no of Object.keys(EXGEN)){const g=EXGEN[no];
  for(const t of ['any'].concat(g.types.map(x=>x.id))){
   let nul=0,exc=0,bad=0,empty=0,first='';const n=300;
   for(let i=0;i<n;i++){
     try{const q=g.make(t);if(!q){nul++;continue}
       const txt=[q.q,q.f,q.m,(q.h||[]).join(' '),(q.s||[]).join(' ')].join(' | ');
       if(BAD.test(txt)){bad++;if(!first)first=txt.slice(0,160)}
       if(q.a===undefined||q.a===null||String(q.a).trim()===''||BAD.test(String(q.a)))empty++;
     }catch(e){exc++;if(!first)first=String(e&&e.stack||e).slice(0,200)}}
   rep.push({no,t,n,nul,exc,bad,empty,first})}}
 return rep}"""

with sync_playwright() as p:
    b, ctx, pg, logs = open_page(p, ROOT + '/out5.html')
    pg.wait_for_timeout(1500)
    pg.set_default_timeout(600000)
    rep = pg.evaluate(JS)
    b.close()
bad = [r for r in rep if r['exc'] or r['bad'] or r['empty'] or r['nul'] > 0.6 * r['n']]
print(f'комбинаций {len(rep)}, с проблемами {len(bad)}')
for r in bad:
    print(json.dumps(r, ensure_ascii=False))
sys.exit(1 if bad else 0)
