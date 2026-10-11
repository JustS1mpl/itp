import json,os
from playwright.sync_api import sync_playwright
from h import open_page
W=os.getcwd()
ch=json.load(open('checks.json',encoding='utf-8'))
JS='''async (ch)=>{await skReady();
 const bad=[];
 for(const e of ch.EX){const r=await exec(e.code,{lines:e.lines,files:e.files||{}});
   if(r.err||norm(r.out,true)!==norm(e.out,true))bad.push(['EX',e.code,e.out,r.out,r.err]);}
 for(const e of ch.FL){const r=await exec(e.code,{lines:e.lines,files:e.files||{}});
   if(r.err||norm(r.out,true)!==norm(e.right,true))bad.push(['FL',e.code,e.right,r.out,r.err]);}
 for(const t of ch.TK){for(const [i,o] of t.tests){const r=await exec(t.tail?t.sol+'\\n'+t.tail:t.sol,{lines:i===''?[]:i.split('\\n'),files:t.files||{}});
   if(r.err||norm(r.out,true)!==norm(o,true))bad.push(['TK',t.where,i,o,r.out,r.err]);}}
 return bad}'''
with sync_playwright() as p:
    b,c,pg,logs=open_page(p,W+'/out5.html')
    bad=pg.evaluate(JS,ch)
    print(len(ch['EX']),len(ch['FL']),len(ch['TK']),'bad',len(bad))
    for x in bad: print(x)
    print(logs[:5])
    b.close()
