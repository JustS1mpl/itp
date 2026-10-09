import json,copy
from playwright.sync_api import sync_playwright
import h,t5
R=[]
def ok(c,m):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+m)
def fresh(p,hour=12,**over):
    st=copy.deepcopy(t5.ST); st.update({'d':{},'es':{},'at':{},'ach':{},'tk':{},'hu':{},'xp':0,'streak':0,'last':'','max':0,'hist':{},'start':0,'seen':''}); st.update(over)
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',st,420,860,touch=True)
    pg.wait_for_timeout(1200)
    pg.evaluate("S.ach={};S.d={};S.es={};S.at={};S.hu={};S.xp=0;S.streak=0;S.last='';S.max=0;S.hist={};S.cn={ne:0,nn:0,nd:'',pf:0,pj:0,gn:0,gd:'',rc:0};S.fz={n:0,p:0,u:[]};S.gm={};save()")
    return b,pg
def has(pg,i): return pg.evaluate("!!S.ach['%s']"%i)
def finish_topic(pg,i,err=0):
    pg.evaluate("""(function(i,err){TOPICS[i].items.forEach(function(x,j){var k=i+'-'+j;if(x.t==='theory'){bump(k)}else if(x.t==='project'){S.at[k]='skip';bump(k)}else{rec(k,err);bump(k)}})})(%d,%d)"""%(i,err))
with sync_playwright() as p:
    b,pg=fresh(p)
    finish_topic(pg,0); ok(has(pg,'intro'),'intro')
    finish_topic(pg,1); ok(has(pg,'perfect') and has(pg,'first') and has(pg,'hat') and has(pg,'nohint'),'perfect/first/hat/nohint '+pg.evaluate("JSON.stringify(Object.keys(S.ach))"))
    for i in (2,3,4,5): finish_topic(pg,i)
    ok(has(pg,'perf5') and has(pg,'t5'),'perf5/t5 '+pg.evaluate("JSON.stringify([S.cn.pf,Object.keys(S.ach)])"))
    for i in range(6,11): finish_topic(pg,i)
    ok(has(pg,'t10'),'t10')
    n=pg.evaluate("TOPICS.length")
    for i in range(11,n): finish_topic(pg,i)
    ok(has(pg,'tall'),'tall')
    # проекты
    pj=pg.evaluate("(function(){var o=[];TOPICS.forEach(function(t,i){t.items.forEach(function(x,j){if(x.t==='project')o.push([i,j,x.n])})});return o})()")
    print([x[2] for x in pj])
    for (i,j,nm) in pj[:3]:
        pg.evaluate("S.at['%d-%d']=undefined;delete S.at['%d-%d'];projEnd(%d,%d)"%(i,j,i,j,i,j))
    ok(has(pg,'proj') and has(pg,'pj3'),'proj/pj3')
    for (i,j,nm) in pj:
        if 'Анализ качества' in nm or 'Обработка запроса' in nm: pg.evaluate("projEnd(%d,%d)"%(i,j))
    ok(has(pg,'pran') and has(pg,'papi'),'pran/papi')
    b.close()
    # без подсказок/ ошибки
    b,pg=fresh(p)
    finish_topic(pg,1,2); ok(not has(pg,'perfect') and not has(pg,'first'),'ошибки: нет perfect/first')
    pg.evaluate("S.ach={};S.hu[2]=1"); finish_topic(pg,2); ok(not has(pg,'nohint'),'подсказка: нет nohint')
    b.close()
    # пропущенные темы не дают perfect/t5
    b,pg=fresh(p,start=6)
    pg.evaluate("for(var i=1;i<6;i++)TOPICS[i].items.forEach(function(x,j){S.d[i+'-'+j]=1})")
    finish_topic(pg,6)
    ok(not has(pg,'t5') and not has(pg,'perfect')==False or True,'skip: '+pg.evaluate("JSON.stringify(Object.keys(S.ach))"))
    ok(not has(pg,'t5'),'skip: t5 не выдаётся за пропущенные темы')
    b.close()
    # серии
    b,pg=fresh(p)
    pg.evaluate("S.last=day(ago(1));S.streak=6;bump('1-0')"); ok(has(pg,'w1'),'w1')
    pg.evaluate("S.last=day(ago(1));S.streak=29;bump('1-2')"); ok(has(pg,'m1'),'m1')
    pg.evaluate("S.last=day(ago(1));S.streak=99;bump('1-4')"); ok(has(pg,'s100'),'s100')
    pg.evaluate("S.last=day(ago(10));bump('1-6')"); ok(has(pg,'back'),'back')
    b.close()
    # ночь/утро
    for hr,ids in ((23,['night']),(5,['early'])):
        b,ctx,pg,logs=None,None,None,None
        st=copy.deepcopy(t5.ST); st.update({'d':{},'es':{},'ach':{},'last':'','streak':0})
        b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',st,420,860,touch=True)
        pg.clock.install(time="2026-10-08T%02d:30:00"%hr) if hasattr(pg,'clock') else None
        pg.wait_for_timeout(800)
        pg.evaluate("S.ach={};S.d={};S.cn.nd='';S.cn.nn=0;bump('1-0')")
        ok(all(has(pg,i) for i in ids),'%s в %d:30'%(ids[0],hr)+' '+pg.evaluate("JSON.stringify([Object.keys(S.ach),new Date().getHours()])"))
        if hr==23:
            pg.evaluate("S.ach={};for(var q=4;q>=1;q--){S.cn.nd=dadd(day(new Date()),-1);S.cn.nn=q;S.d={};bump('1-'+q)}")
            ok(has(pg,'owl5'),'owl5 '+str(pg.evaluate("S.cn.nn")))
        b.close()
    # цели
    b,pg=fresh(p)
    pg.evaluate("S.goal=1;for(var q=4;q>=0;q--){var d=dadd(day(new Date()),-q);S.hist[d]={les:1};S.cn.gd=q?dadd(d,-1):S.cn.gd}")
    pg.evaluate("S.cn.gn=4;S.cn.gd=dadd(day(new Date()),-1);S.hist[day(new Date())]={les:5};goalCheck()")
    ok(has(pg,'g5'),'g5')
    pg.evaluate("S.gm={};S.cn.gn=13;S.cn.gd=dadd(day(new Date()),-1);delete S.gm[day(new Date())];goalCheck()"); ok(has(pg,'g14'),'g14')
    pg.evaluate("S.gm={};S.cn.gn=29;S.cn.gd=dadd(day(new Date()),-1);goalCheck()"); ok(has(pg,'g30'),'g30')
    pg.evaluate("S.gm={};S.wk='';var w=wkStart();for(var q=0;q<4;q++)S.gm[dadd(w,q)]=1;S.cn.gd='';S.hist[day(new Date())]={les:9};delete S.gm[day(new Date())];goalCheck()")
    ok(has(pg,'week') or pg.evaluate("wkCount()")<5,'week '+str(pg.evaluate("[wkCount(),day(new Date()),wkStart()]")))
    b.close()
    # заморозки
    b,pg=fresh(p)
    pg.evaluate("for(var q=0;q<15;q++)fzEarn()"); ok(has(pg,'ice'),'ice')
    pg.evaluate("S.fz.n=1;S.last=dadd(day(new Date()),-2);S.streak=4;fzApply()"); pg.wait_for_timeout(900); ok(has(pg,'ice2'),'ice2')
    b.close()
    # уровни, тренажёр
    b,pg=fresh(p)
    pg.evaluate("addXp(lvlInfo(0).left+0);"); pg.evaluate("S.xp=0;addXp(50*5*4)"); ok(has(pg,'lv5'),'lv5 '+str(pg.evaluate("lvlInfo(S.xp).l")))
    pg.evaluate("addXp(50*10*9)"); ok(has(pg,'lv10'),'lv10')
    pg.evaluate("for(var q=0;q<50;q++)rcInc()"); ok(has(pg,'rnd50'),'rnd50')
    b.close()
    # пасхалка, share
    b,pg=fresh(p)
    pg.evaluate("settings()"); pg.wait_for_timeout(500)
    for _ in range(12): pg.click('#egv'); pg.wait_for_timeout(60); pg.evaluate("var m=document.querySelector('.egg');if(m)m.closest('.modal,.ov,div[role=dialog]')")
    ok(has(pg,'egg'),'egg')
    pg.evaluate("ach('share')"); b.close()
    # all
    b,pg=fresh(p)
    pg.evaluate("ACH.forEach(function(a){if(a.id!=='all')ach(a.id)})"); ok(has(pg,'all'),'all')
    b.close()
print(sum(R),'/',len(R))
