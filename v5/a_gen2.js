/* ===================== v5.1.3: задание №2 ЕГЭ (таблицы истинности), генератор и разбор ===================== */
(function(){
  var VARS='wxyz',SYM={and:'∧',or:'∨',imp:'→',eq:'≡',xor:'⊕'};
  function V(n){return['v',n]}function Not(e){return['not',e]}
  function Op(t){return function(a,b){return[t,a,b]}}
  var And=Op('and'),Or=Op('or'),Imp=Op('imp'),Eq=Op('eq'),Xor=Op('xor');
  function ev(e,env){var t=e[0];if(t==='v')return env[e[1]];if(t==='not')return 1-ev(e[1],env);
    var a=ev(e[1],env),b=ev(e[2],env);return t==='and'?a&b:t==='or'?a|b:t==='imp'?(1-a)|b:t==='eq'?1-(a^b):a^b}
  function render(e){
    var t=e[0];if(t==='v')return e[1];
    if(t==='not'){var c=e[1];return'¬'+(c[0]==='v'||c[0]==='not'?render(c):'('+render(c)+')')}
    function flat(x){return x[0]===t&&(t==='and'||t==='or')?flat(x[1]).concat(flat(x[2])):[x]}
    var items=(t==='and'||t==='or')?flat(e):[e[1],e[2]];
    return items.map(function(it){var s=render(it);
      if(SYM[it[0]]&&(it[0]!==t||(t!=='and'&&t!=='or')))s='('+s+')';return s}).join(' '+SYM[t]+' ')}
  function vars(e,o){o=o||{};if(e[0]==='v')o[e[1]]=1;else for(var i=1;i<e.length;i++)vars(e[i],o);return o}
  function bits4(i){return[(i>>3)&1,(i>>2)&1,(i>>1)&1,i&1]}
  function truthCol(e){var c=[];for(var i=0;i<16;i++){var b=bits4(i);c.push(ev(e,{w:b[0],x:b[1],y:b[2],z:b[3]}))}return c}
  function dependsAll(col){for(var k=0;k<4;k++){var s=3-k,same=true;for(var i=0;i<16;i++)if(col[i]!==col[i^(1<<s)]){same=false;break}if(same)return false}return true}
  var BIT={w:3,x:2,y:1,z:0};
  function completions(col,perm,cells,f){var mask=0,val=0;
    for(var j=0;j<4;j++)if(cells[j]!==null){var b=BIT[perm[j]];mask|=1<<b;val|=cells[j]<<b}
    var o=[];for(var i=0;i<16;i++)if(col[i]===f&&(i&mask)===val)o.push(i);return o}
  function distinctOk(lists){
    function rec(k,used){if(k===lists.length)return true;
      for(var n=0;n<lists[k].length;n++){var c=lists[k][n];if(used.indexOf(c)<0&&rec(k+1,used.concat([c])))return true}return false}
    return rec(0,[])}
  var PERMS=(function(){var o=[];function p(a,r){if(!a.length){o.push(r);return}for(var i=0;i<a.length;i++)p(a.slice(0,i).concat(a.slice(i+1)),r+a[i])}p(VARS.split(''),'');return o})();
  function consistent(col,rows,upto){var R=upto?rows.slice(0,upto):rows,res=[];
    PERMS.forEach(function(pm){var L=R.map(function(r){return completions(col,pm,r[0],r[1])});
      if(L.every(function(l){return l.length})&&distinctOk(L))res.push(pm)});return res}
  function colOpts(perms){var o=[];for(var j=0;j<4;j++){var s={};perms.forEach(function(p){s[p[j]]=1});o.push(Object.keys(s).sort().join(''))}return o}
  /* ---------- генераторы выражений ---------- */
  function lit(r,v,p){p=p===undefined?.3:p;return r()<p?Not(V(v)):V(v)}
  function clause(r,k,a,b){return Op(k)(lit(r,a),lit(r,b))}
  function gDisj(r){var s=exShuf(r,VARS.split('')),p=s[0],q=s[1],rr=s[2],t=s[3];
    var k=function(){return exPick(r,['and','imp','eq','and'])};
    var t1=clause(r,k(),p,q),t2=clause(r,k(),exPick(r,[p,q]),rr),t3=r()<.5?lit(r,t,.5):clause(r,k(),exPick(r,[rr,p]),t);
    return Or(Or(t1,t2),t3)}
  function gConj(r){var s=exShuf(r,VARS.split('')),p=s[0],q=s[1],rr=s[2],t=s[3];
    var k=function(){return exPick(r,['imp','eq','or','imp'])};
    var c1=clause(r,k(),p,q),c2=clause(r,k(),exPick(r,[p,q]),rr),c3=r()<.7?clause(r,k(),exPick(r,[rr,p]),t):Or(lit(r,t),lit(r,rr));
    return And(And(c1,c2),c3)}
  function four(r){var s=exShuf(r,VARS.split(''));return[V(s[0]),V(s[1]),V(s[2]),V(s[3])]}
  function gMixed(r){var f=four(r),a=f[0],b=f[1],c=f[2],d=f[3];
    return exPick(r,[function(){return Or(And(Imp(a,b),Imp(b,c)),Eq(d,Or(a,b)))},function(){return And(Imp(Or(a,b),c),Or(d,Not(b)))},
      function(){return Or(Imp(And(a,b),c),Not(And(d,a)))},function(){return Or(Imp(Or(a,b),And(c,d)),Eq(a,c))},
      function(){return And(Or(Not(a),b),Or(Imp(c,d),And(a,Not(b))))},function(){return Or(Imp(Imp(a,b),c),Not(d))},
      function(){return And(Imp(Eq(a,b),Or(c,d)),Or(a,Not(c)))},function(){return Imp(And(Imp(a,b),c),Or(d,Not(a)))}])()}
  function gXor(r){var f=four(r),a=f[0],b=f[1],c=f[2],d=f[3];
    return exPick(r,[function(){return Imp(Xor(a,b),Eq(c,d))},function(){return Or(Xor(Eq(a,b),c),And(d,a))},
      function(){return And(Xor(a,b),Imp(c,Eq(d,a)))},function(){return Or(Not(Eq(a,b)),Xor(c,d))},
      function(){return Eq(Xor(a,b),Or(c,Not(d)))},function(){return And(Or(Xor(a,c),b),Imp(d,Xor(a,b)))}])()}
  var GEN={disj:gDisj,conj:gConj,mixed:gMixed,xor:gXor};
  function pickRows(r,col,rule){
    var z=[],o=[],i;for(i=0;i<16;i++)(col[i]?o:z).push(i);var rows,rest;
    function fill(a,k){var rs=exShuf(r,a).slice(0,k);rest=[];for(var i=0;i<16;i++)if(rs.indexOf(i)<0)rest.push(i);return rs.concat(exShuf(r,rest).slice(0,3-k))}
    if(rule==='zero2'&&z.length>=2)rows=fill(z,z.length>=3?exPick(r,[2,3]):2);
    else if(rule==='one2'&&o.length>=2)rows=fill(o,o.length>=3?exPick(r,[2,3]):2);
    else if(rule==='mix'&&z.length&&o.length){rows=[exPick(r,z),exPick(r,o)];rest=[];for(i=0;i<16;i++)if(rows.indexOf(i)<0)rest.push(i);rows.push(exPick(r,rest))}
    else rows=exShuf(r,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]).slice(0,3);
    return exShuf(r,rows)}
  function ri(r,lo,hi){return lo+Math.floor(r()*(hi-lo+1))}
  function makeFragment(r,sp){
    for(var tr=0;tr<3000;tr++){
      var e=GEN[sp.cls](r);if(Object.keys(vars(e)).length!==4)continue;
      var col=truthCol(e);if(!dependsAll(col))continue;
      var ones=col.reduce(function(a,b){return a+b},0);if(ones<4||ones>12)continue;
      var idx=pickRows(r,col,sp.rule),perm=exShuf(r,VARS.split('')).join(''),full=[];
      idx.forEach(function(i){var b=bits4(i),a={w:b[0],x:b[1],y:b[2],z:b[3]};full.push([0,1,2,3].map(function(j){return a[perm[j]]}))});
      var fr=full.map(function(c,k){return[c,col[idx[k]]]});
      var cp=consistent(col,fr);if(cp.length!==1||cp[0]!==perm)continue;
      var target=ri(r,sp.blanks[0],sp.blanks[1]),pos=[];for(var a=0;a<3;a++)for(var j=0;j<4;j++)pos.push([a,j]);pos=exShuf(r,pos);
      var bl={},nb=0;
      for(var p=0;p<pos.length&&nb<target;p++){var a2=pos[p][0],j2=pos[p][1],key=a2+','+j2;
        var cnt=0;for(var jj=0;jj<4;jj++)if(bl[a2+','+jj]||jj===j2)cnt++;if(cnt===4)continue;
        bl[key]=1;
        var rt=full.map(function(c,k){return[c.map(function(v,jx){return bl[k+','+jx]?null:v}),col[idx[k]]]});
        var c2=consistent(col,rt);if(c2.length===1&&c2[0]===perm)nb++;else delete bl[key]}
      if(nb<sp.blanks[0])continue;
      var rows=full.map(function(c,k){return[c.map(function(v,jx){return bl[k+','+jx]?null:v}),col[idx[k]]]});
      if(consistent(col,rows).join()!==perm)continue;
      var n2=consistent(col,rows,2).length;if(n2<sp.n2[0]||n2>sp.n2[1])continue;
      return{expr:e,text:render(e),col:col,rows:rows,answer:perm}}
    return null}
  /* ---------- таблица на 3 переменных ---------- */
  function gen3(r){var s=exShuf(r,['x','y','z']),a=V(s[0]),b=V(s[1]),c=V(s[2]);
    return exPick(r,[function(){return And(Or(a,b),Not(c))},function(){return And(Imp(a,b),Imp(b,c))},function(){return Or(And(a,Not(b)),Eq(b,c))},
      function(){return Or(Not(And(a,b)),c)},function(){return Imp(Eq(a,b),Not(c))},function(){return Or(Xor(a,b),And(b,c))},
      function(){return Imp(Or(a,Not(b)),c)},function(){return And(Eq(a,Not(b)),Or(b,c))}])()}
  function make3(r){for(var tr=0;tr<500;tr++){var e=gen3(r);if(Object.keys(vars(e)).length!==3)continue;
    var col=[];for(var i=0;i<8;i++)col.push(ev(e,{x:(i>>2)&1,y:(i>>1)&1,z:i&1}));
    var s=col.reduce(function(a,b){return a+b},0);if(s<3||s>5)continue;return{expr:e,text:render(e),col:col,answer:col.join('')}}return null}
  /* ---------- тексты ---------- */
  var STM4=function(t){return'Логическая функция F задаётся выражением '+t+'. На рисунке приведён частично заполненный фрагмент таблицы истинности функции F: три различные строки; в некоторых клетках значения пропущены, над столбцами вместо переменных стоит «???». Определите, какому столбцу таблицы соответствует каждая из переменных w, x, y, z. В ответе запишите буквы w, x, y, z подряд, без пробелов, в том порядке, в котором идут их столбцы слева направо.'};
  var STM3=function(t){return'Логическая функция F задаётся выражением '+t+'. Постройте её таблицу истинности для переменных x, y, z. В ответе запишите 8 значений F подряд, без пробелов, в порядке наборов (x, y, z) = 000, 001, 010, 011, 100, 101, 110, 111.'};
  var FM4='Четыре буквы w, x, y, z подряд, без пробелов, например zywx.',FM3='Восемь цифр 0 и 1 подряд, без пробелов.';
  var QM={'2.1':'Берут слабую строку (F = 1) первой и не могут отсеять порядки. Сначала нужны строки с F = 0.','2.2':'Берут слабую строку (F = 0) первой. Для конъюнкции сильная строка это F = 1.','2.3':'Не раскрывают скобки по частям и путают, какая операция верхняя.','2.4':'Сразу пытаются угадать порядок. Лучше выписать, какие переменные могут стоять в каждом столбце.','2.5':'Путают ⊕ и ≡: «⊕» это «разные», «≡» это «одинаковые».','2.6':'Выполняют операции не по порядку: сначала ¬, потом скобки, потом ∧, ∨, →.'};
  function bs(i,n){var s=i.toString(2);while(s.length<n)s='0'+s;return s}
  function topOp(t){var d=0,f={};for(var i=0;i<t.length;i++){var ch=t[i];if(ch==='(')d++;else if(ch===')')d--;else if(d===0&&SYM_R[ch])f[SYM_R[ch]]=1}
    return f.imp?'imp':f.eq?'eq':f.xor?'xor':f.or?'or':f.and?'and':'not'}
  var SYM_R={'∧':'and','∨':'or','→':'imp','≡':'eq','⊕':'xor'};
  var OPN={or:'дизъюнкция ∨',and:'конъюнкция ∧',imp:'импликация →',eq:'эквиваленция ≡',xor:'исключающее ИЛИ ⊕',not:'отрицание ¬'};
  function pl(n,a){var m=n%10,h=n%100;return n+' '+(m===1&&h!==11?a[0]:m>=2&&m<=4&&(h<10||h>=20)?a[1]:a[2])}
  /* разбор по тексту выражения и таблице значений: работает и для готовых заданий, и для созданных */
  function sol4(text,col,rows,ans){
    var op=topOp(text),ones=col.reduce(function(a,b){return a+b},0),sv;
    if(op==='or'||op==='imp')sv=0;else if(op==='and')sv=1;else sv=ones<=8?1:0;
    var why={or:'Дизъюнкция равна 0 только тогда, когда ВСЕ слагаемые равны 0, поэтому нулей у такой функции мало и они сильно ограничивают переменные.',
      and:'Конъюнкция равна 1 только тогда, когда ВСЕ множители равны 1, поэтому единиц у такой функции мало и они сильно ограничивают переменные.',
      imp:'Импликация равна 0 в единственном случае: «из истины следует ложь». Поэтому нулей мало.'}[op]||('Здесь «редкое» значение F: '+sv+' (таких наборов меньше).');
    var ss=[];for(var i=0;i<16;i++)if(col[i]===sv)ss.push(i);
    var s=['Верхняя операция выражения F = '+text+': '+OPN[op]+'. '+why,
      'Выписываем все наборы (w x y z), на которых F = '+sv+': '+(ss.length<=10?ss.map(function(i){return bs(i,4)}).join(', '):'их '+ss.length+' из 16, перечислять не будем')+'. Строка таблицы с таким значением F обязана быть одним из этих наборов.'];
    var ord=[0,1,2].sort(function(a,b){return(rows[a][1]!==sv)-(rows[b][1]!==sv)||a-b});
    s.push('Сначала строки с F = '+sv+' (они ограничивают сильнее): порядок '+ord.map(function(i){return i+1}).join(', ')+'.');
    var prev=[];
    for(var k=0;k<3;k++){
      var ri=ord[k],cells=rows[ri][0],f=rows[ri][1],z=0,o=0;cells.forEach(function(c){if(c===0)z++;else if(c===1)o++});
      var fits=[];for(i=0;i<16;i++)if(col[i]===f){var b=bits4(i),oo=b[0]+b[1]+b[2]+b[3];if(oo>=o&&4-oo>=z)fits.push(i)}
      var sub=ord.slice(0,k+1).map(function(i){return rows[i]}),pm=consistent(col,sub),op2=colOpts(pm);
      var line='Строка '+(ri+1)+': '+cells.map(function(c){return c===null?'_':c}).join(' ')+' | F = '+f+'. Нужны наборы с F = '+f+', где не меньше '+z+' нулей и '+o+' единиц';
      line+=(fits.length<=8?': '+fits.map(function(i){return bs(i,4)}).join(', '):' (их '+fits.length+')')+'. ';
      line+='Столбцы теперь: '+op2.map(function(x,j){return(j+1)+'-й: '+x.split('').join(', ')}).join('; ')+'.';
      if(pm.length===1)line+=' Остался один порядок: '+pm[0]+'.';
      s.push(line);prev=pm}
    var fin=consistent(col,rows);
    s.push('Порядок столбцов: '+(fin[0]||ans)+'.');
    return s}
  function hints4(text,col,rows){
    var op=topOp(text),sv=(op==='or'||op==='imp')?0:(op==='and'?1:(col.reduce(function(a,b){return a+b},0)<=8?1:0));
    var n=col.filter(function(v){return v===sv}).length;
    return['Найди верхнюю операцию: какое значение F у неё «редкое»?','Выпиши наборы с F = '+sv+' (их '+n+'). Строка с таким F должна быть одним из них.','Начни со строки, где больше всего известных клеток: по числу нулей и единиц отсеки наборы, потом расставь переменные по столбцам.']}
  function sol6(text,col,e){
    var s=['Выражение F = '+text+'. Переменных три, поэтому наборов 2³ = 8. Наборы (x y z) идут как двоичные числа: 000, 001, 010, 011, 100, 101, 110, 111.'],out=[];
    var op=e?e[0]:topOp(text);
    if(e&&SYM[e[0]]){var L=e[1],R=e[2];s.push('Верхняя операция «'+SYM[e[0]]+'». Считаем отдельно левую часть A = '+render(L)+' и правую B = '+render(R)+', потом F.');
      for(var i=0;i<8;i++){var env={x:(i>>2)&1,y:(i>>1)&1,z:i&1};out.push(bs(i,3)+': A='+ev(L,env)+', B='+ev(R,env)+', F='+col[i])}}
    else for(i=0;i<8;i++)out.push(bs(i,3)+': F='+col[i]);
    s.push(out.join('; ')+'.');s.push('Выписываем F сверху вниз: '+col.join('')+'.');return s}
  /* общая подготовка готовых заданий из data: {col, rows, expr} */
  function st2(text,col){var op=topOp(text),sv=(op==='or'||op==='imp')?0:(op==='and'?1:(col.reduce(function(a,b){return a+b},0)<=8?1:0));
    return"print('w x y z')\nfor w in range(2):\n    for x in range(2):\n        for y in range(2):\n            for z in range(2):\n                F = 0  # впиши выражение через and, or, not\n                if "+(sv?'F':'not F')+":\n                    print(w, x, y, z)\n"}
  window.exFill2=function(q){
    if(q.rows&&!q.starter)q.starter=st2(q.expr,q.col);
    if(q.rows){q.tb={r:q.rows.map(function(x){return x[0]}),f:q.rows.map(function(x){return x[1]})};
      if(!q.s)q.s=sol4(q.expr,q.col,q.rows,q.a);if(!q.h)q.h=hints4(q.expr,q.col,q.rows)}
    else{if(!q.s)q.s=sol6(q.expr,q.col);if(!q.h)q.h=['Сколько всего наборов у трёх переменных?','Посчитай значение каждой скобки отдельно.','Запиши F сверху вниз.']}};
  window.exTb=function(tb){
    var h='<table class="exft"><tr>'+'<th>???</th><th>???</th><th>???</th><th>???</th><th class="fc">F</th></tr>';
    tb.r.forEach(function(r,i){h+='<tr>'+r.map(function(c){return'<td>'+(c===null?'':c)+'</td>'}).join('')+'<td class="fc">'+tb.f[i]+'</td></tr>'});
    return h+'</table>'};
  window.exEx2={sol4:sol4,sol6:sol6,render:render,consistent:consistent};
  window.ex2Fill=function(root){root.querySelectorAll('.ex2').forEach(function(el){
    var d=typeof EX2D!=='undefined'&&EX2D[el.dataset.id];if(!d||el.dataset.ok)return;el.dataset.ok=1;var h='';
    if(d.rows)h+='<figure class="exf exfw">'+exTb({r:d.rows.map(function(x){return x[0]}),f:d.rows.map(function(x){return x[1]})})+'</figure>';
    if(el.dataset.sol){var s=d.s||(d.rows?sol4(d.expr,d.col,d.rows,d.a):sol6(d.expr,d.col));
      h+='<p><b>Решение по шагам:</b></p><ol>'+s.map(function(x){return'<li>'+esc(x)+'</li>'}).join('')+'</ol><p><b>Ответ: '+esc(d.a)+'</b></p>'}
    el.innerHTML=h})};
  var SPEC={'2.1':function(r){return{cls:'disj',rule:'zero2',blanks:[3,6],n2:[1,4]}},'2.2':function(r){return{cls:'conj',rule:'one2',blanks:[3,6],n2:[1,4]}},
    '2.3':function(r){return{cls:'mixed',rule:exPick(r,['mix','mix','any']),blanks:[3,6],n2:[1,8]}},
    '2.4':function(r){return{cls:exPick(r,['mixed','disj','conj']),rule:'any',blanks:[6,8],n2:[3,14]}},
    '2.5':function(r){return{cls:'xor',rule:exPick(r,['mix','any']),blanks:[3,7],n2:[1,10]}}};
  EXGEN[2]={no:2,name:'Таблицы истинности',types:[
    {id:'2.1',n:'Дизъюнкция',d:'Строки с F = 0'},{id:'2.2',n:'Конъюнкция',d:'Строки с F = 1'},{id:'2.3',n:'Смешанная структура',d:'Выражение со скобками'},
    {id:'2.4',n:'Мало известных клеток',d:'Много пропусков в строках'},{id:'2.5',n:'Исключающее ИЛИ',d:'Разные значения и вложенные ≡'},{id:'2.6',n:'Построить таблицу',d:'Найти 8 значений F'}],
    make:function(type,r){r=r||exRnd((Date.now()^(Math.random()*4294967296))>>>0);
      if(type==='any')type=exPick(r,['2.1','2.2','2.3','2.3','2.4','2.5','2.6']);
      if(type==='2.6'){var g=make3(r);if(!g)return null;return{q:STM3(g.text),expr:g.text,f:FM3,h:['Сколько всего наборов у трёх переменных?','Посчитай значение каждой скобки отдельно.','Запиши F сверху вниз.'],s:sol6(g.text,g.col,g.expr),a:g.answer,m:QM['2.6'],type:type}}
      var g2=makeFragment(r,SPEC[type](r));if(!g2)return null;
      return{q:STM4(g2.text),starter:st2(g2.text,g2.col),expr:g2.text,tb:{r:g2.rows.map(function(x){return x[0]}),f:g2.rows.map(function(x){return x[1]})},f:FM4,h:hints4(g2.text,g2.col,g2.rows),s:sol4(g2.text,g2.col,g2.rows,g2.answer),a:g2.answer,m:QM[type],type:type}}};
})();
