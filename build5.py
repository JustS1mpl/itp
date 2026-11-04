import re, sys, json, os
sys.path.insert(0, '.')
VER = '7.1.1'
s = open('base43.html', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, ('якорь найден %d раз(а), нужно %d' % (c, n), a[:100])
    s = s.replace(a, b)


rep("if(/bad input|SyntaxError/.test(err)&&/:=/.test(OC))err+='. Оператор := в ИТП работает только в условии цикла while'",'')
rep("navigator.share(d).catch(function(){});return false","navigator.share(d).then(function(){ach('share')}).catch(function(){});return false")
rep("execLimit:src.ask?5000:3000","execLimit:src.ask?null:10000,yieldLimit:src.ask?60:null")
rep("if(out.length+x.length>4000){out+=x.slice(0,4000-out.length);cut=true}else out+=x;if(src.live)src.live(out)}","if(out.length+x.length>LIM){out+=x.slice(0,LIM-out.length);cut=true}else out+=x;if(src.live)lv()}")
rep("var out='',n=0,marks=[],my=++TK,cut=false,ov=false,LS=0,LL=0;","var LIM=src.ask?300000:100000,LT0=0,PD=0,out='',n=0,marks=[],my=++TK,cut=false,ov=false,LS=0,LL=0;function lv(){var t=Date.now();if(t-LT0>90){LT0=t;PD=0;src.live(out)}else PD=1}")
rep("over:ov,used:n","over:ov,stopped:STOPT===my,used:n")
rep("return src.ask(p).then(function(v){Sk.execStart=new Date();","return src.ask(p).then(function(v){if(STOPT===my)throw new Error('ITPSTOP');Sk.execStart=new Date();")
rep("function exec(code,src){","var STOPT=-1;function exec(code,src){")
rep("(cut?'\\n…вывод обрезан':'')","(cut?'\\n…вывод обрезан: показаны первые '+LIM+' символов (программа при этом выполнялась до конца)':'')")

rep("function fixErr(e,code){if(!e)return e;","function fixErr(e,code){if(!e)return e;try{e=itpTrFull(e)}catch(_x){}")
rep("function fin2(err){","function fin2(err){if(err&&/^SystemExit\\b/.test(err))err=null;")
rep("function isOpen(i,j){var k=i+'-'+j;", "function isOpen(i,j){if(typeof DEV==='function'&&DEV())return 1;var k=i+'-'+j;if(TOPICS[i].opt)return S.d[k]||ocur(i)===k?1:0;if(j===0&&IT(i,0).t==='theory')return 1;")
rep("function nxI(i,j){if(!(i<S.start)||TOPICS[i].intro)return false;", "function nxI(i,j){if(!(i<S.start||i<FRN()[0])||TOPICS[i].intro)return false;")
# пропущенные и оставшиеся позади островки: теория открыта всегда, остальное — когда прочитана ближайшая теория перед ним
# (раньше требовалась вся теория темы до островка, и ученик не понимал, почему следующий островок закрыт)
rep("if(i<S.start){if(IT(i,j).t==='theory')return 1;for(var x=0;x<j;x++)if(IT(i,x).t==='theory'&&!S.d[i+'-'+x])return 0;return 1}", "if(i<S.start||bfr(i,j)){if(IT(i,j).t==='theory')return 1;var x=thPrev(i,j);return x<0||S.d[i+'-'+x]?1:0}")
rep("(S.d[i+'-'+j]||(i<S.start&&!t.intro))", "(S.d[i+'-'+j]||(i<S.start&&!t.intro&&!t.opt))")
rep("esc(q.e||'')", "esc(q.e||'')+xm(q)", 3)
rep("(String(it.html).match(/\\[\\[([^\\]|]+)/g)||[])", "(String(it.html).replace(/<pre>[\\s\\S]*?<\\/pre>/g,'').match(/\\[\\[([^\\]|]+)/g)||[])")
rep("it.html.split(/(<pre>[\\s\\S]*?<\\/pre>)/).map(function(p){return /^<pre>/.test(p)?", "it.html.split(/(<pre[^>]*>[\\s\\S]*?<\\/pre>)/).map(function(p){return /^<pre /.test(p)?p:/^<pre>/.test(p)?")
rep("replace(/<pre>[\\s\\S]*?<\\/pre>/g,'').match", "replace(/<pre[^>]*>[\\s\\S]*?<\\/pre>/g,'').match")
# --- звук касаний теперь делает v5/a_sound.js (после обработчиков события, чтобы не дублировать другие звуки)
rep("document.addEventListener('click',function(e){if(e.target.closest('button'))snd([600])});", "")
# --- Python не поднимать всем через 2,5 с после загрузки (это шло во время вступления и тормозило слабые телефоны):
#     на нормальных устройствах — в простое после вступления, на слабых — когда открыт урок (pyWarm, v5/a_py.js)
rep("window.addEventListener('load',function(){setTimeout(skReady,2500);", "window.addEventListener('load',function(){if(!WEAK())setTimeout(function(){if(window.pyWarm)pyWarm()},6000);")
# --- версия
s = s.replace('4.3.0', VER)

# --- шрифт Nunito встроен
rep("var l=document.createElement('link');l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family=Nunito:wght@500;700;800&display=swap';document.head.appendChild(l)", "")
# --- замена CSS целиком: v6 — одна дизайн-система для обеих тем (v5.css, v5b.css, v5c.css больше не нужны)
css = open('v5/v6.css', encoding='utf-8').read()
import base64 as _pb
_pi = lambda f: 'url(data:image/png;base64,' + _pb.b64encode(open('assets/mascot/' + f, 'rb').read()).decode() + ')'
css = ':root{--pi-o:' + _pi('profile_icon.png') + ';--pi-f:' + _pi('profile_fill.png') + '}\n' + css
rep("""'<div class="q">'+esc(q.q)+'</div>'+(q.c?'<pre>'+hl(q.c)+'</pre>':'');
    ord.forEach(function(k){h+='<button class="opt" data-k="'+k+'">'+esc(q.o[k])+'</button>'});
    show(h+'<div id="fb"></div><button class="btn" id="go" disabled>Проверить</button>');""",
"""'<div class="q">'+esc(q.q)+'</div>'+(q.v||'')+(q.c?'<pre>'+hl(q.c)+'</pre>':'');
    ord.forEach(function(k){h+='<button class="opt" data-k="'+k+'">'+esc(q.o[k])+'</button>'});
    show(h+'<div id="fb"></div><button class="btn" id="go" disabled>Проверить</button>');if(q.v)imgZoom(app);""")
# тройные кавычки: строка на несколько строк кода целиком зелёная (раньше подсвечивалась только первая пара кавычек)
rep('function hl(c){var re=/(#[^\\n]*)|(', 'function hl(c){var re=/(#[^\\n]*)|("{3}[\\s\\S]*?(?:"{3}|$)|\'{3}[\\s\\S]*?(?:\'{3}|$)|')
# Nunito — шесть готовых начертаний (400–900, woff2, assets/nunito_static.json из переменного nunito.b64 через fontTools),
# а не один переменный шрифт: на телефонах Chrome во время анимаций (прозрачность, сдвиг) временами рисовал текст
# переменного шрифта запасным (владелец, dev.35). block вместо swap и загрузка всех начертаний сразу — чтобы начертание,
# впервые нужное посреди анимации, не мелькнуло запасным шрифтом
import json as _js
_NF = _js.load(open('assets/nunito_static.json'))
css = ''.join("@font-face{font-family:'Nunito';font-style:normal;font-weight:%s;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}\n" % (w, _NF[w]) for w in sorted(_NF)) + css
a = s.index('<style>'); b = s.index('</style>')
s = s[:a] + '<style>\n' + css + '\n' + s[b:]
# приложение для телефона рисуется под системными полосами (ItpSysPlugin): их размер приходит в --sa-top/--sa-bottom/…,
# а в браузере этих переменных нет и работает обычный env(safe-area-inset-*)
s = re.sub(r"env\(safe-area-inset-(top|bottom|left|right)((?:,[^()]*)?)\)", r"var(--sa-\1,env(safe-area-inset-\1\2))", s)
s = s.replace('</style>', "</style><script>try{['400','500','600','700','800','900'].forEach(function(w){document.fonts.load(w+' 16px Nunito')})}catch(e){}</script>", 1)

# --- пакет смайликов
pack = open('assets/emoji_pack.b64').read()
# U2-6: убрать мелкие подкрашивающие слои по краям (пятна у звезды и др.), см. emofix.py
import gzip as _egz, base64 as _eb
sys.path.insert(0, 'base')   # старая база сборки: emofix, msgs, патчи — в папке base/
from emofix import emo_clean
_ep, _es = emo_clean(json.loads(_egz.decompress(_eb.b64decode(pack))))
pack = _eb.b64encode(_egz.compress(json.dumps(_ep, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), 9, mtime=0)).decode()
print('смайлики: убрано слоёв', _es[0], 'у', _es[1])
rep('<script type="text/plain" id="sk-lib">', '<script type="text/plain" id="emo-pack">' + pack + '</script>\n<script type="text/plain" id="sk-lib">')

# --- reduced-motion -> RM()
mm = "matchMedia('(prefers-reduced-motion:reduce)').matches"
a = s.index('<script>\nvar ') if '<script>\nvar ' in s else s.index('<script>', s.index('</script>') )
n = s.count(mm); s = s.replace(mm, 'RM()'); print('RM заменено', n)

rep(open('base/pyold.txt',encoding='utf8').read(), open('base/pynew.txt',encoding='utf8').read())
# --- навигация
rep("[['home','🏠','Главная'],['oge','📚','ОГЭ/ЕГЭ'],['ed','⌨️','Компилятор'],['prof','🐇','Профиль']]",
    "[['home','🗺️','Путь'],['pr','🎯','Практика'],['ed','💻','Код'],['prof','🐰','Профиль']]")
rep("({home:home,oge:oge,ed:editor,prof:profile})[b.dataset.t]()", "({home:home,pr:practice,ed:editor,prof:profile})[b.dataset.t]()")
rep("'Главная, ОГЭ/ЕГЭ, Компилятор, Профиль'", "'Путь, Практика, Код, Профиль'")

# --- clean
rep('function clean(r){if(!r||typeof r', 'function clean0(r){if(!r||typeof r')

# --- show: убрать оглавление
rep('function show(h,tab){cancelAnimationFrame(TYR);HRE=null;', 'function show(h,tab){cancelAnimationFrame(TYR);HRE=null;tocKill();')

# --- теория
rep("if(!S.d[i+'-'+j])bump(i+'-'+j);if(TOPICS[i].intro&&!w", "if(!S.d[i+'-'+j]){snd('theory');bump(i+'-'+j)}if(TOPICS[i].intro&&!w")
rep("if(fresh&&!rm)typeIn($('tb'),$('tm'));", "tocBuild();if(fresh&&!rm&&ST('ty'))typeIn($('tb'),$('tm'));")
rep("(fresh&&!rm?TMSK:TMT)", "(fresh&&!rm&&ST('ty')?TMSK:TMT)")
rep("function typeIn(box,tm){", "function typeIn(box,tm){box.classList.add('noemo');")
rep("if(tm)tm.textContent=TMT;box.removeEventListener('click',fin)", "if(tm)tm.textContent=TMT;box.removeEventListener('click',fin);box.classList.remove('noemo');emoScan(box)")

# --- подсказки
rep("var use=function(){S.hc=1;HINT=1;drc(i,j,k);save();showHint()};", "var use=function(){S.hc=1;S.hu[i]=1;HINT=1;drc(i,j,k);save();showHint()};")

# --- звуки/победы
rep("fx(true);\n    if(!S.tk[tk]){S.tk[tk]=1;save()}", "fx(true,'test');\n    if(!S.tk[tk]){S.tk[tk]=1;save()}")
rep("fx(true);projEnd(i,j);", "fx(true,'none');projEnd(i,j);")
rep("S.at[key]='full';lv=addXp(x)}\n  bump(key);", "S.at[key]='full';lv=addXp(x)}\n  bump(key);ach('proj');snd('fanfare');")
rep("var tj=!tj0&&tdone(i);home();\n  toast(tj?", "var tj=!tj0&&tdone(i);if(tj)topicDone(i);home();\n  toast(tj?")

# --- индикатор ввода
rep("ir.classList.add('on');ii.value='';st('⌨️ Программа ждёт ввод: напиши ответ в поле ниже и нажми «Ввод»');ii.focus();",
    "ir.classList.add('on');ir.classList.remove('typing');ii.value='';st('⌨️ Программа ждёт ввод: напиши ответ в поле ниже и нажми «Ввод»','wait');snd('tick');ii.oninput=function(){ir.classList.add('typing');var r=$('rst');if(r)r.classList.remove('wait')};ii.focus();")

# --- пульс кнопки «Проверить»
rep("  skReady();\n  $('run').onclick=function(){var o=$('o');if(!SKOK){o.style.display='block';o.textContent='Загружаю среду Python…'}needSk()", "  skReady();chkPulse();\n  $('run').onclick=function(){var o=$('o');if(!SKOK){o.style.display='block';o.textContent='Загружаю среду Python…'}needSk()", 2)

# --- экраны завершения: полоса опыта и пульс
rep("""'<button class="btn" id="go">Дальше</button>'+(nx?""", """xpStrip()+'<button class="btn pulse" id="go">Дальше</button>'+(nx?""")
rep("""<button class="btn" id="go">К темам</button></div>');\n  HINT=0;""", """'+xpStrip()+'<button class="btn pulse" id="go">К темам</button></div>');\n  HINT=0;""")
rep("""<button class="btn" id="go">К темам</button>'+(it.sol?""", """'+xpStrip()+'<button class="btn pulse" id="go">К темам</button>'+(it.sol?""")

# --- компилятор
rep("show(head()+'<h2>Компилятор кода</h2><button class=\"fname\"", "show(head('Код')+'<button class=\"fname\"")
rep('<div class="seg2 sm"><button id="fs" class="pri">', '<div class="edtools"><button id="fs" class="pri">')
rep("pr={'(':')','[':']','{':'}','\"':'\"'},AP=String.fromCharCode(39);pr[AP]=AP;", "pr={'(':')','[':']','{':'}','\"':'\"'},AP=String.fromCharCode(39);pr[AP]=AP;if(!ST('ac'))pr={};")
rep("if(p===q&&v[p]===d&&(d===')'", "if(ST('ac')&&p===q&&v[p]===d&&(d===')'")

# --- календарь и заморозки
rep("""g+='<i class="l'+l+'" data-d="'+k+'" title="'+calText(k)+'"></i>';""", """g+='<i class="l'+l+(!l&&S.fz.u.indexOf(k)>=0?' fz':'')+'" data-d="'+k+'" title="'+calText(k)+'"></i>';""")
rep("return t+': '+(n?n+' '+pl(n,['островок','островка','островков']):'без занятий');", "return t+': '+(n?n+' '+pl(n,['островок','островка','островков']):(S.fz.u.indexOf(k)>=0?'заморозка сохранила серию':'без занятий'));")
rep('больше</span></div>\';', 'больше</span>\'+(S.fz.u.length?\'<span class="cleg"><i class="l0 fz"></i> заморозка</span>\':\'\')+\'</div>\';')

# --- резервная копия без блока «Обращение»
a = s.index('<h2 style="font-size:20px">Настройки</h2><h3>Обращение</h3>')
b = s.index('<h3>Резервная копия</h3>', a)
s = s[:a] + '<h2 style="font-size:20px">Резервная копия</h2>' + s[b+len('<h3>Резервная копия</h3>'):]

rep("show('<div class=\"center\"><h2>Добро пожаловать в ИТП</h2>", "show('<div class=\"center\" style=\"padding-top:14px\">'+rabbit('eat')+'<h2>Добро пожаловать в ИТП</h2>")
# --- конфетти по настройке
rep("function confetti(big){", "function confetti(big){if(!ST('gc')){snd('fanfare');return}")


# --- v5.1: копирование кода, проекты-достижения, введение из настроек, поделиться
rep("'<pre>'+hl(p.slice(5,-6))+'</pre>'", "'<div class=\"cpw\"><button type=\"button\" class=\"cp\" aria-label=\"Копировать код\"></button><pre>'+hl(p.slice(5,-6))+'</pre></div>'")
rep("if(TOPICS[i].intro&&S.start>0){goBack();toast('Готово. Эта кнопка больше не нужна и пропала из профиля');return}", "if(TOPICS[i].intro&&(S.start>0||w)){goBack();if(!w)toast('Готово. Эта кнопка больше не нужна и пропала из профиля');return}")
rep("saveFile('itp-progress.png',BLOB);toast('Картинка сохранена');return false", "saveFile('itp-progress.png',BLOB);ach('share');toast('Картинка сохранена');return false")



import json as _j2
# --- v5.5.0: картинки к новым темам (assets/img/*.webp) и скрытый «хвост» у задач на функции
import base64 as _b64, glob as _glob, os as _os
_im = {}
for _f in sorted(_glob.glob('assets/img/*.webp')):
    _im['p-' + _os.path.basename(_f)[:-5]] = 'data:image/webp;base64,' + _b64.b64encode(open(_f, 'rb').read()).decode()
EXIMG = _j2.dumps(_im, ensure_ascii=False)
rep("var r=await exec(code,{lines:q.tests[n][0]===''?[]:q.tests[n][0].split('\\n')});", "var r=await exec(q.tail?code+'\\n'+q.tail:code,{lines:q.tests[n][0]===''?[]:q.tests[n][0].split('\\n')});")
rep("(!r.err&&r.used<r.total?", "(!q.tail&&!r.err&&r.used<r.total?")
rep("var hint=r.over?", "var hint=(r.over&&!q.tail)?")
rep("(S.tk[tk]?'':'# Пиши код здесь\\n')", "(S.tk[tk]?'':'# Пиши код здесь\\n'+(q.starter||''))")
rep("[0]||'# Пиши код здесь\\n',hs=String(it.h", "[0]||'# Пиши код здесь\\n'+(it.starter||''),hs=String(it.h")
# --- движок: ввод, файлы, модули
import json as _json
_py = {}
for _k, _f in (('json','json'),('csv','csv'),('pprint','pprint'),('_strptime','strptime'),('timeit','timeit'),('itpshim','main'),('io','io'),('functools','functools'),('heapq','heapq'),('statistics','statistics')):
    _py[_k] = open('v5/shim_%s.py' % _f, encoding='utf-8').read()
rep("output:function(x){if(my!==TK||cut)return;", "output:function(x){if(x==='\\x05'){SENT=1;return}if(my!==TK||cut)return;")
rep("if(my!==TK)return new Promise(function(){});\n        if(src.ask){", "if(my!==TK)return new Promise(function(){});\n        if(SENT){SENT=0;if(src.ask)return src.ask('').then(function(v){Sk.execStart=new Date();out+=v+'\\n';if(src.live)src.live(out);return v===''?'\\x05EOF':v});LL=0;if(n>=src.lines.length)return '\\x05EOF';return src.lines[n++]}\n        if(src.ask){")
rep("var OC=code,WL=wal(code);code=WL.code;", "var OC=code,WL=wal(code),PL=0,SENT=0;code=WL.code;if(ITPNEED.test(OC)){code='from itpshim import *\\n'+(/\\bstrict\\b/.test(OC)?'zip = zip_\\n':'')+code;PL=/\\bstrict\\b/.test(OC)?2:1}try{Sk.sysmodules.mp$del_subscript(new Sk.builtin.str('itpshim'));Sk.sysmodules.mp$del_subscript(new Sk.builtin.str('timeit'))}catch(e){}")
rep("Sk.misceval.asyncToPromise(function(){return Sk.importMainWithBody('<stdin>',false,code,true)})", "Sk.builtins.__itp_files__=Sk.ffi.remapToPy(src.files||FCUR||{});Sk.builtins.__itp_stdin__=/\\bstdin\\b/.test(OC)?Sk.builtin.bool.true$:Sk.builtin.bool.false$;Sk.misceval.asyncToPromise(function(){return Sk.importMainWithBody('<stdin>',false,code,true)},{'Sk.yield':function(sp){if(PD){PD=0;if(src.live)src.live(out)}if(STOPT===my||(src.alive&&!src.alive()))return Promise.reject(new Error('ITPSTOP'));return new Promise(function(r,j){setTimeout(function(){try{r(sp.resume())}catch(x){j(x)}},0)})}})")
rep("if(WL.map)err=err.replace(/(line |строке )(\\d+)/g,function(m0,a,b){return a+(WL.map[+b-1]||b)});", "if(WL.map||PL)err=err.replace(/(line |строке )(\\d+)/g,function(m0,a,b){return a+((WL.map?WL.map[+b-1-PL]:+b-PL)||b)});")


# --- форматирование с разделителем _ (как в Python: f"{n:_}")
rep("(0)?(\\d+)?(,)?(?:\\.(\\d+))?", "(0)?(\\d+)?([,_])?(?:\\.(\\d+))?")
rep('d[0]=d[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,",")', 'd[0]=d[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,a[7])')
rep('g[0]=g[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,",")', 'g[0]=g[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,h[7])')


exec(open('base/msgs.py',encoding='utf-8').read())
# --- вставка ядра и интерфейса
core = open('v5/a_core.js', encoding='utf-8').read() + '\n' + open('v5/a_sound.js', encoding='utf-8').read() + '\n' + open('v5/a_ui.js', encoding='utf-8').read()
for extra in ('v5/a_fix.js','v5/a_fix2.js','v5/a_fix3.js','v5/a_fix4.js','v5/a_more.js','v5/a_dev.js','v5/a_img.js','v5/a_mood.js','v5/a_notify.js','v5/a_web.js','v5/a_out.js','v5/a_py.js','v5/a_turtle.js','v5/a_ux.js','v5/a_screens.js','v5/a_boot.js','v5/a_upd.js','v5/a_launch.js'):
    try: core += '\n' + open(extra, encoding='utf-8').read()
    except FileNotFoundError: pass
anchor = "seedLit();window.addEventListener('resize',function(){if(app.querySelector('.path'))links()});\napplyTheme();"
# --- настроения кролика: ликующий прыжок (состояние happy: итоги, курс пройден, карточка «Поделиться»; cheer.webp — новый рисунок 2026-11-02), плачущий cry/cryhead (U2-5) и хмурый: grump — целиком, grumphead — голова (реакция на первую ошибку); по аналогии с wow и wowhead
import base64 as _mb
_mood = ''.join("IMG.%s='data:image/webp;base64,%s';\n" % (k, _mb.b64encode(open('assets/mascot/%s.webp' % f, 'rb').read()).decode()) for k, f in (('eat', 'lovecarrot'), ('happy', 'cheer'), ('grumphead', 'grump_head'), ('grump', 'grump'), ('rolled', 'rolled'), ('wow', 'wow'), ('cool', 'cool'), ('wowhead', 'wow_head'), ('cry', 'cry'), ('cryhead', 'cry_head'), ('sleep', 'sleep'), ('angry', 'angry'), ('back', 'back'), ('wink', 'wink'), ('angryhead', 'angry_head'), ('logo', 'logo'), ('wordmark', 'wordmark')) if os.path.exists('assets/mascot/%s.webp' % f))
# --- тени под лапами кролика — готовыми, посчитанными при сборке (раньше браузер на каждом запуске раскодировал 6 картинок
#     и перебирал их пиксели, feetOf в a_ui.js). Тот же расчёт: нижний непрозрачный ряд и ширина лап в полосе 6 % над ним
from PIL import Image as _FI
def _feet(f):
    im = _FI.open('assets/mascot/%s.webp' % f).convert('RGBA')
    W = min(240, im.width); H = round(W * im.height / im.width)
    a = im.resize((W, H), _FI.BILINEAR).getchannel('A').load()
    yb = next((y for y in range(H - 1, -1, -1) if any(a[x, y] > 140 for x in range(W))), -1)
    if yb < 0:
        return None
    band = max(2, round(H * .06)); xs = [x for y in range(yb, max(-1, yb - band), -1) for x in range(W) if a[x, y] > 140]
    return min(xs) / W, (max(xs) + 1) / W, (yb + 1) / H
_fc = ''
for _st, _f in (('eat', 'lovecarrot'), ('happy', 'cheer'), ('grump', 'grump'), ('rolled', 'grump'), ('wow', 'wow'), ('cool', 'cool'), ('sleep', 'sleep'), ('angry', 'angry'), ('back', 'back'), ('wink', 'wink'), ('cry', 'cry')):
    if not os.path.exists('assets/mascot/%s.webp' % _f):
        continue
    _r = _feet(_f)
    if not _r:
        continue
    _l, _rr, _y = _r; _pad = (_rr - _l) * .12
    _fc += ':root:not([data-theme=dark]) .rw.im.%s::after{left:%.1f%%;right:%.1f%%;bottom:%.1f%%}\n' % (_st, max(0, _l - _pad) * 100, max(0, 1 - _rr - _pad) * 100, (1 - _y) * 100 - 4)
_si = s.index('</style>'); s = s[:_si] + '\n/* тени под лапами кролика — посчитаны при сборке (build5.py) */\n' + _fc + s[_si:]
print('тени под лапами: готовые,', _fc.count('\n'), 'спрайтов')
core = 'var EXIMG=' + EXIMG + ';\n' + _mood + core
core = core.replace('/*ITPY*/{}', _json.dumps(_py, ensure_ascii=False))
rep(anchor, core + "\nseedLit();window.addEventListener('resize',function(){if(app.querySelector('.path'))links()});\napplyTheme();if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',emoLoad);else emoLoad();")
# --- достижения за проекты (по названию острова project). Правило действует и в старом projEnd базы,
#     и в новом projEnd из v5/a_screens.js, поэтому якорь встречается 2 раза.
# достижения за проекты 7.0 (DECISIONES §48): одиночные по началу названия, многоэтапные — когда пройдены все этапы
rep("bump(key);ach('proj');snd('fanfare');", "bump(key);ach('proj');if(!at||at==='skip'){S.cn.pj=Math.min(99999,S.cn.pj+1);save();if(S.cn.pj>=3)ach('pj3')}var pn_=it.n||'';[['Квитанция','preceipt'],['Угадай число','pguess'],['Частотный словарь','pfreq'],['Шифр Цезаря','pcaesar'],['Дневник расходов','pdiary']].forEach(function(r){if(pn_.indexOf(r[0])===0)ach(r[1])});[['Мессенджер, этап','pmsg'],['RPG, этап','prpg']].forEach(function(r){if(pn_.indexOf(r[0])!==0)return;var ok_=true;TOPICS[i].items.forEach(function(x,k){if(x.t==='project'&&(x.n||'').indexOf(r[0])===0&&!S.d[i+'-'+k])ok_=false});if(ok_)ach(r[1])});snd('fanfare');", 2)

s=s.replace('.slice(0,16).join(','.slice(0,20).join(').replace('maxlength="16"','maxlength="20"')
assert '4.3.0' not in s
import base64 as _b64, gzip as _gz
def _b(path, gz=False):
    d = open(path, 'rb').read()
    if gz: d = _gz.compress(d, 9)
    return _b64.b64encode(d).decode()
_P = 'pyo/pyodide/'
_blocks = ''.join('<script type="text/plain" id="%s">%s</script>\n' % (i, t) for i, t in (
    ('py-wasm', _b(_P + 'pyodide.asm.wasm', 1)), ('py-asm', _b(_P + 'pyodide.asm.js', 1)), ('py-zip', _b(_P + 'python_stdlib.zip')),
    ('py-lock', open(_P + 'pyodide-lock.json', encoding='utf-8').read().replace('</', '<\\/')),
    ('py-loader', open(_P + 'pyodide.js', encoding='utf-8').read().replace('</script', '<\\/script')),
    ('py-glue', open('v5/py/glue.py', encoding='utf-8').read() + '\n_TURTLE_SRC = ' + repr(open('v5/py/turtle_shim.py', encoding='utf-8').read()) + '\n_REQUESTS_SRC = ' + repr(open('v5/py/requests_shim.py', encoding='utf-8').read()) + '\n_MINIWEB_SRC = ' + repr(open('v5/py/miniweb_shim.py', encoding='utf-8').read()) + '\n'),('py-worker', open('v5/py/worker.js', encoding='utf-8').read())))
assert s.count('</body>') == 1
s = s.replace('</body>', _blocks + '</body>')
s = s.replace('v5.1.3', VER).replace('__VER__', VER)
# --- полное название приложения: «И так, программирование» (сокращение ИТП прежнее)
assert 'Пайтон' not in s
rep('<title>ИТП v' + VER + '</title>', '<title>ИТП — И так, программирование</title>\n<meta name="description" content="ИТП («И так, программирование»): учебное приложение по Python для старшеклассников.">\n<meta name="color-scheme" content="light dark">'
    # iPhone/iPad (a_web.js): с экрана «Домой» — на весь экран, со своим значком и названием
    '\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">'
    '\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<meta name="apple-mobile-web-app-title" content="ИТП">'
    '\n<link rel="apple-touch-icon" href="apple-touch-icon.png">')
# пробные сборки 7.0 хранят сохранения под своим ключом: не портят настоящий прогресс 6.x и не берут его себе
if '-dev' in VER:
    rep("var KEY='pyshag2',", "var KEY='pyshag7dev',")
# U2-3: у каждого языка программирования свой ключ прогресса (saveKey в v5/a_core.js; у Python ключ прежний)
s = re.sub(r"var KEY='(pyshag[^']*)',", r"var KEY=saveKey('\1'),", s)
assert "var KEY=saveKey(" in s
open('out5.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
