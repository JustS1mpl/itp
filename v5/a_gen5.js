/* ===================== v5.4.0: задание №5 ЕГЭ (алгоритм строит число R по записи N), генератор и разбор ===================== */
(function(){
  var LIMIT=200000;
  function bits(n){return n.toString(2)}
  function inv(s){return s.replace(/[01]/g,function(c){return c==='0'?'1':'0'})}
  function qt(s){return'«'+s+'»'}
  function cap(s){return s.charAt(0).toUpperCase()+s.slice(1)}
  function sideTxt(l,r){var p=[];if(l)p.push('слева дописывается '+qt(l));if(r)p.push('справа дописывается '+qt(r));return p.length===2?p.join(', а '):p[0]}
  var HEAD='Алгоритм получает на вход натуральное число N и строит новое число R следующим образом.\n1. Строится двоичная запись числа N.\n',TAIL='\n3. Полученная запись является двоичной записью искомого числа R.';
  function rule(kind,P){
    var R={kind:kind,P:P};
    if(kind==='A'){
      R.text=HEAD+'2. Если N чётное, то в этой записи '+sideTxt(P.el,P.er)+'; если N нечётное, то '+sideTxt(P.ol,P.orr)+'.'+TAIL;
      R.f=function(n){var b=bits(n);return parseInt(n%2===0?P.el+b+P.er:P.ol+b+P.orr,2)};
      R.trace=function(n){var b=bits(n),s=n%2===0?P.el+b+P.er:P.ol+b+P.orr;return{bin:b,branch:n%2===0?'чётное':'нечётное',step:s,R:parseInt(s,2)}};
      R.short='дописывание по чётности'}
    else if(kind==='B'){
      var cl=function(m){return Object.keys(m).map(function(k){return'каждая цифра '+qt(k)+' заменяется на '+qt(m[k])}).join(', ')};
      R.text=HEAD+'2. Если N чётное, то в записи '+cl(P.em)+'; если N нечётное, то '+cl(P.om)+'.'+TAIL;
      var ap=function(m,b){return b.split('').map(function(c){return m[c]!==undefined?m[c]:c}).join('')};
      R.f=function(n){return parseInt(ap(n%2===0?P.em:P.om,bits(n)),2)};
      R.trace=function(n){var b=bits(n),s=ap(n%2===0?P.em:P.om,b);return{bin:b,branch:n%2===0?'чётное':'нечётное',step:s,R:parseInt(s,2)}};
      R.short='замена цифр'}
    else if(kind==='C'){
      var what=P.flip?'0, если число единиц в записи нечётно, иначе 1':'1, если число единиц в записи нечётно, иначе 0',where=P.side==='r'?'справа':'слева';
      var rep={1:'',2:' Затем те же действия выполняются ещё раз для полученной записи.',3:' Затем те же действия выполняются ещё два раза (для каждой новой записи).'}[P.times];
      R.text=HEAD+'2. '+cap(where)+' к записи дописывается контрольный разряд: '+what+'.'+rep+TAIL;
      var cnt1=function(s){return s.split('1').length-1};
      R.run=function(n){var s=bits(n),seq=[];for(var i=0;i<P.times;i++){var p=String(cnt1(s)%2);if(P.flip)p=p==='0'?'1':'0';s=P.side==='r'?s+p:p+s;seq.push(s)}return{s:s,seq:seq}};
      R.f=function(n){return parseInt(R.run(n).s,2)};
      R.trace=function(n){var o=R.run(n);return{bin:bits(n),branch:'',step:o.seq.join(' → '),R:parseInt(o.s,2)}};
      R.short='контрольный разряд'}
    else if(kind==='D'){
      var wh=P.side==='r'?'справа':'слева',rp={1:'',2:' Затем с полученным числом выполняются те же действия ещё раз.'}[P.times];
      R.text=HEAD+'2. '+cap(wh)+' к записи дописывается двоичная запись остатка от деления N на '+P.k+'.'+rp+TAIL;
      R.run=function(n){var cur=n,seq=[];for(var i=0;i<P.times;i++){var r=bits(cur%P.k),s=bits(cur);s=P.side==='r'?s+r:r+s;seq.push(s+' (ост. '+(cur%P.k)+')');cur=parseInt(s,2)}return{cur:cur,seq:seq}};
      R.f=function(n){return R.run(n).cur};
      R.trace=function(n){var o=R.run(n);return{bin:bits(n),branch:'остаток '+(n%P.k),step:o.seq.join(' → '),R:o.cur}};
      R.short='остаток от деления'}
    else if(kind==='E'){
      var sd=function(x){return x==='r'?'справа':'слева'};
      R.text=HEAD+'2. Строится инверсия этой записи (все нули заменяются единицами, а единицы — нулями).\n3. Если N чётное, то инверсия дописывается к исходной записи '+sd(P.es)+'; если N нечётное, то '+(P.oextra?'в начало записи инверсии добавляется «'+P.oextra+'», после чего она дописывается '+sd(P.os_):'инверсия дописывается '+sd(P.os_))+'.\n4. Полученная запись является двоичной записью искомого числа R.';
      R.run=function(n){var b=bits(n),c=inv(b),s;if(n%2===0){s=P.es==='r'?b+c:c+b}else{c=P.oextra+c;s=P.os_==='r'?b+c:c+b}return{b:b,c:c,s:s}};
      R.f=function(n){return parseInt(R.run(n).s,2)};
      R.trace=function(n){var o=R.run(n);return{bin:o.b,branch:n%2===0?'чётное':'нечётное',step:'инверсия '+o.c+' → '+o.s,R:parseInt(o.s,2)}};
      R.short='инверсия'}
    else{
      var pairs={3:[[0,1],[1,2]],4:[[0,1],[2,3]],'-4':[[0,1],[1,2],[2,3]]}[String(P.d)],dd=Math.abs(P.d),names=['первой','второй','третьей','четвёртой'];
      var sums=pairs.map(function(p){return'сумма '+names[p[0]]+' и '+names[p[1]]+' цифр'}).join('; '),od=P.order==='asc'?'неубывания':'невозрастания',exn={3:678,4:3678,'-4':3678}[String(P.d)];
      var dg=String(exn).split('').map(Number),sv=pairs.map(function(p){return dg[p[0]]+dg[p[1]]}).sort(function(a,b){return P.order==='desc'?b-a:a-b});
      R.text='Автомат получает на вход '+dd+'-значное десятичное число N. По нему строится новое число R:\n1. Вычисляются суммы: '+sums+'.\n2. Полученные числа записываются друг за другом (без разделителей) в порядке '+od+'.\nПример. Для N = '+exn+' вычисляются суммы '+pairs.map(function(p){return dg[p[0]]+dg[p[1]]}).join(', ')+'; в порядке '+od+' получается R = '+sv.join('')+'.';
      R.domain=[Math.pow(10,dd-1),Math.pow(10,dd)-1];
      R.sm=function(n){var d=String(n).split('').map(Number),s=pairs.map(function(p){return d[p[0]]+d[p[1]]});return{sm:s,sv:s.slice().sort(function(a,b){return P.order==='desc'?b-a:a-b})}};
      R.f=function(n){return parseInt(R.sm(n).sv.join(''),10)};
      R.trace=function(n){var o=R.sm(n);return{bin:String(n),branch:'',step:'суммы '+o.sm.join(', ')+' → '+o.sv.join(''),R:R.f(n)}};
      R.short='суммы цифр'}
    return R}
  function dom(R){return R.domain||[1,LIMIT]}
  function solve(R,form,q){
    var f=R.f,d=dom(R),lo=Math.max(d[0],1),hi=d[1],n,best;
    if(form==='min_gt'){for(n=lo;n<=hi;n++)if(f(n)>q.X)return n;return null}
    if(form==='min_ge'){for(n=lo;n<=hi;n++)if(f(n)>=q.X)return n;return null}
    if(form==='max_le'){best=-1;for(n=lo;n<=q.M;n++)best=Math.max(best,f(n));return best}
    if(form==='min_eq'){for(n=lo;n<=hi;n++)if(f(n)===q.X)return n;return null}
    if(form==='max_eq'){best=null;for(n=d[0];n<=hi;n++)if(f(n)===q.X)best=n;return best}
    if(form==='count'){var S={};for(n=q.a;n<=q.b;n++)S[f(n)]=1;return Object.keys(S).length}
    if(form==='count_n'){var c=0;for(n=d[0];n<=hi;n++)if(f(n)===q.X)c++;return c}
    return null}
  function trap(R,form,q,ans){
    var f=R.f,d=dom(R),lo=Math.max(d[0],1),hi=d[1],t=null,n;
    if(form==='min_gt'){for(n=lo;n<=hi;n++)if(f(n)>=q.X){t=[n,'нестрогое неравенство вместо строгого: взяли N, для которого R = '+q.X+' (а нужно R > '+q.X+')'];break}}
    else if(form==='min_ge'){for(n=lo;n<=hi;n++)if(f(n)>q.X){t=[n,'строгое неравенство вместо нестрогого: пропустили N, для которого R = '+q.X];break}}
    else if(form==='max_le'){t=[f(q.M),'решили, что наибольшее R получается у наибольшего N = '+q.M+' (R = '+f(q.M)+'), не проверив остальные N']}
    else if(form==='min_eq'){var sols=[];for(n=lo;n<=Math.min(hi,3000);n++)if(f(n)===q.X)sols.push(n);
      var other=R.kind!=='F'?sols.filter(function(x){return x%2!==sols[0]%2}):[];
      if(other.length)t=[other[0],'нашли решение только в одной ветке (по чётности N = '+other[0]+'), не проверив другую'];
      else if(sols.length>1)t=[sols[sols.length-1],'взяли не наименьшее из подходящих N']}
    else if(form==='max_eq'){for(n=d[0];n<=hi;n++)if(f(n)===q.X){t=[n,'взяли наименьшее подходящее N вместо наибольшего'];break}}
    else if(form==='count'){t=[q.b-q.a+1,'посчитали количество чисел N ('+(q.b-q.a+1)+'), а не количество различных R']}
    if(t&&t[0]!==ans)return t;return null}
  function question(R,form,q){
    if(R.kind==='F'){
      var t={min_eq:'Укажите наименьшее число N, при вводе которого автомат выдаёт число R = '+q.X+'.',max_eq:'Укажите наибольшее число N, при вводе которого автомат выдаёт число R = '+q.X+'.',count_n:'Сколько существует чисел N, при вводе которых автомат выдаёт число R = '+q.X+'?',min_gt:'Укажите наименьшее число N, при вводе которого автомат выдаёт число R, большее '+q.X+'.'}[form];
      return t+' В ответе запишите число.'}
    return{min_gt:'Укажите минимальное число N, после обработки которого с помощью этого алгоритма получится число R, большее '+q.X+'. В ответе запишите это число N в десятичной системе счисления.',
      min_ge:'Укажите минимальное число N, после обработки которого с помощью этого алгоритма получится число R, не меньшее '+q.X+'. В ответе запишите это число N в десятичной системе счисления.',
      max_le:'Укажите максимальное число R, которое может получиться в результате работы алгоритма, если N не превосходит '+q.M+'. В ответе запишите число R в десятичной системе счисления.',
      min_eq:'Укажите наименьшее число N, при котором в результате работы алгоритма получается R = '+q.X+'. В ответе запишите число N в десятичной системе счисления.',
      count:'Сколько различных значений R может получиться, если N — натуральное число от '+q.a+' до '+q.b+' включительно? В ответе запишите количество.'}[form]}
  /* подбор параметров вопроса (порт pick_params) */
  function ri(r,a,b){return a+Math.floor(r()*(b-a+1))}
  function pick(R,form,r,level){
    var d=dom(R),q,n0,ans,tr;
    for(var it=0;it<4000;it++){
      if(R.kind==='F'){
        if(form==='min_eq'||form==='max_eq'||form==='count_n'){n0=ri(r,d[0],d[1]);q={X:R.f(n0)}}
        else if(form==='min_gt'){n0=ri(r,d[0],d[1]);q={X:R.f(n0)-exPick(r,[0,1,2])}}
        else continue}
      else if(form==='min_gt'||form==='min_ge'){n0=ri(r,6+level*4,20+level*25);q={X:R.f(n0)-(form==='min_gt'?exPick(r,[0,1,2]):0)}}
      else if(form==='max_le'){q={M:ri(r,8+level*2,14+level*4)}}
      else if(form==='min_eq'){n0=ri(r,5,40+level*40);q={X:R.f(n0)}}
      else if(form==='count'){var a=ri(r,1,6);q={a:a,b:a+ri(r,9,13+level*3)}}
      else continue;
      ans=solve(R,form,q);if(ans===null)continue;
      if(form.indexOf('min')===0&&R.kind!=='F'&&ans>400)continue;
      tr=trap(R,form,q,ans);
      if(tr===null&&form!=='count_n'&&form!=='min_eq')continue;
      return{q:q,ans:ans,trap:tr}}
    return null}
  /* разбор */
  function compact(R,ns){ns=ns.slice();if(ns.length>24)ns=ns.slice(0,5).concat([null],ns.slice(-5));return ns.map(function(n){return n===null?'…':n+'→'+R.f(n)}).join('; ')}
  function rng(a,b){var o=[];for(var i=a;i<=b;i++)o.push(i);return o}
  function row(R,n){var t=R.trace(n);return R.kind==='F'?'N = '+n+': '+t.step+' → R = '+t.R:'N = '+n+' ('+t.bin+(t.branch?', '+t.branch:'')+'): '+t.step+' → R = '+t.R}
  function sampleN(R,form,q,ans){
    if(form==='max_le'){var bn=1,bv=-1;for(var n=1;n<=q.M;n++){var v=R.f(n);if(v>bv){bv=v;bn=n}}return bn}
    if(form==='count')return q.a;
    if(R.kind==='F'){if(form!=='count_n')return ans;var d=dom(R);for(var m=d[0];m<=d[1];m++)if(R.f(m)===q.X)return m}
    return ans}
  function steps(R,form,q,ans){
    var f=R.f,d=dom(R),lo=d[0],hi=d[1],S=['Запишем алгоритм функцией f(n) (код ниже). Проверка вручную: '+row(R,sampleN(R,form,q,ans))+'.'];
    if((form==='min_gt'||form==='min_ge')&&R.kind!=='F'){
      S.push('Считаем R для N = 1, 2, 3, … до первого подходящего (N→R): '+compact(R,rng(1,ans))+'.');
      S.push('Первое N с R '+(form==='min_gt'?'>':'≥')+' '+q.X+' — N = '+ans+' (R = '+f(ans)+').');
      if(ans>1)S.push('Для предыдущего N = '+(ans-1)+' значение R = '+f(ans-1)+' — условие не выполнено.')}
    else if(form==='max_le'){var ns=rng(1,q.M),am=ns[0];ns.forEach(function(n){if(f(n)>f(am))am=n});
      S.push('Считаем R для всех N от 1 до '+q.M+' (N→R): '+compact(R,ns)+'.');S.push('Наибольшее значение R = '+ans+' получается при N = '+am+'.')}
    else if(form==='min_eq'&&R.kind!=='F'){S.push('Перебираем N = 1, 2, 3… (N→R): '+compact(R,rng(1,ans))+'.');S.push('R = '+q.X+' впервые получается при N = '+ans+'.')}
    else if(form==='count'){var nn=rng(q.a,q.b),vals=nn.map(f),dups={};vals.forEach(function(v){if(vals.filter(function(x){return x===v}).length>1)dups[v]=1});
      S.push('Считаем R для N от '+q.a+' до '+q.b+' (N→R): '+compact(R,nn)+'.');var dk=Object.keys(dups).map(Number).sort(function(a,b){return a-b});
      S.push('Повторяются значения: '+(dk.length?dk.join(', '):'повторов нет')+'.');S.push('Чисел N — '+vals.length+', различных значений R — '+ans+'.')}
    else if(R.kind==='F'){
      if(form==='min_gt'){S.push('Перебираем '+String(lo).length+'-значные числа с '+lo+': первое с R > '+q.X+' — N = '+ans+' (R = '+f(ans)+').')}
      else{var sol=[];for(var n2=lo;n2<=hi;n2++)if(f(n2)===q.X)sol.push(n2);
        S.push('Все N, при которых R = '+q.X+': '+sol.slice(0,40).join(', ')+(sol.length>40?' … (всего '+sol.length+')':' (всего '+sol.length+')')+'.');
        S.push({min_eq:'Наименьшее из них — '+sol[0]+'.',max_eq:'Наибольшее из них — '+sol[sol.length-1]+'.',count_n:'Количество таких N — '+sol.length+'.'}[form])}}
    S.push('Ответ: '+ans+'.');return S}
  function mistake(R,tr,ans){
    if(tr)return'Ошибка: '+tr[1]+'. Получается '+tr[0]+' вместо верного '+ans+'.';
    if(R.kind==='F')return'Ошибка: суммы склеили как числа (сложили) или записали в обратном порядке сортировки. Верный ответ — '+ans+'.';
    return'Ошибка: перепутаны ветки алгоритма (правило для чётных применено к нечётному N), дописали цифры не с той стороны или оставили результат в двоичной записи. Верный ответ — '+ans+'.'}
  var RH={A:'Две ветки: для чётного N цифры дописываются одним способом, для нечётного другим. Запиши их через if n % 2 == 0 и склей строки знаком +.',
    B:'Замены удобно хранить словарём m и применять так: "".join(m.get(c, c) for c in b). Цифры, которых в словаре нет, остаются как были.',
    C:'Контрольный разряд: p = str(s.count("1") % 2). Если в условии он инвертирован, замени 0 на 1 и наоборот. Дописывай его столько раз, сколько сказано.',
    D:'Остаток в двоичной записи: bin(n % k)[2:]. Для остатка 0 получится "0", это нормально. Если действия повторяются, повторяй их уже для нового числа.',
    E:'Инверсия записи: c = "".join("1" if x == "0" else "0" for x in b). Потом склей b и c в нужном порядке, как сказано для чётных и нечётных N.',
    F:'Разбей число на цифры: d = [int(c) for c in str(n)]. Найди суммы по условию, отсортируй их (reverse=True для невозрастания) и склей без разделителей.'};
  function hints(R,form){
    var h=[RH[R.kind]];
    h.push(form==='max_le'?'Найди R для всех N от 1 до M и возьми наибольшее: max(f(n) for n in range(1, M + 1)). Наибольшее R не обязано быть у наибольшего N.':form==='count'?'Собери все R для N из диапазона в множество {f(n) for n in range(a, b + 1)}: одинаковые значения встретятся один раз. Ответ len(множества).':R.kind==='F'?'Переберись все N нужной разрядности по порядку и выбери подходящие: наименьшее, наибольшее или посчитай их количество.':'Перебирай N = 1, 2, 3, … и считай R для каждого. Для минимального N останавливайся на первом подходящем (цикл while).');
    h.push('Проверь f(n) вручную для двух небольших N. '+(form==='min_gt'?'Слово «большее» значит строго >.':form==='min_ge'?'Слова «не меньшее» значат >=.':'Ещё раз прочитай последнюю фразу: что спрашивают, N или R.'));
    return h}
  function starter(R){
    if(R.kind==='F')return'def f(n):\n    d = [int(c) for c in str(n)]    # цифры числа N\n    # найди суммы цифр, отсортируй и склей\n    return int(...)\n\n';
    if(R.kind==='C'||R.kind==='D')return'def f(n):\n    s = bin(n)[2:]    # двоичная запись N\n    # допиши нужное по условию\n    return int(s, 2)\n\n';
    return'def f(n):\n    b = bin(n)[2:]    # двоичная запись N\n    # построй s по условию (ветки по n % 2)\n    return int(s, 2)\n\n'}
  function fill(q){
    var Q=q.query,R=rule(Q.rule,Q.params),ans=solve(R,Q.form,Q.q),tr=trap(R,Q.form,Q.q,ans),L=R.text.split('\n');
    q._v=String(ans);q.pr=R.text;q.q='';q.qq=question(R,Q.form,Q.q);q.pl='Условие';
    if(!q.s)q.s=steps(R,Q.form,Q.q,ans);if(!q.h)q.h=hints(R,Q.form);if(!q.m)q.m=mistake(R,tr,ans);if(!q.starter)q.starter=starter(R);
    q.f='Одно целое число в десятичной системе.';
    return q}
  window.exFill5=fill;
  window.ex5={rule:rule,solve:solve,trap:trap,question:question,pick:pick,steps:steps,hints:hints};
  /* ---------- генератор ---------- */
  var BPOOL=[[{'1':'11'},{'0':'00'}],[{'0':'00'},{'1':'10'}],[{'1':'10'},{'0':'01'}],[{'0':'01'},{'1':'11'}],[{'1':'00'},{'0':'11'}],[{'0':'11'},{'1':'01'}]];
  var LS=['','1','10','11','01'],RS=['','0','1','01','10'];
  function ruleFor(r,t){
    if(t==='5.1'||t==='5.7a'){for(var i=0;i<100;i++){var P={el:exPick(r,LS),er:exPick(r,RS),ol:exPick(r,LS),orr:exPick(r,RS)};if(!(P.el||P.er)||!(P.ol||P.orr))continue;if(P.el===P.ol&&P.er===P.orr)continue;if(P.er&&P.er===P.orr&&!P.el&&!P.ol)continue;return rule('A',P)}}
    if(t==='5.2'){var b=exPick(r,BPOOL);return rule('B',{em:b[0],om:b[1]})}
    if(t==='5.3'||t==='5.7c')return rule('C',{side:exPick(r,['r','l']),times:exPick(r,[1,2,3]),flip:r()<.5});
    if(t==='5.4'||t==='5.7d')return rule('D',{k:exPick(r,[3,4,5,6,7]),side:exPick(r,['r','l']),times:exPick(r,[1,2])});
    if(t==='5.5'||t==='5.7e')return rule('E',{es:exPick(r,['r','l']),os_:exPick(r,['r','l']),oextra:exPick(r,['','','1'])});
    if(t==='5.6')return rule('F',{d:exPick(r,[3,4,-4]),order:exPick(r,['asc','desc'])});
    return null}
  EXGEN[5]={no:5,name:'Алгоритм строит число R',types:[{id:'5.1',n:'Дописывание цифр',d:'Слева и справа по чётности'},{id:'5.2',n:'Замена цифр',d:'Каждая цифра по правилу'},{id:'5.3',n:'Контрольный разряд',d:'Бит чётности'},{id:'5.4',n:'Остаток от деления',d:'Дописывается остаток'},{id:'5.5',n:'Инверсия записи',d:'Нули в единицы и наоборот'},{id:'5.6',n:'Суммы цифр',d:'Десятичное число и сортировка'},{id:'5.7',n:'Сколько различных R',d:'Множество значений'}],
    make:function(type,r){r=r||exRnd((Date.now()^(Math.random()*4294967296))>>>0);if(type==='any')type=exPick(r,['5.1','5.1','5.2','5.3','5.4','5.5','5.6','5.7']);
      for(var at=0;at<30;at++){
        var t=type,R,form;
        if(type==='5.7'){t=exPick(r,['5.7a','5.7c','5.7d','5.7e']);form='count'}
        else if(type==='5.6')form=exPick(r,['min_eq','max_eq','count_n','min_gt']);
        else form=exPick(r,['min_gt','min_gt','min_ge','max_le','max_le','min_eq']);
        R=ruleFor(r,t);if(!R)return null;
        var pk=pick(R,form,r,exPick(r,[0,1,2]));if(!pk)continue;
        var q={query:{rule:R.kind,params:R.P,form:form,q:pk.q},type:type};fill(q);q.a=q._v;return q}
      return null}};
})();
