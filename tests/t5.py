import sys,json,datetime
from playwright.sync_api import sync_playwright
import h
def today(n=0): return (datetime.date.today()-datetime.timedelta(days=n)).isoformat()
ST={'nick':'Тест','start':0,'g':'m','xp':180,'streak':3,'last':today(),'seen':today(),'max':5,'reg':today(10),
 'd':{'0-0':1,'1-0':1,'1-1':1,'1-2':1,'1-3':1,'1-4':1},'hist':{today():{'xp':20,'les':1},today(1):{'xp':40,'les':3},today(2):{'xp':30,'les':2}},
 'at':{'1-1':'full','1-3':'full'},'es':{'1-1':0,'1-3':2},
 'set':{},'goal':2,'ach':{'first':today(1),'night':today(2),'intro':today(5)},'fz':{'n':1,'p':4,'u':[today(6)]},'gm':{today(1):1}}
import os; W=os.getcwd()+'/'
def run(shots,w=420,h_=860,dark=False,file='out5.html',script=None):
    with sync_playwright() as p:
        b,ctx,pg,logs=h.open_page(p,W+file,ST,w,h_,touch=(w<600),color_scheme='dark' if dark else 'light')
        pg.wait_for_timeout(1500)
        for name,js in shots:
            if js: pg.evaluate(js); pg.wait_for_timeout(900)
            pg.screenshot(path=W+'v5/'+name+'.png')
        if script: script(pg)
        print('\n'.join(logs[:20]))
        b.close()
if __name__=='__main__':
    run([('s_home',None),('s_prac','practice()'),('s_prof','profile()'),('s_set','settings()')])
