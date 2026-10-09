/* ===================== v5.4.0: задание №6 ЕГЭ (Черепаха и Чертёжник), генератор и разбор ===================== */
(function(){
  var K=Math.PI/180;
  function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){var t=a%b;a=b;b=t}return a}
  function pl(n,a){var m=n%10,h=n%100;return n+' '+(m===1&&h!==11?a[0]:m>=2&&m<=4&&(h<10||h>=20)?a[1]:a[2])}
  function f2(v){var s=(Math.round(v*100)/100).toFixed(2);if(s==='-0.00')s='0.00';return s.replace(/\.00$/,'')}
  function sgn(v){return v<0?'−'+f2(-v):f2(v)}
  /* ---------- исполнение программы Черепахи ---------- */
  function runT(prog){
    var x=0,y=0,ang=90,down=true,lines=[[[0,0]]];
    (function ex(p){p.forEach(function(c){
      if(c[0]==='rep'){for(var i=0;i<c[1];i++)ex(c[2])}
      else if(c[0]==='F'){x+=c[1]*Math.cos(ang*K);y+=c[1]*Math.sin(ang*K);if(down)lines[lines.length-1].push([x,y])}
      else if(c[0]==='R')ang-=c[1];else if(c[0]==='L')ang+=c[1];
      else if(c[0]==='up')down=false;else{down=true;lines.push([[x,y]])}})})(prog);
    return{lines:lines,x:x,y:y,ang:ang}}
  function polygon(l){for(var i=1;i<l.length;i++)if(Math.abs(l[i][0]-l[0][0])<1e-7&&Math.abs(l[i][1]-l[0][1])<1e-7)return l.slice(0,i);return null}
  function polysOf(prog){var R=runT(prog),o=[];R.lines.forEach(function(l){if(l.length>2)o.push(polygon(l))});return o}
  function onEdge(px,py,P){for(var i=0;i<P.length;i++){var a=P[i],b=P[(i+1)%P.length],dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((px-a[0])*dx+(py-a[1])*dy)/(dx*dx+dy*dy))),ex=px-a[0]-t*dx,ey=py-a[1]-t*dy;if(ex*ex+ey*ey<1e-12)return true}return false}
  function inside(px,py,P){var r=false;for(var i=0;i<P.length;i++){var a=P[i],b=P[(i+1)%P.length];if((a[1]>py)!==(b[1]>py)&&px<a[0]+(py-a[1])*(b[0]-a[0])/(b[1]-a[1]))r=!r}return r}
  function member(px,py,P,strict){var e=onEdge(px,py,P),i=inside(px,py,P);return strict?(i&&!e):(i||e)}
  function bounds(polys){var a=[1e9,1e9,-1e9,-1e9];polys.forEach(function(P){P.forEach(function(p){a[0]=Math.min(a[0],p[0]);a[1]=Math.min(a[1],p[1]);a[2]=Math.max(a[2],p[0]);a[3]=Math.max(a[3],p[1])})});return[Math.floor(a[0])-1,Math.floor(a[1])-1,Math.ceil(a[2])+1,Math.ceil(a[3])+1]}
  function rows(polys,mode,strict){ // mode: one | union | inter ; возвращает [[y,[x...]],...]
    var B=bounds(polys),o=[];
    for(var Y=B[3];Y>=B[1];Y--){var xs=[];
      for(var X=B[0];X<=B[2];X++){
        var m=mode==='inter'?polys.every(function(P){return member(X,Y,P,strict)}):mode==='union'?polys.some(function(P){return member(X,Y,P,strict)}):member(X,Y,polys[0],strict);
        if(m)xs.push(X)}
      if(xs.length)o.push([Y,xs])}
    return o}
  function cnt(rs){return rs.reduce(function(a,r){return a+r[1].length},0)}
  function runsOf(xs){var o=[],s=xs[0],p=xs[0];for(var i=1;i<=xs.length;i++){if(i<xs.length&&xs[i]===p+1){p=xs[i];continue}o.push([s,p]);s=xs[i];p=xs[i]}return o}
  function runTxt(xs){return runsOf(xs).map(function(r){return r[0]===r[1]?'x = '+r[0]:'x от '+r[0]+' до '+r[1]}).join(', ')}
  function rowSteps(rs){ // сжимаем одинаковые подряд идущие строки
    var out=[],i=0;
    while(i<rs.length){var t=runTxt(rs[i][1]),n=rs[i][1].length,j=i;while(j+1<rs.length&&rs[j+1][0]===rs[j][0]-1&&runTxt(rs[j+1][1])===t)j++;
      if(j>i)out.push('y от '+rs[j][0]+' до '+rs[i][0]+' ('+pl(j-i+1,['строка','строки','строк'])+'): '+t+' → по '+n+' в каждой, всего '+n*(j-i+1));
      else out.push('y = '+rs[i][0]+': '+t+' → '+n);
      i=j+1}
    return out}
  /* ---------- Чертёжник ---------- */
  function drawPts(moves,k){
    var x=0,y=0,S={'0,0':1},v=[[0,0]];
    for(var r=0;r<k;r++)moves.forEach(function(m){var g=gcd(m[0],m[1]);for(var t=1;t<=g;t++)S[(x+m[0]*t/g)+','+(y+m[1]*t/g)]=1;x+=m[0];y+=m[1]});
    return Object.keys(S).length}
  function drawPoly(moves){var x=0,y=0,P=[[0,0]];moves.forEach(function(m,i){x+=m[0];y+=m[1];if(i<moves.length-1)P.push([x,y])});return P}
  function area2(P){var s=0;for(var i=0;i<P.length;i++){var a=P[i],b=P[(i+1)%P.length];s+=a[0]*b[1]-b[0]*a[1]}return Math.abs(s)}
  function pick(moves){var P=drawPoly(moves),S2=area2(P),B=moves.reduce(function(a,m){return a+gcd(m[0],m[1])},0);return{P:P,S2:S2,B:B,I:(S2-B+2)/2}}
  function segX(a,b,c,d){function o(p,q,r){var v=(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]);return v>0?1:v<0?-1:0}
    var o1=o(a,b,c),o2=o(a,b,d),o3=o(c,d,a),o4=o(c,d,b);if(o1*o2<0&&o3*o4<0)return true;
    function on(p,q,r){return Math.min(p[0],q[0])<=r[0]&&r[0]<=Math.max(p[0],q[0])&&Math.min(p[1],q[1])<=r[1]&&r[1]<=Math.max(p[1],q[1])}
    return(o1===0&&on(a,b,c))||(o2===0&&on(a,b,d))||(o3===0&&on(c,d,a))||(o4===0&&on(c,d,b))}
  function simple(P){var n=P.length;for(var i=0;i<n;i++)for(var j=i+1;j<n;j++){if(j===i+1||(i===0&&j===n-1))continue;if(segX(P[i],P[(i+1)%n],P[j],P[(j+1)%n]))return false}return true}
  /* ---------- прямоугольники ---------- */
  function box(l){var xs=l.map(function(p){return Math.round(p[0])}),ys=l.map(function(p){return Math.round(p[1])});return[Math.min.apply(null,xs),Math.max.apply(null,xs),Math.min.apply(null,ys),Math.max.apply(null,ys)]}
  function inter(prog){var L=runT(prog).lines,a=box(L[0]),b=box(L[1]);return{a:a,b:b,w:Math.min(a[1],b[1])-Math.max(a[0],b[0]),h:Math.min(a[3],b[3])-Math.max(a[2],b[2]),x0:Math.max(a[0],b[0]),x1:Math.min(a[1],b[1]),y0:Math.max(a[2],b[2]),y1:Math.min(a[3],b[3])}}
  /* ---------- запись на языке задания ---------- */
  var CN={F:'Вперёд',R:'Направо',L:'Налево'};
  function cmd(c){return c[0]==='up'?'Поднять хвост':c[0]==='down'?'Опустить хвост':CN[c[0]]+' '+c[1]}
  function progText(prog){var o=[],cur=[];
    function fl(){if(cur.length)o.push(cur.join(' '));cur=[]}
    prog.forEach(function(c){if(c[0]==='rep'){fl();o.push('Повтори '+c[1]+' ['+c[2].map(cmd).join(' ')+']')}else cur.push(cmd(c))});
    fl();return o.join('\n')}
  function moveText(moves,k){return'Повтори '+k+' раз\n'+moves.map(function(m){return'    Сместиться на ('+m[0]+', '+m[1]+')'}).join('\n')+'\nКонец'}
  var INTRO_T='Исполнитель Черепаха действует на плоскости с декартовой системой координат. В начальный момент Черепаха находится в начале координат, её голова направлена вдоль положительного направления оси ординат, хвост опущен. При опущенном хвосте за Черепахой остаётся след. Черепаха может выполнять команды: Вперёд n (n — целое число) — передвижение на n единиц в том направлении, куда указывает голова; Направо m (m — целое число) — изменение направления на m градусов по часовой стрелке; Налево m — изменение направления на m градусов против часовой стрелки. Команды Поднять хвост (Черепаха перемещается, не оставляя следа) и Опустить хвост. Запись Повтори k [Команда1 Команда2 … КомандаS] означает, что последовательность команд в скобках повторится k раз. Черепахе был дан для исполнения следующий алгоритм:';
  var INTRO_D='Исполнитель Чертёжник перемещается на координатной плоскости, оставляя след в виде линии. Чертёжник может выполнять команду Сместиться на (a, b) (a, b — целые числа), перемещающую его из точки (x, y) в точку (x + a, y + b). Запись Повтори k раз … Конец означает, что команды между словами повторяются k раз. В начале исполнения Чертёжник находится в начале координат. Дан алгоритм:';
  var QS={strict:'Какое количество точек с целочисленными координатами будет находиться внутри области, ограниченной линией, заданной данным алгоритмом? Точки на линии учитывать не следует. В ответе запишите число.',
    incl:'Какое количество точек с целочисленными координатами будет находиться внутри области, ограниченной линией, заданной данным алгоритмом, включая точки на самой линии? В ответе запишите число.',
    union_incl:'Определите количество точек с целочисленными координатами, которые находятся внутри объединения фигур, ограниченных заданными линиями, включая точки на границах. В ответе запишите число.',
    union_strict:'Определите количество точек с целочисленными координатами, которые находятся внутри объединения фигур, ограниченных заданными линиями. Точки на границах учитывать не следует. В ответе запишите число.',
    inter_incl:'Определите количество точек с целочисленными координатами, которые находятся внутри пересечения фигур, ограниченных заданными линиями, включая точки на границах. В ответе запишите число.',
    inter_strict:'Определите количество точек с целочисленными координатами, которые находятся внутри пересечения фигур, ограниченных заданными линиями. Точки на границах учитывать не следует. В ответе запишите число.',
    perim:'Определите периметр области пересечения фигур, ограниченных заданными линиями. В ответе запишите число.',
    area:'Определите площадь области пересечения фигур, ограниченных заданными линиями. В ответе запишите число.',
    traj:'Сколько точек с целочисленными координатами лежит на траектории Чертёжника (начальную точку учитывать)? В ответе запишите число.',
    inside:'Сколько точек с целочисленными координатами находится строго внутри области, ограниченной линией, которую оставляет Чертёжник? Точки на линии учитывать не следует. В ответе запишите число.'};
  /* ---------- запись на Python (Черепаха) ---------- */
  function pyProg(prog,ind,sp){var o=[],p=ind;
    prog.forEach(function(c){
      if(c[0]==='rep'){o.push(p+'for _ in range('+c[1]+'):');o=o.concat(pyProg(c[2],ind+'    '))}
      else o.push(p+({F:'forward('+c[1]+')',R:'right('+c[1]+')',L:'left('+c[1]+')',up:'penup()',down:'pendown()'}[c[0]]))});
    return o}
  function pyTurtle(Q){
    if(Q.kind==='D')return'from turtle import *\n\nfor _ in range('+Q.k+'):\n    for a, b in '+JSON.stringify(Q.moves).replace(/\[(-?\d+),(-?\d+)\]/g,'($1, $2)').replace(/,\(/g,', (')+':\n        goto(xcor() + a, ycor() + b)\n';
    return'from turtle import *\n\nleft(90)  # в условии голова смотрит вверх, а в Python по умолчанию вправо\n'+pyProg(Q.prog,'').join('\n')+'\n'}
  /* ---------- решение одного задания ---------- */
  function solve(Q){
    var I={Q:Q,kind:Q.kind,form:Q.form};
    if(Q.kind==='T'){
      var polys=polysOf(Q.prog),f=Q.form,two=/^(union|inter)/.test(f),strict=/strict$/.test(f)||f==='strict',mode=two?(/^union/.test(f)?'union':'inter'):'one';
      I.polys=polys;I.strict=strict;I.mode=mode;I.rs=rows(polys,mode,strict);I.answer=cnt(I.rs);
      I.rsAlt=rows(polys,mode,!strict);I.alt=cnt(I.rsAlt);
      if(two){I.each=polys.map(function(P){return cnt(rows([P],'one',strict))});I.sum=I.each.reduce(function(a,b){return a+b},0);I.other=cnt(rows(polys,mode==='union'?'inter':'union',strict))}}
    else if(Q.kind==='R'){var r=inter(Q.prog);I.r=r;I.answer=Q.form==='perim'?2*(r.w+r.h):r.w*r.h}
    else{I.answer=Q.form==='traj'?drawPts(Q.moves,Q.k):pick(Q.moves).I;
      if(Q.form==='traj'){I.ends=Q.moves.length*Q.k+1}else{I.pk=pick(Q.moves)}}
    return I}
  function polyTxt(P,n){return P.map(function(p){return'('+f2(p[0])+'; '+f2(p[1])+')'}).join(', ')}
  function steps(I){
    var Q=I.Q,S=[];
    if(Q.kind==='T'){
      S.push('Исполняем программу. Старт (0, 0), голова вверх (угол 90°). «Вперёд n»: x += n·cos α, y += n·sin α. «Направо m» уменьшает угол α на m, «Налево m» увеличивает. Повторы после замыкания идут по уже нарисованному следу.');
      I.polys.forEach(function(P,i){S.push((I.polys.length>1?'Фигура '+(i+1)+', ':'Фигура, ')+'вершины: '+polyTxt(P)+'.')});
      if(I.polys.length>1)S.push('Хвост между фигурами поднят: Черепаха сдвигается и поворачивается, но не рисует, поэтому вторая фигура начинается с нового места.');
      var what=I.mode==='union'?'в объединении':I.mode==='inter'?'в пересечении':'внутри фигуры';
      S.push('Считаем целые точки '+what+' ('+(I.strict?'линия не входит':'линия входит')+') по строкам:');
      S=S.concat(rowSteps(I.rs));
      S.push('Сумма по строкам: '+I.answer+'.')}
    else if(Q.kind==='R'){var r=I.r;
      S.push('Повторы идут по следу, поэтому каждая фигура — прямоугольник. Исполняем программу и берём границы по x и y.');
      S.push('Прямоугольник 1: x от '+r.a[0]+' до '+r.a[1]+', y от '+r.a[2]+' до '+r.a[3]+'.');
      S.push('Прямоугольник 2: x от '+r.b[0]+' до '+r.b[1]+', y от '+r.b[2]+' до '+r.b[3]+'.');
      S.push('Пересечение: x от max('+r.a[0]+', '+r.b[0]+') = '+r.x0+' до min('+r.a[1]+', '+r.b[1]+') = '+r.x1+'; y от max('+r.a[2]+', '+r.b[2]+') = '+r.y0+' до min('+r.a[3]+', '+r.b[3]+') = '+r.y1+'.');
      S.push('Размеры общей части: '+r.w+' × '+r.h+'. '+(Q.form==='perim'?'Периметр 2·('+r.w+' + '+r.h+') = '+I.answer+'.':'Площадь '+r.w+'·'+r.h+' = '+I.answer+'.'))}
    else if(Q.form==='traj'){
      var x=0,y=0;S.push('Алгоритм из '+Q.moves.length+' '+(Q.moves.length<5?'перемещений':'перемещений')+' повторяется '+Q.k+' раз. На перемещении (a, b) лежат НОД(|a|, |b|) целых точек, считая конец и не считая начало.');
      Q.moves.forEach(function(m){var g=gcd(m[0],m[1]);S.push('Сместиться на ('+m[0]+', '+m[1]+'): из ('+x+', '+y+') в ('+(x+m[0])+', '+(y+m[1])+'); НОД('+Math.abs(m[0])+', '+Math.abs(m[1])+') = '+g+' → '+pl(g,['точка','точки','точек'])+'.');x+=m[0];y+=m[1]});
      S.push('Один проход сдвигает Черепаху на ('+x+', '+y+'). Точки складываем в множество: совпавшие при повторах считаются один раз. Вместе с начальной точкой различных точек: '+I.answer+'.')}
    else{var pk=I.pk;
      S.push('Сумма перемещений равна (0, 0): путь замкнут, повторы идут по тому же следу. Вершины: '+pk.P.map(function(p){return'('+p[0]+', '+p[1]+')'}).join(', ')+'.');
      S.push('Удвоенная площадь по формуле шнурка: 2S = '+pk.S2+', S = '+(pk.S2/2)+'.');
      S.push('Точки на линии: B = сумма НОД по сторонам = '+pk.B+'.');
      S.push('Формула Пика: I = S − B/2 + 1 = '+(pk.S2/2)+' − '+(pk.B/2)+' + 1 = '+pk.I+'.')}
    return S}
  function hints(I){var Q=I.Q,f=Q.form;
    if(Q.kind==='D'&&f==='traj')return['Для каждого перемещения (a, b) найди НОД(|a|, |b|): столько целых точек лежит на отрезке (конец считаем, начало нет).','Один проход сдвигает Чертёжника на сумму всех (a, b). Выпиши точки первых проходов и посмотри, повторяются ли они.','Совпавшие точки считаются один раз. Не забудь прибавить начальную точку (0, 0).'];
    if(Q.kind==='D')return['Найди вершины: последовательно прибавляй (a, b), пока не вернёшься в (0, 0).','Площадь по формуле шнурка: 2S = |Σ(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|. Точки на линии B = сумма НОД по сторонам.','Формула Пика: I = S − B/2 + 1. Это число внутренних точек.'];
    if(Q.kind==='R')return['Повторы идут по следу, поэтому каждая фигура — прямоугольник. Исполни программу и выпиши границы по x и y.','Пересечение: левая граница = большая из левых, правая = меньшая из правых. Так же по y.','Размеры общей части w и h. '+(f==='perim'?'Периметр равен 2·(w + h), а не w + h.':'Площадь равна w·h.')+' Кнопка «🐢» нарисует оба прямоугольника.'];
    var h=['Исполни программу: старт (0, 0), голова вверх, «Направо» уменьшает угол. Найди вершины каждой фигуры (до первого возврата в начало).'];
    h.push(/^union/.test(f)?'Считай по строкам: для каждого целого y выпиши целые x, которые лежат хотя бы в одной фигуре. Общие точки считай один раз.':/^inter/.test(f)?'Считай по строкам: для каждого целого y выпиши целые x, которые лежат в обеих фигурах сразу.':'Считай по строкам: для каждого целого y выпиши целые x между левой и правой сторонами.');
    h.push((/strict$/.test(f)||f==='strict'?'Точки на линии не считаем.':'Точки на линии считаем.')+' Кнопка «🐢» нарисует фигуры: включи «Точки» и «Отмечать», чтобы пересчитать на рисунке.');
    return h}
  function mistake(I){var Q=I.Q,f=Q.form;
    if(Q.kind==='T'){
      if(I.mode==='union'&&I.sum!==I.answer)return'Складывают количества точек двух фигур, и общие точки считаются дважды: получается '+I.sum+' вместо '+I.answer+'.';
      if(I.mode==='inter'&&I.other!==I.answer)return'Считают объединение вместо пересечения: получается '+I.other+' вместо '+I.answer+'.';
      if(I.alt!==I.answer)return I.strict?'Считают и точки на линии, а их учитывать не следует: получается '+I.alt+' вместо '+I.answer+'.':'Забывают точки на линии, а их нужно учитывать: получается '+I.alt+' вместо '+I.answer+'.';
      return'Путают направление поворота («Направо» уменьшает угол) или считают, что голова смотрит вправо, а не вверх.'}
    if(Q.kind==='R')return f==='perim'?'Записывают полупериметр w + h = '+(I.r.w+I.r.h)+' вместо 2·(w + h) = '+I.answer+'.':'Берут периметр '+2*(I.r.w+I.r.h)+' вместо площади '+I.answer+'.';
    if(f==='traj')return'Считают только концы перемещений ('+I.ends+') и забывают промежуточные целые точки на отрезках. Верный ответ '+I.answer+'.';
    return'Находят площадь (S = '+(I.pk.S2/2)+') вместо числа внутренних точек: верный ответ '+I.answer+'.'}
  function alt(I){var Q=I.Q;
    if(Q.kind==='T')return'Руками: найти вершины (cos/sin), для каждой целой строки y записать диапазон x и сложить. Программой: та же проверка «внутри» и «на линии» для каждой целой точки (урок «Считаем точки программой»).';
    if(Q.kind==='R')return'Нарисуй оба прямоугольника на клетчатой бумаге, найди общую часть и сложи её стороны.';
    return Q.form==='traj'?'Программой: в цикле добавлять в множество все точки каждого отрезка и вывести len(множества).':'Можно пересчитать точки по строкам, но формула Пика быстрее.'}
  /* ---------- сборка полей задания ---------- */
  function fill(q){
    var Q=q.query,I=solve(Q);q._v=String(I.answer);
    if(Q.kind==='D'){q.q=INTRO_D;q.pr=moveText(Q.moves,Q.k)}else{q.q=INTRO_T;q.pr=progText(Q.prog)}
    q.qq=QS[Q.form];
    if(!q.s)q.s=steps(I);if(!q.h)q.h=hints(I);if(!q.m)q.m=mistake(I);if(!q.alt)q.alt=alt(I);
    q.tu=pyTurtle(Q);if(!q.starter)q.starter=q.tu;
    q.f='Одно целое число.';
    return q}
  window.exFill6=fill;
  window.ex6={solve:solve,runT:runT,polysOf:polysOf,drawPts:drawPts,pick:pick,inter:inter,pyTurtle:pyTurtle,progText:progText,QS:QS};
  /* ---------- генератор ---------- */
  function R(r,a,b){return a+Math.floor(r()*(b-a+1))}
  function shape(r,kind){
    if(kind==='rect'){var a=R(r,3,14),b=R(r,3,14);if(a===b)b=a+R(r,1,3);return[['rep',exPick(r,[2,3,4,5,6,9]),[['F',a],['R',90],['F',b],['R',90]]]]}
    if(kind==='sq')return[['rep',exPick(r,[4,5,8]),[['F',R(r,4,12)],['R',90]]]];
    if(kind==='tri')return[['rep',exPick(r,[3,4,5,7]),[['F',R(r,5,14)],['R',120]]]];
    if(kind==='hex')return[['rep',exPick(r,[6,7,8,13]),[['F',R(r,3,7)],['R',60]]]];
    if(kind==='par60')return[['rep',exPick(r,[2,3,4]),[['F',R(r,4,10)],['R',60],['F',R(r,4,10)],['R',120]]]];
    if(kind==='par120')return[['rep',exPick(r,[2,3,4]),[['F',R(r,4,10)],['R',120],['F',R(r,4,10)],['R',60]]]];
    if(kind==='par45')return[['rep',exPick(r,[2,3,5,7]),[['F',R(r,6,12)],['R',45],['F',R(r,5,9)],['R',135]]]]}
  var K1=['rect','sq','tri','hex','par60','par120','par45'];
  function oneFig(r,hard){return shape(r,exPick(r,hard?K1:['rect','sq','tri','hex','par60','par45','tri']))}
  function twoFig(r,easyBoth){
    var k1=exPick(r,easyBoth?['rect','sq']:K1),k2=exPick(r,easyBoth?['rect','sq']:K1);
    var mv=[['up'],['F',R(r,1,6)],[exPick(r,['L','R']),90],['F',R(r,1,6)],[null,90],['down']];
    mv[4][0]=mv[2][0]==='L'?'R':'L';
    return shape(r,k1).concat(mv,shape(r,k2))}
  function genT(r,type){
    var forms={'6.1':['strict'],'6.2':['incl'],'6.3':['union_incl','union_strict'],'6.4':['inter_incl','inter_strict']}[type];
    for(var at=0;at<600;at++){
      var f=exPick(r,forms),prog=(type==='6.1'||type==='6.2')?oneFig(r,at>200):twoFig(r,at>400),Q={kind:'T',form:f,prog:prog},P;
      try{P=polysOf(prog)}catch(e){continue}
      if(!P||P.length!==(type<'6.3'?1:2))continue;
      var bad=false;P.forEach(function(p){if(!p||p.length<3||area2(p)<2)bad=true});if(bad)continue;
      var I=solve(Q);
      var lo=type==='6.3'?30:type==='6.4'?3:8,hi=type==='6.3'?160:type==='6.4'?45:110;
      if(I.answer<lo||I.answer>hi)continue;
      if(type==='6.3'&&I.sum===I.answer)continue;
      if(type==='6.4'&&I.other===I.answer)continue;
      if(I.alt===I.answer&&type<'6.3')continue;
      return Q}
    return null}
  function genR(r){
    for(var at=0;at<600;at++){
      var a=R(r,3,12),b=R(r,3,12),c=R(r,3,12),d=R(r,3,12),k1=exPick(r,[2,3,5,9]),k2=exPick(r,[2,4,5,6]);
      var mv=[['up'],['F',R(r,1,8)],[exPick(r,['R','R','L']),90],['F',R(r,1,8)],[null,90],['down']];mv[4][0]=mv[2][0]==='L'?'R':'L';
      var prog=[['rep',k1,[['F',a],['R',90],['F',b],['R',90]]]].concat(mv,[['rep',k2,[['F',c],['R',90],['F',d],['R',90]]]]),Q={kind:'R',form:exPick(r,['perim','area']),prog:prog},I;
      try{I=solve(Q)}catch(e){continue}
      if(I.r.w<1||I.r.h<1||I.answer<4||I.answer>70)continue;
      return Q}
    return null}
  function genD(r,type){
    for(var at=0;at<800;at++){
      var n=R(r,3,4),mv=[],sx=0,sy=0,Q;
      for(var i=0;i<n-(type==='6.6i'?1:0);i++){var a=R(r,-9,9),b=R(r,-9,9);if(!a&&!b)a=3;mv.push([a,b]);sx+=a;sy+=b}
      if(type==='6.6i'){if(!sx&&!sy)continue;if(Math.abs(sx)>9||Math.abs(sy)>9)continue;mv.push([-sx,-sy]);var P=drawPoly(mv);if(!simple(P))continue;var pk=pick(mv);if(pk.S2<8||pk.I<3||pk.I>40)continue;
        if(mv.some(function(m){return !m[0]&&!m[1]}))continue;Q={kind:'D',form:'inside',moves:mv,k:R(r,2,5)}}
      else{var k=R(r,3,9);Q={kind:'D',form:'traj',moves:mv,k:k};var I=drawPts(mv,k);if(I<15||I>160)continue}
      return Q}
    return null}
  EXGEN[6]={no:6,name:'Исполнитель Черепаха',types:[{id:'6.1',n:'Внутри фигуры, линия не входит',d:'Одна замкнутая линия'},{id:'6.2',n:'Внутри фигуры, линия входит',d:'Включая точки на линии'},{id:'6.3',n:'Объединение двух фигур',d:'Общие точки один раз'},{id:'6.4',n:'Пересечение двух фигур',d:'Точки в обеих сразу'},{id:'6.5',n:'Периметр или площадь пересечения',d:'Два прямоугольника'},{id:'6.6',n:'Чертёжник',d:'Траектория и формула Пика'}],
    make:function(type,r){r=r||exRnd((Date.now()^(Math.random()*4294967296))>>>0);if(type==='any')type=exPick(r,['6.1','6.2','6.3','6.3','6.4','6.4','6.5','6.6']);
      var Q=type==='6.5'?genR(r):type==='6.6'?genD(r,r()<.4?'6.6i':'6.6'):genT(r,type);if(!Q)return null;
      var q={query:Q,type:type};fill(q);q.a=q._v;return q}};
})();
