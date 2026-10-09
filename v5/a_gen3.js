/* ===================== v5.1.3: задание №3 ЕГЭ (базы данных, три таблицы): решатель, подсказки, генератор ===================== */
(function(){
  var CAT=[['Зефир ванильный','Мармелад и зефир','г',250,140],['Зефир шоколадный','Мармелад и зефир','г',250,160],['Зефир клубничный','Мармелад и зефир','г',300,150],['Мармелад фруктовый','Мармелад и зефир','г',200,110],['Мармелад жевательный','Мармелад и зефир','г',150,95],
    ['Печенье овсяное','Печенье','г',400,120],['Печенье сдобное','Печенье','г',350,130],['Галеты для завтрака','Печенье','г',200,85],['Крекер солёный','Печенье','г',180,75],['Конфеты шоколадные','Конфеты','г',500,420],['Конфеты карамельные','Конфеты','г',400,210],['Клюква в сахаре','Конфеты','г',150,190],['Драже фруктовое','Конфеты','г',200,130],
    ['Батончик шоколадный','Шоколад','шт',12,360],['Вафельный набор','Печенье','шт',8,175],['Шоколад молочный','Шоколад','г',100,105],['Шоколад горький','Шоколад','г',90,115]];
  var FAMS=['Зефир','Мармелад','Печенье','Конфеты','Шоколад'],GEN={'Зефир':'зефира','Мармелад':'мармелада','Печенье':'печенья','Конфеты':'конфет','Шоколад':'шоколада'};
  var DIST=['Заречный','Прибрежный','Центральный','Северный','Восточный'];
  var STR=[['пр-т','Мира','проспекте Мира'],['ул.','Лермонтова','улице Лермонтова'],['ул.','Металлургов','улице Металлургов'],['пр-т','Революции','проспекте Революции'],['ул.','Садовая','Садовой улице'],['ул.','Гагарина','улице Гагарина']];
  var MON={1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'},MNOM={6:'июнь',8:'август',9:'сентябрь',10:'октябрь'};
  var PLAYS=[['У. Шекспир','Комедия ошибок','Комедия'],['У. Шекспир','Много шума из ничего','Комедия'],['У. Шекспир','Гамлет','Трагедия'],['А. Чехов','Вишнёвый сад','Драма'],['Н. Гоголь','Ревизор','Комедия'],['А. Островский','Гроза','Драма'],['К. Гоцци','Король-олень','Сказка'],['С. Маршак','Двенадцать месяцев','Сказка']];
  var TARS=[['Взрослый','Нет',900],['Взрослый','Да',600],['Детский','Нет',500],['Детский','Да',300],['Студенческий','Да',450]];
  var SURN=[['Иванов','Иванова'],['Петров','Петрова'],['Сидоров','Сидорова'],['Кузнецов','Кузнецова'],['Смирнов','Смирнова'],['Орлов','Орлова'],['Попов','Попова'],['Волков','Волкова']];
  var IM=['А.И.','П.С.','В.Н.','Д.А.','Е.О.','К.Л.','М.Т.','Н.В.','О.Р.','С.И.'],IF=['А.И.','Е.П.','Н.С.','О.В.','Л.А.','М.Д.','Т.Н.','И.К.','В.Р.','Ю.С.'],CITY=['Омск','Тула','Псков','Курск','Тверь'];
  var PK=[2,3,4,5,6,8,10,12,15,20,24,30];
  function ri(r,a,b){return a+Math.floor(r()*(b-a+1))}
  function p2(n){return(n<10?'0':'')+n}
  function ds(y,m,d){return p2(d)+'.'+p2(m)+'.'+y}
  function iso(s){return s.slice(6)+'-'+s.slice(3,5)+'-'+s.slice(0,2)}
  function isoOf(y,m,d){return y+'-'+p2(m)+'-'+p2(d)}
  function dsi(i){return i.slice(8)+'.'+i.slice(5,7)+'.'+i.slice(0,4)}
  function addDay(i,n){var d=new Date(Date.UTC(+i.slice(0,4),+i.slice(5,7)-1,+i.slice(8)+n));return d.getUTCFullYear()+'-'+p2(d.getUTCMonth()+1)+'-'+p2(d.getUTCDate())}
  function T(db,n){for(var i=0;i<db.length;i++)if(db[i].n===n)return db[i].r;return[]}
  function kindFam(k){return/^th_/.test(k)?'theatre':(k==='one_parent'||k==='grandkids'||k==='max_kids'||k==='parents_same_city')?'family':'sweets'}
  /* ---------- конфеты ---------- */
  function shopsOf(db,loc){return T(db,'Магазин').filter(function(s){return loc.type==='district'?s[1]===loc.value:s[2].indexOf(loc.value+',')===0}).map(function(s){return s[0]})}
  function prodsOf(db,Q){return T(db,'Товар').filter(function(p){return Q.name?p[2]===Q.name:p[2].indexOf(Q.prefix)===0}).map(function(p){return p[0]})}
  function selMoves(db,Q,withOp){var sh=shopsOf(db,Q.loc),pr=prodsOf(db,Q);
    return T(db,'Движение товаров').filter(function(m){var d=iso(m[1]);return d>=Q.d1&&d<=Q.d2&&sh.indexOf(m[2])>=0&&pr.indexOf(m[3])>=0&&(!withOp||!Q.op||m[5]===Q.op)})}
  function prodMap(db){var o={};T(db,'Товар').forEach(function(p){o[p[0]]=p});return o}
  function sum(a,f){var s=0;a.forEach(function(x){s+=f(x)});return s}
  function ansSw(db,Q){var P=prodMap(db),k=Q.kind;
    if(k==='mass')return sum(selMoves(db,Q,1).filter(function(m){return P[m[3]][3]==='г'}),function(m){return m[4]*P[m[3]][4]})/1000;
    if(k==='revenue')return sum(selMoves(db,Q,1),function(m){return m[4]*P[m[3]][5]});
    if(k==='packs')return sum(selMoves(db,Q,1),function(m){return m[4]});
    if(k==='delta')return sum(selMoves(db,Q,0),function(m){return m[5]==='Поступление'?m[4]:-m[4]});
    return selMoves(db,Q,1).length}
  function cp(o,e){var n={};for(var k in o)n[k]=o[k];for(var k2 in e)n[k2]=e[k2];return n}
  function wrongSw(db,Q){var P=prodMap(db),k=Q.kind,a=ansSw(db,Q),res=[],all=cp(Q,{op:null});
    if(k==='mass'){res.push([sum(selMoves(db,all,1).filter(function(m){return P[m[3]][3]==='г'}),function(m){return m[4]*P[m[3]][4]})/1000,'не отобрали тип операции (взяли и «Поступление», и «Продажа»)']);
      res.push([sum(selMoves(db,Q,1).filter(function(m){return P[m[3]][3]==='г'}),function(m){return m[4]*P[m[3]][4]}),'не перевели граммы в килограммы (забыли разделить на 1000)']);
      res.push([sum(selMoves(db,Q,1).filter(function(m){return P[m[3]][3]==='г'}),function(m){return m[4]}),'посчитали упаковки вместо массы (забыли умножить на «Количество в упаковке»)'])}
    else if(k==='revenue'){res.push([sum(selMoves(db,all,1),function(m){return m[4]*P[m[3]][5]}),'не отобрали тип операции (в выручку попали и поступления)']);
      res.push([sum(selMoves(db,Q,1),function(m){return P[m[3]][5]}),'взяли цену один раз за операцию, не умножив на «Количество упаковок»'])}
    else if(k==='packs'||k==='count_ops'){res.push([k==='packs'?sum(selMoves(db,all,1),function(m){return m[4]}):selMoves(db,all,1).length,'не учли тип операции']);
      res.push([k==='packs'?selMoves(db,Q,1).length:sum(selMoves(db,Q,1),function(m){return m[4]}),k==='packs'?'посчитали число операций вместо упаковок':'посчитали упаковки вместо операций'])}
    else if(k==='delta'){var rows=selMoves(db,Q,0),po=sum(rows.filter(function(m){return m[5]==='Поступление'}),function(m){return m[4]}),pr=sum(rows.filter(function(m){return m[5]==='Продажа'}),function(m){return m[4]});
      res.push([po,'посчитали только поступления (забыли вычесть продажи)']);res.push([po+pr,'сложили поступления и продажи вместо вычитания']);res.push([pr-po,'перепутали порядок вычитания (получился обратный знак)'])}
    if(k!=='delta')res.push([ansSw(db,cp(Q,{d2:addDay(Q.d2,-1)})),'не включили последний день периода (поняли «по '+(+Q.d2.slice(8))+'» как «до», не включая)']);
    var out=[],seen=[a];res.forEach(function(x){if(seen.indexOf(x[0])<0&&x[0]===x[0]){seen.push(x[0]);out.push(x)}});return out}
  /* ---------- театр ---------- */
  function thRows(db,Q){var pl={},tr={};T(db,'Спектакль').forEach(function(p){pl[p[0]]=p});T(db,'Тариф').forEach(function(t){tr[t[0]]=t});
    return T(db,'Продажи').filter(function(s){var d=iso(s[1]);if(d<Q.d1||d>Q.d2)return false;var p=pl[s[2]],t=tr[s[3]];
      return(!Q.author||p[1]===Q.author)&&(!Q.genre||p[3]===Q.genre)&&(!Q.cat||t[1]===Q.cat)&&(!Q.benefit||t[2]===Q.benefit)})}
  function ansTh(db,Q){var tr={};T(db,'Тариф').forEach(function(t){tr[t[0]]=t});return sum(thRows(db,Q),function(s){return s[4]*(Q.kind==='th_revenue'?tr[s[3]][3]:1)})}
  function wrongTh(db,Q){var a=ansTh(db,Q),res=[];
    if(Q.benefit)res.push([ansTh(db,cp(Q,{benefit:null})),'не учли условие про льготу (взяли все тарифы категории)']);
    if(Q.genre)res.push([ansTh(db,cp(Q,{genre:null})),'взяли все спектакли автора, а не только нужного жанра']);
    if(Q.cat)res.push([ansTh(db,cp(Q,{cat:null})),'не отобрали категорию зрителя']);
    if(Q.kind==='th_revenue')res.push([ansTh(db,cp(Q,{kind:'th_count'})),'посчитали число билетов вместо выручки (забыли цену)']);
    res.push([thRows(db,Q).length,'посчитали число строк-продаж вместо числа билетов']);res.push([ansTh(db,cp(Q,{d2:addDay(Q.d2,-1)})),'не включили последний день периода']);
    var out=[],seen=[a];res.forEach(function(x){if(seen.indexOf(x[0])<0){seen.push(x[0]);out.push(x)}});return out}
  /* ---------- люди ---------- */
  function famMaps(db){var par={},kids={},nm={},city={};T(db,'Люди').forEach(function(p){nm[p[0]]=p[1];city[p[0]]=p[4]});T(db,'Родственные связи').forEach(function(x){(par[x[1]]=par[x[1]]||[]).push(x[0]);(kids[x[0]]=kids[x[0]]||[]).push(x[1])});return{par:par,kids:kids,nm:nm,city:city}}
  function ansFam(db,Q){var M=famMaps(db),k=Q.kind,n=0;
    if(k==='one_parent'){Object.keys(M.nm).forEach(function(p){if((M.par[p]||[]).length===1)n++});return n}
    if(k==='max_kids'){Object.keys(M.kids).forEach(function(a){n=Math.max(n,M.kids[a].length)});return n}
    if(k==='grandkids'){(M.kids[Q.pid]||[]).forEach(function(c){n+=(M.kids[c]||[]).length});return n}
    Object.keys(M.nm).forEach(function(p){var pr=M.par[p]||[];if(pr.length===2&&M.city[pr[0]]===M.city[pr[1]])n++});return n}
  /* ---------- общий вызов ---------- */
  function answer(db,Q){var f=kindFam(Q.kind);return f==='sweets'?ansSw(db,Q):f==='theatre'?ansTh(db,Q):ansFam(db,Q)}
  function fmt(x){return Math.abs(x-Math.round(x))<1e-9?String(Math.round(x)):String(x).replace('.',',')}
  /* ---------- текст ---------- */
  function distG(d){return/ый$/.test(d)?d.slice(0,-2)+'ого':d}
  function locIn(Q){return Q.loc.type==='district'?'в магазинах '+distG(Q.loc.value)+' района':'в магазинах, расположенных на '+prep(Q.loc.value)}
  function locTo(Q){return Q.loc.type==='district'?'в магазины '+distG(Q.loc.value)+' района':'в магазины, расположенные на '+prep(Q.loc.value)}
  function prep(v){for(var i=0;i<STR.length;i++)if(STR[i][0]+' '+STR[i][1]===v)return STR[i][2];return v}
  function target(Q){return Q.prefix?'всех видов '+GEN[Q.prefix]:'товара «'+Q.name+'»'}
  function period(a,b){var d1=+a.slice(8),d2=+b.slice(8),m1=+a.slice(5,7),m2=+b.slice(5,7);return m1===m2?'с '+d1+' по '+d2+' '+MON[m1]+' включительно':'с '+d1+' '+MON[m1]+' по '+d2+' '+MON[m2]+' включительно'}
  function question(Q,db){var k=Q.kind,per=Q.d1?period(Q.d1,Q.d2):'';
    if(k==='mass')return'определите общую массу (в кг) '+target(Q)+', '+(Q.op==='Поступление'?'поступивших '+locTo(Q):'проданных '+locIn(Q))+', '+per+'.';
    if(k==='revenue')return'определите общую выручку (в руб.) от продажи '+target(Q)+' '+locIn(Q)+', '+per+'.';
    if(k==='delta')return'определите, на сколько увеличилось количество упаковок '+target(Q)+', имеющихся в наличии '+locIn(Q)+', '+per+'.';
    if(k==='packs')return Q.op==='Продажа'?'определите, сколько упаковок '+target(Q)+' было продано '+locIn(Q)+', '+per+'.':'определите, сколько упаковок '+target(Q)+' поступило '+locTo(Q)+', '+per+'.';
    if(k==='count_ops')return'определите, сколько операций «'+Q.op+'» с '+target(Q)+' зафиксировано '+locIn(Q)+', '+per+'.';
    if(/^th_/.test(k)){var who=[];if(Q.author)who.push('по пьесам автора '+Q.author);if(Q.genre)who.push('жанра «'+Q.genre+'»');var cond=[];if(Q.cat)cond.push('зрителям категории «'+Q.cat+'»');if(Q.benefit)cond.push(Q.benefit==='Да'?'по льготным тарифам':'по тарифам без льготы');
      var sold=cond.length?'проданных '+cond.join(', '):'проданных';
      return k==='th_revenue'?'определите общую выручку (в руб.) от продажи билетов на спектакли '+who.join(' ')+', '+sold+', '+period(Q.d1,Q.d2)+'.':'определите общее количество билетов на спектакли '+who.join(' ')+', '+sold+', '+period(Q.d1,Q.d2)+'.'}
    if(k==='one_parent')return'определите, у скольких людей в базе указан ровно один родитель.';
    if(k==='max_kids')return'определите наибольшее количество детей у одного человека, указанное в базе.';
    if(k==='grandkids'){var nm=famMaps(db).nm[Q.pid];return'определите количество внуков человека «'+nm+'» (ID '+Q.pid+').'}
    return'определите, у скольких людей в базе указаны оба родителя и эти родители родились в одном городе.'}
  function statement(Q,db,month){var f=kindFam(Q.kind),h='Ниже приведён фрагмент ';
    if(f==='sweets')return h+'базы данных «Кондитерские изделия» о поставках конфет и печенья в магазины районов города. База состоит из трёх таблиц: «Движение товаров» (операции поступления и продажи за '+(MNOM[month]||month)+' 2026 г.; поле «Тип операции» — «Поступление» или «Продажа»), «Товар» (характеристики товаров) и «Магазин» (район и адрес магазина). Используя информацию из базы данных, '+question(Q,db)+' В ответе запишите только число.';
    if(f==='theatre')return h+'базы данных «Театр» о продаже билетов за октябрь 2026 г. База состоит из трёх таблиц: «Спектакль» (автор, название, жанр), «Тариф» (категория зрителя, льгота, цена билета) и «Продажи» (дата, спектакль, тариф, количество билетов). Используя информацию из базы данных, '+question(Q,db)+' В ответе запишите только число.';
    return h+'базы данных о людях и их родственных связях. Таблица «Люди»: ID, фамилия и инициалы, пол, год и город рождения. Таблица «Родственные связи»: каждая строка — пара «ID родителя — ID ребёнка»; указаны не все родители. Используя информацию из базы данных, '+question(Q,db)+' В ответе запишите только число.'}
  function dstr(i){return dsi(i)}
  function steps(db,Q){var f=kindFam(Q.kind),S=[],k=Q.kind;
    if(f==='sweets'){var P=prodMap(db),Sh={};T(db,'Магазин').forEach(function(s){Sh[s[0]]=s});
      var sh=shopsOf(db,Q.loc),pr=prodsOf(db,Q),rows=selMoves(db,Q,k!=='delta');
      S.push('Магазины (таблица «Магазин»), у которых '+(Q.loc.type==='district'?'район = «'+Q.loc.value+'»':'адрес начинается с «'+Q.loc.value+',»')+': '+sh.map(function(i){return i+' ('+Sh[i][1]+', '+Sh[i][2]+')'}).join('; ')+'.');
      S.push(('Товары (таблица «Товар»), у которых '+(Q.prefix?'наименование начинается с «'+Q.prefix+'»':'наименование = «'+Q.name+'»')+': '+pr.map(function(a){return'артикул '+a+' — '+P[a][2]+', '+P[a][3]+', '+P[a][4]+' в уп., '+P[a][5]+' руб.'}).join('; ')+'.').replace('..','.'));
      S.push('В «Движении товаров» оставляем строки: магазин из списка, артикул из списка, дата с '+dstr(Q.d1)+' по '+dstr(Q.d2)+' включительно'+(k==='delta'?', любой тип операции (знак зависит от типа)':', тип операции «'+Q.op+'»')+'. Подходит '+rows.length+' из '+T(db,'Движение товаров').length+' строк.');
      var vals=rows.map(function(m){return k==='mass'?m[4]*P[m[3]][4]:k==='revenue'?m[4]*P[m[3]][5]:k==='count_ops'?1:k==='delta'?(m[5]==='Поступление'?m[4]:-m[4]):m[4]});
      S.push('Вклад каждой строки: '+rows.map(function(m,i){return'ID '+m[0]+': '+(k==='mass'?m[4]+' уп. × '+P[m[3]][4]+' г = '+vals[i]+' г':k==='revenue'?m[4]+' уп. × '+P[m[3]][5]+' руб. = '+vals[i]:k==='delta'?(m[5]==='Поступление'?'+':'−')+m[4]+' уп.':k==='count_ops'?'1 операция':m[4]+' уп.')}).join('; ')+'.');
      var tot=sum(vals,function(x){return x}),sm=vals.map(function(x,i){return k==='delta'?(x<0?'− '+(-x):(i?'+ ':'')+x):(i?'+ ':'')+x}).join(' ');
      S.push('Сумма: '+sm+' = '+tot+(k==='mass'?' г = '+fmt(tot/1000)+' кг':'')+'.');
      S.push('Контроль: ответ целый, границы периода включены, тип операции проверен, единицы приведены (кг / руб. / упаковки).');return S}
    if(f==='theatre'){var pl={},tr={};T(db,'Спектакль').forEach(function(p){pl[p[0]]=p});T(db,'Тариф').forEach(function(t){tr[t[0]]=t});
      var ps=T(db,'Спектакль').filter(function(p){return(!Q.author||p[1]===Q.author)&&(!Q.genre||p[3]===Q.genre)}).map(function(p){return p[0]}),ts=T(db,'Тариф').filter(function(t){return(!Q.cat||t[1]===Q.cat)&&(!Q.benefit||t[2]===Q.benefit)}).map(function(t){return t[0]}),rw=thRows(db,Q);
      S.push('Спектакли (таблица «Спектакль»), подходящие по автору и жанру: '+ps.map(function(i){return i+' — '+pl[i][2]+', '+pl[i][3]}).join('; ')+'.');
      S.push('Тарифы (таблица «Тариф»), подходящие по категории и льготе: '+ts.map(function(i){return i+' — '+tr[i][1]+', льгота: '+tr[i][2]+', '+tr[i][3]+' руб.'}).join('; ')+'.');
      S.push('В «Продажах» оставляем строки: спектакль из списка, тариф из списка, дата с '+dstr(Q.d1)+' по '+dstr(Q.d2)+' включительно. Подходит '+rw.length+' из '+T(db,'Продажи').length+'.');
      if(k==='th_revenue'){S.push('Вклад каждой строки: '+rw.map(function(s){return'ID '+s[0]+': '+s[4]+' бил. × '+tr[s[3]][3]+' руб. = '+s[4]*tr[s[3]][3]}).join('; ')+'.');S.push('Сумма: '+rw.map(function(s){return s[4]*tr[s[3]][3]}).join(' + ')+' = '+ansTh(db,Q)+'.')}
      else{S.push('Количество билетов по строкам: '+rw.map(function(s){return'ID '+s[0]+': '+s[4]}).join('; ')+'.');S.push('Сумма: '+rw.map(function(s){return s[4]}).join(' + ')+' = '+ansTh(db,Q)+'.')}
      S.push('Контроль: условия соединены по «И» (автор, жанр, категория, льгота, период); границы дат включены.');return S}
    var M=famMaps(db),ids=Object.keys(M.nm).map(Number);
    if(k==='one_parent'){var on=ids.filter(function(p){return(M.par[p]||[]).length===1});S.push('Считаем, сколько раз каждый ID встречается в столбце «ID ребёнка» таблицы «Родственные связи»: ровно один раз — один родитель в базе.');S.push('Такие люди: '+on.map(function(p){return p+' ('+M.nm[p]+')'}).join(', ')+'.');S.push('Людей без родителей в базе (0 вхождений) и с двумя родителями (2 вхождения) не считаем. Всего: '+on.length+'.')}
    else if(k==='grandkids'){var ch=M.kids[Q.pid]||[],g=0;S.push('Дети человека '+Q.pid+' ('+M.nm[Q.pid]+'): '+ch.map(function(c){return c+' ('+M.nm[c]+')'}).join(', ')+'.');S.push('Дети этих детей (внуки): '+ch.map(function(c){g+=(M.kids[c]||[]).length;return'у '+c+': '+((M.kids[c]||[]).join(', ')||'нет')}).join('; ')+'.');S.push('Внуков всего: '+g+'.')}
    else if(k==='max_kids'){var cn=Object.keys(M.kids).map(Number).sort(function(a,b){return a-b});S.push('Считаем, сколько раз каждый ID встречается в столбце «ID родителя»: '+cn.map(function(a){return a+': '+M.kids[a].length}).join(', ')+'.');S.push('Наибольшее значение: '+ansFam(db,Q)+'.')}
    else{var ok=ids.filter(function(p){var pr=M.par[p]||[];return pr.length===2&&M.city[pr[0]]===M.city[pr[1]]});S.push('Берём людей с ровно двумя родителями и сравниваем города рождения родителей.');S.push('Подходят: '+(ok.map(function(p){var pr=M.par[p];return p+' ('+M.nm[p]+'; родители '+pr[0]+' и '+pr[1]+', город '+M.city[pr[0]]+')'}).join('; ')||'никто')+'.');S.push('Всего: '+ok.length+'.')}
    S.push('Контроль: строки связей — не люди; ребёнок с двумя родителями встречается в связях дважды.');return S}
  function hints(db,Q){var f=kindFam(Q.kind),H=[],k=Q.kind;
    if(f==='sweets'){var sh=shopsOf(db,Q.loc),pr=prodsOf(db,Q),rows=selMoves(db,Q,k!=='delta');
      H.push('Движение товаров хранит только ID магазина и артикул. Район или адрес берут из таблицы «Магазин», название и цену из таблицы «Товар»: по ключу, то есть по совпадению ID или артикула.');
      H.push('Начни с таблицы «Магазин». Найди строки, у которых '+(Q.loc.type==='district'?'район «'+Q.loc.value+'»':'адрес начинается с «'+Q.loc.value+',»')+'. Таких магазинов должно получиться '+sh.length+'.');
      H.push('Подходящие магазины: '+sh.join(', ')+'. Запиши их, они понадобятся.');
      H.push('Теперь таблица «Товар». Нужны товары, у которых '+(Q.prefix?'название начинается с «'+Q.prefix+'»':'название «'+Q.name+'»')+'. Их артикулы: '+pr.join(', ')+'.');
      H.push('В «Движении товаров» оставь строки, где ID магазина и артикул из твоих списков, дата с '+dsi(Q.d1)+' по '+dsi(Q.d2)+' ВКЛЮЧАЯ обе границы'+(k==='delta'?'. Тип операции не отбирай: он нужен для знака.':', а тип операции «'+Q.op+'». Должно остаться '+rows.length+' строк.'));
      H.push(k==='mass'?'Масса строки = упаковки × количество в упаковке (граммы). Сложи всё и раздели на 1000, чтобы получить килограммы.':k==='revenue'?'Выручка строки = упаковки × цена за упаковку из таблицы «Товар». Сложи по всем оставшимся строкам.':k==='delta'?'Поступление прибавляй, продажу вычитай. Сложи все числа со знаками.':k==='count_ops'?'Нужно число оставшихся строк, а не сумма упаковок.':'Сложи столбец «Количество упаковок» по оставшимся строкам.')}
    else if(f==='theatre'){var ps=T(db,'Спектакль').filter(function(p){return(!Q.author||p[1]===Q.author)&&(!Q.genre||p[3]===Q.genre)}).map(function(p){return p[0]}),ts=T(db,'Тариф').filter(function(t){return(!Q.cat||t[1]===Q.cat)&&(!Q.benefit||t[2]===Q.benefit)}).map(function(t){return t[0]});
      H.push('Таблица «Продажи» хранит только ID спектакля и ID тарифа. Автора и жанр берут из «Спектакль», категорию, льготу и цену из «Тариф».');
      H.push('Отбери спектакли по автору и жанру (условия соединяй по «И»). Их ID: '+ps.join(', ')+'.');
      H.push('Отбери тарифы'+(Q.cat||Q.benefit?' по категории зрителя и льготе. Их ID: '+ts.join(', ')+'.':': условий по тарифу нет, подходят все.'));
      H.push('В «Продажах» оставь строки с этими спектаклями и тарифами и датой с '+dsi(Q.d1)+' по '+dsi(Q.d2)+' включительно. Должно остаться '+thRows(db,Q).length+' строк.');
      H.push(Q.kind==='th_revenue'?'Выручка строки = количество билетов × цена билета из таблицы «Тариф». Сложи по всем строкам.':'Нужна сумма столбца «Количество билетов», а не число строк.')}
    else{if(k==='one_parent'){H.push('Родитель описан строкой в «Родственных связях». У ребёнка один родитель, если его ID встречается в столбце «ID ребёнка» ровно один раз.');H.push('Выпиши столбец «ID ребёнка» и посчитай, сколько раз встречается каждый ID. Нужны те, у кого ровно одно вхождение (ноль не считается).')}
      else if(k==='max_kids'){H.push('Ребёнок описан строкой связи, в столбце «ID родителя» стоит родитель.');H.push('Посчитай, сколько раз каждый ID встречается в столбце «ID родителя». Наибольшее из этих чисел и есть ответ.')}
      else if(k==='grandkids'){H.push('Внуки человека это дети его детей.');H.push('Сначала найди детей человека '+Q.pid+' (строки, где «ID родителя» = '+Q.pid+'). Потом для каждого ребёнка найди его детей.')}
      else{H.push('Сначала найди людей, у которых в столбце «ID ребёнка» ровно два вхождения: два родителя.');H.push('Для каждого такого человека посмотри в таблице «Люди» город рождения обоих родителей и сравни.')}}
    if(f==='sweets')return[H[1],H[3],H[4]+' '+H[5]];if(f==='theatre')return[H[1],H[2],H[3]+' '+H[4]];return H.slice(0,3)}
  function mistake(db,Q){var f=kindFam(Q.kind),w=f==='sweets'?wrongSw(db,Q):f==='theatre'?wrongTh(db,Q):[];
    if(!w.length)return f==='family'?'Ошибка: считать строки связей как людей. Связь это пара «родитель — ребёнок», а не человек.':'';
    return'Типичные неверные ответы: '+w.slice(0,3).map(function(x){return fmt(x[0])+' — '+x[1]}).join('; ')+'.'}
  function schema(db){var n=db.map(function(t){return t.n});
    if(n.indexOf('Движение товаров')>=0)return'Связи: «Движение товаров».ID магазина → «Магазин».ID магазина; «Движение товаров».Артикул → «Товар».Артикул.';
    if(n.indexOf('Продажи')>=0)return'Связи: «Продажи».ID спектакля → «Спектакль».ID спектакля; «Продажи».ID тарифа → «Тариф».ID тарифа.';
    return'Связи: «Родственные связи».ID родителя и ID ребёнка → «Люди».ID.'}
  window.exFill3=function(q){var Q=q.query;if(!Q||!q.db)return;
    if(!q.s)q.s=steps(q.db,Q);if(!q.h)q.h=hints(q.db,Q);if(!q.m)q.m=mistake(q.db,Q);q._v=fmt(answer(q.db,Q))};
  window.exDb=function(db){return'<div class="exdb">'+db.map(function(t){return'<div class="exdbt"><div class="exdbn">'+esc(t.n)+' <small>'+t.r.length+' '+(t.r.length%10===1&&t.r.length%100!==11?'строка':(t.r.length%10>=2&&t.r.length%10<=4&&(t.r.length%100<10||t.r.length%100>=20))?'строки':'строк')+'</small></div><div class="exdbs"><table class="exdbtab"><tr>'+t.h.map(function(x){return'<th>'+esc(x)+'</th>'}).join('')+'</tr>'+t.r.map(function(r){return'<tr>'+r.map(function(x){return'<td>'+esc(String(x))+'</td>'}).join('')+'</tr>'}).join('')+'</table></div></div>'}).join('')+'<p class="exdbk">'+esc(schema(db))+'</p><p class="exdbk">Нажимай на строки, чтобы отмечать подходящие.</p></div>'};
  document.addEventListener('click',function(e){var tr=e.target.closest&&e.target.closest('.exdbtab tr');if(tr&&!tr.querySelector('th'))tr.classList.toggle('sel')});
  /* ---------- генератор ---------- */
  function genSweets(r,sp){
    for(var at=0;at<300;at++){
      var month=exPick(r,[6,8,9,10]),nSh=sp.nShops||6,nPr=sp.nPrd||9,fam=exPick(r,FAMS),must=CAT.filter(function(c){return c[0].indexOf(fam)===0}).slice(0,3).map(function(c){return c[0]}),name=null;
      if(sp.pool==='name'){var cs=CAT.filter(function(c){return c[2]==='г'||sp.kind!=='mass'});name=exPick(r,cs)[0];must=[name].concat(must.filter(function(m){return m!==name}).slice(0,1))}
      var chosen=CAT.filter(function(c){return must.indexOf(c[0])>=0}),others=exShuf(r,CAT.filter(function(c){return must.indexOf(c[0])<0}));chosen=exShuf(r,chosen.concat(others.slice(0,Math.max(0,nPr-chosen.length))));
      var arts=exShuf(r,Array.apply(null,{length:59}).map(function(_,i){return i+1})).slice(0,chosen.length).sort(function(a,b){return a-b});
      var prod=chosen.map(function(c,i){return[arts[i],c[1],c[0],c[2],c[3],c[4]]}),sts=exShuf(r,STR).slice(0,3),dists=exShuf(r,DIST).slice(0,3),shops=[];
      for(var i=0;i<nSh;i++){var st=i<sts.length*2?sts[i%sts.length]:exPick(r,sts);shops.push(['М'+(i+1),exPick(r,dists),st[0]+' '+st[1]+', '+ri(r,1,59)])}
      var loc;if(sp.loc==='street'){var by={};shops.forEach(function(s){var k=s[2].split(',')[0];(by[k]=by[k]||[]).push(s[0])});var cand=Object.keys(by).filter(function(k){return by[k].length>=2});if(!cand.length)continue;loc={type:'street',value:exPick(r,cand)}}
      else{var dd={};shops.forEach(function(s){dd[s[1]]=1});loc={type:'district',value:exPick(r,Object.keys(dd))}}
      var L=ri(r,5,9),days=14,d0=ri(r,2,Math.max(2,days-L)),Q={kind:sp.kind,loc:loc,d1:isoOf(2026,month,d0),d2:isoOf(2026,month,d0+L-1)};
      if(name)Q.name=name;else Q.prefix=fam;if(sp.kind!=='delta')Q.op=sp.op;
      var db0=[{n:'Движение товаров',h:[],r:[]},{n:'Товар',h:[],r:prod},{n:'Магазин',h:[],r:shops}],hs=shopsOf(db0,loc),hp=prodsOf(db0,Q);if(!hp.length||!hs.length)continue;
      var os=shops.map(function(s){return s[0]}).filter(function(x){return hs.indexOf(x)<0}),op2=prod.map(function(p){return p[0]}).filter(function(x){return hp.indexOf(x)<0});if(!os.length||!op2.length)continue;
      var rows=[];function add(day,sh,art,pk,t){rows.push([day,sh,art,pk,t])}
      var nh=ri(r,sp.hit[0],sp.hit[1]),op=Q.op;
      for(i=0;i<nh;i++){var day=i===0?d0:i===1?d0+L-1:ri(r,d0,d0+L-1);add(day,exPick(r,hs),exPick(r,hp),exPick(r,PK),sp.kind==='delta'?(i%3!==2?'Поступление':'Продажа'):op)}
      var oo=op==='Поступление'?'Продажа':'Поступление';
      add(ri(r,d0,d0+L-1),exPick(r,hs),exPick(r,hp),exPick(r,[4,6,10,20]),oo);add(ri(r,d0,d0+L-1),exPick(r,hs),exPick(r,hp),exPick(r,[3,5,12]),oo);
      add(d0-1,exPick(r,hs),exPick(r,hp),exPick(r,[5,10,20]),op||'Поступление');add(d0+L,exPick(r,hs),exPick(r,hp),exPick(r,[5,10,20]),op||'Поступление');
      add(ri(r,d0,d0+L-1),exPick(r,os),exPick(r,hp),exPick(r,[4,8,12]),op||'Поступление');add(ri(r,d0,d0+L-1),exPick(r,hs),exPick(r,op2),exPick(r,[4,8,12]),op||'Поступление');
      while(rows.length<sp.nMoves)add(ri(r,1,days),exPick(r,shops)[0],exPick(r,prod)[0],exPick(r,PK),r()<.55?'Поступление':'Продажа');
      rows.sort(function(a,b){return a[0]-b[0]||(a[1]<b[1]?-1:a[1]>b[1]?1:0)||a[2]-b[2]});
      var mv=rows.map(function(x,i){return[i+1,ds(2026,month,x[0]),x[1],x[2],x[3],x[4]]});
      var db=[{n:'Движение товаров',h:['ID операции','Дата','ID магазина','Артикул','Количество упаковок, шт.','Тип операции'],r:mv},{n:'Товар',h:['Артикул','Отдел','Наименование товара','Ед_изм','Количество в упаковке','Цена за упаковку'],r:prod},{n:'Магазин',h:['ID магазина','Район','Адрес'],r:shops}];
      if(sp.kind==='mass'){var sel=selMoves(db,Q,1),fixed=false;
        for(var z=sel.length-1;z>=0&&!fixed;z--){for(var pk=2;pk<=40;pk++){var old=sel[z][4];sel[z][4]=pk;var a0=ansSw(db,Q);if(Math.abs(a0-Math.round(a0))<1e-9&&a0>=1){fixed=true;break}sel[z][4]=old}}
        if(!fixed)continue}
      var a=ansSw(db,Q);if(a<(sp.min||1)||Math.abs(a-Math.round(a))>1e-9)continue;if(wrongSw(db,Q).length<2)continue;
      if(sp.kind!=='delta'&&ansSw(db,cp(Q,{d2:addDay(Q.d2,-1)}))===a)continue;
      return{db:db,Q:Q,month:month,a:a}}
    return null}
  function genTheatre(r,sp){
    for(var at=0;at<500;at++){var pls=exShuf(r,PLAYS).slice(0,6).map(function(p,i){return['С'+(i+1)].concat(p)}),tars=TARS.map(function(t,i){return['Т'+(i+1)].concat(t)}),n=sp.n,sales=[];
      for(var i=0;i<n;i++)sales.push([ri(r,1,10),exPick(r,pls)[0],exPick(r,tars)[0],ri(r,1,6)]);sales.sort(function(a,b){return a[0]-b[0]});
      var db=[{n:'Продажи',h:['ID продажи','Дата','ID спектакля','ID тарифа','Количество билетов'],r:sales.map(function(s,i){return[i+1,ds(2026,10,s[0]),s[1],s[2],s[3]]})},{n:'Спектакль',h:['ID спектакля','Автор','Название','Жанр'],r:pls},{n:'Тариф',h:['ID тарифа','Категория зрителя','Льгота','Цена билета, руб.'],r:tars}];
      var pp=exPick(r,pls),L=ri(r,4,8),d1=ri(r,1,Math.max(1,10-L)),Q={kind:sp.kind,d1:isoOf(2026,10,d1),d2:isoOf(2026,10,d1+L-1),author:pp[1],genre:pp[3]};
      if(sp.cat){var tt=exPick(r,tars);Q.cat=tt[1];if(sp.benefit)Q.benefit=tt[2]}
      var a=ansTh(db,Q);if(thRows(db,Q).length<3||a<=0||wrongTh(db,Q).length<3)continue;
      return{db:db,Q:Q,month:10,a:a}}return null}
  function genFamily(r,sp){
    for(var at=0;at<2000;at++){var people=[],rel=[],nid=0;
      function newp(sex,y,si,c){nid++;var sn=SURN[si];people.push([nid,(sex==='М'?sn[0]:sn[1])+' '+exPick(r,sex==='М'?IM:IF),sex,y,c]);return nid}
      var g0=[];for(var f=0;f<2;f++){var si=Math.floor(r()*SURN.length);g0.push([newp('М',ri(r,1940,1950),si,exPick(r,CITY)),newp('Ж',ri(r,1942,1952),(si+1)%SURN.length,exPick(r,CITY))])}
      var cur=[];g0.forEach(function(g){var nk=ri(r,2,3);for(var j=0;j<nk;j++){var sex=exPick(r,['М','Ж']),c=newp(sex,ri(r,1968,1978),Math.floor(r()*SURN.length),exPick(r,CITY));[g[0],g[1]].forEach(function(pa,ix){if(ix===1&&r()<.2)return;rel.push([pa,c])});cur.push(c)}});
      var pm=exShuf(r,cur.filter(function(p){return people[p-1][2]==='М'})),pf=exShuf(r,cur.filter(function(p){return people[p-1][2]==='Ж'}));
      for(var z=0;z<Math.min(pm.length,pf.length);z++){var nk2=ri(r,1,3);for(var j2=0;j2<nk2;j2++){var c2=newp(exPick(r,['М','Ж']),ri(r,1992,2005),Math.floor(r()*SURN.length),exPick(r,CITY));rel.push([pm[z],c2]);if(r()<.85)rel.push([pf[z],c2])}}
      rel.sort(function(a,b){return a[0]-b[0]||a[1]-b[1]});
      var db=[{n:'Люди',h:['ID','Фамилия_И.О.','Пол','Год рождения','Город рождения'],r:people},{n:'Родственные связи',h:['ID родителя','ID ребёнка'],r:rel}],Q={kind:sp.kind};
      if(sp.kind==='grandkids'){var M=famMaps(db),cand=Object.keys(M.kids).map(Number).filter(function(p){var n=0;M.kids[p].forEach(function(c){n+=(M.kids[c]||[]).length});return n>=2});if(!cand.length)continue;Q.pid=exPick(r,cand)}
      var a=ansFam(db,Q);if(a<2||(sp.kind==='max_kids'&&a<3))continue;return{db:db,Q:Q,month:10,a:a}}return null}
  var SPEC={'3.1':function(r){return{f:'sw',kind:'mass',pool:'prefix',op:exPick(r,['Поступление','Продажа']),loc:exPick(r,['street','district']),nMoves:exPick(r,[22,26,30]),hit:[5,7]}},
    '3.2':function(r){return{f:'sw',kind:'revenue',pool:exPick(r,['prefix','name']),op:'Продажа',loc:exPick(r,['street','district']),nMoves:exPick(r,[22,26]),hit:[5,7]}},
    '3.3':function(r){return{f:'sw',kind:'delta',pool:exPick(r,['prefix','name']),loc:exPick(r,['street','district']),nMoves:exPick(r,[22,26]),hit:[5,7],min:5}},
    '3.4':function(r){return{f:'sw',kind:exPick(r,['packs','packs','count_ops']),pool:exPick(r,['prefix','name']),op:exPick(r,['Поступление','Продажа']),loc:exPick(r,['street','district']),nMoves:exPick(r,[22,26]),hit:[5,7]}},
    '3.5':function(r){var v=exPick(r,[0,1,2]);return{f:'th',kind:v?'th_revenue':'th_count',cat:v>0,benefit:v>1,n:exPick(r,[22,24,26])}},
    '3.6':function(r){return{f:'fm',kind:exPick(r,['one_parent','grandkids','max_kids','parents_same_city'])}}};
  var FMT='Одно целое число, без единиц измерения.';
  EXGEN[3]={no:3,name:'Базы данных',types:[{id:'3.1',n:'Масса товара',d:'Поступило или продано, в килограммах'},{id:'3.2',n:'Выручка',d:'Упаковки × цена'},{id:'3.3',n:'Изменение запаса',d:'Поступление минус продажа'},{id:'3.4',n:'Упаковки и операции',d:'Сумма или число строк'},{id:'3.5',n:'Театр',d:'Билеты и выручка по условиям'},{id:'3.6',n:'Люди и родственники',d:'Подсчёт по связям'}],
    make:function(type,r){r=r||exRnd((Date.now()^(Math.random()*4294967296))>>>0);if(type==='any')type=exPick(r,['3.1','3.1','3.2','3.3','3.4','3.5','3.6']);
      var sp=SPEC[type](r),g=sp.f==='sw'?genSweets(r,sp):sp.f==='th'?genTheatre(r,sp):genFamily(r,sp);if(!g)return null;
      var q={q:statement(g.Q,g.db,g.month),db:g.db,query:g.Q,f:FMT,a:fmt(g.a),type:type};exFill3(q);return q}};
  window.ex3={answer:answer,steps:steps,hints:hints,fmt:fmt};
})();
