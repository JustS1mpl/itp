"""Устойчивость к повреждённому сохранению: clean() и все экраны на 400 случайно испорченных состояниях.

Запуск из корня репозитория после сборки: python3 tests/state_fuzz.py
Также проверяет, что нормальное состояние проходит цикл «сохранить → прочитать» без потерь.
"""
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h import open_page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = """()=>{
 const errs={};let n=0;
 const rnd=a=>a[Math.floor(Math.random()*a.length)];
 const junk=[null,undefined,NaN,-1,1e12,'x','',[],{},[1,2],{a:1},'2026-13-45','2026-02-30','9999-99-99',true,false,'__proto__',0.5,'1-2','0-0'];
 const base=JSON.parse(JSON.stringify(S));
 base.nick='Тест';base.start=2;base.xp=500;base.streak=3;base.max=5;base.last=day(new Date());
 TOPICS.forEach((t,i)=>{if(i<4)(t.items||[]).forEach((x,j)=>{base.d[i+'-'+j]=1;base.es[i+'-'+j]=1})});
 base.sv=[{id:'a1',n:'код',c:'print(1)',t:1}];base.cur='a1';base.nt={print:'z'};base.ach={intro:day(new Date())};
 const keys=Object.keys(base);
 const scr={home:()=>home(),profile:()=>profile(),settings:()=>settings(),dict:()=>dict(),editor:()=>editor(),practice:()=>practice(),
   exhome:()=>{S.mode='ex';home();S.mode='py'},streak:()=>streakSheet(),level:()=>levelSheet(),codes:()=>codes()};
 const same=JSON.stringify(clean(JSON.parse(JSON.stringify(base))))===JSON.stringify(base);
 for(let it=0;it<400;it++){
   const o=JSON.parse(JSON.stringify(base)),k=rnd(keys);
   if(Math.random()<.5||!o[k]||typeof o[k]!=='object'||Array.isArray(o[k]))o[k]=rnd(junk);
   else{const kk=Object.keys(o[k]);o[k][kk.length?rnd(kk):'zz']=rnd(junk)}
   if(Math.random()<.2)o[rnd(keys)]=rnd(junk);
   let c;try{c=clean(o)}catch(e){errs['clean:'+k+':'+String(e).slice(0,80)]=1;continue}
   S=c;seedLit();n++;
   for(const [nm,f] of Object.entries(scr)){try{f()}catch(e){errs[nm+' <- '+k+': '+String(e&&e.message||e).slice(0,100)]=1}}}
 return {n,errs,same}}"""

with sync_playwright() as p:
    b, ctx, pg, logs = open_page(p, ROOT + '/out5.html')
    pg.wait_for_timeout(1500)
    pg.set_default_timeout(300000)
    r = pg.evaluate(JS)
    b.close()
print('состояний', r['n'], '| нормальное состояние читается без потерь:', r['same'], '| ошибок', len(r['errs']))
for k in r['errs']:
    print(' ', k)
sys.exit(0 if r['same'] and not r['errs'] and not logs else 1)
