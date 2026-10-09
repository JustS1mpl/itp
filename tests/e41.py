import subprocess,sys,json,time
from playwright.sync_api import sync_playwright
import h,t5
progs=[
("a=input('a: ')\nb=input('b: ')\nprint(a+b)",['x','y']),
("import random\nprint(random.randint(1,10**9))\nn=int(input('n '))\nprint(random.randint(1,10**9))\nprint(random.random())\ns=input()\nprint(s*n)",['3','ab']),
("total=0\nwhile True:\n    s=input('> ')\n    if s=='q':break\n    total+=int(s)\n    print('sum',total)\nprint('bye',total)",['1','2','3','q']),
("name=input('Имя: ')\nprint('Привет, '+name+'!')\nfor i in range(3):\n    print(i,end=' ')\nprint()\nx=input('Ещё: ')\nprint(x[::-1])",['Аня','слово']),
("s={'b','a','c'}\nprint(s)\nd=input()\nprint(s,d)\nprint(hash('x')%7)\nz=input()\nprint({'q','w','e'},z)",['1','2']),
("import time\nt=time.time()\nx=input()\nprint(round(time.time()-t)<5)",['5']),
("l=[int(input()) for _ in range(3)]\nprint(l,sum(l))",['1','2','3']),
("print('no input here')",[]),
]
def host(code,lines):
    pre="import sys,builtins\n_L=iter(%r)\ndef _inp(p=''):\n    v=next(_L)\n    sys.stdout.write(str(p)+v+'\\n')\n    return v\nbuiltins.input=_inp\n"%(lines,)
    r=subprocess.run([sys.executable,'-c',pre+code],capture_output=True,text=True,env={'PYTHONHASHSEED':'0'})
    return r.stdout
with sync_playwright() as p:
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,420,860,touch=False)
    pg.evaluate("skReady()")
    bad=0
    for code,lines in progs:
        t=time.time()
        r=pg.evaluate("""async([c,L])=>{let k=0;const r=await exec(c,{live:()=>{},ask:()=>Promise.resolve(L[k++])});return [r.raw,r.err]}""",[code,lines])
        hs=host(code,lines)
        same=r[0]==hs
        # для случайных/временных/хеш-тестов сравниваем только форму
        print('OK ' if same else 'DIFF',round(time.time()-t,1),code.split('\n')[0][:40],'' if same else (repr(r[0])[:160],repr(hs)[:160],r[1]))
    print(logs[:3]);b.close()
