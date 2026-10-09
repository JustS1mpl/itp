/* ===================== v5.1.3: задание №4 ЕГЭ (неравномерные коды, условие Фано), генератор и разбор ===================== */
(function(){
  var RU='АБВГДЕЖЗИК'.split(''),LAT='ABCDEFGHIJ'.split(''),WORDS=['ПРОГРАММА','ИНФОРМАТИКА','АЛГОРИТМ','КОМПЬЮТЕР','ПЕРЕМЕННАЯ','ТРАНСЛЯТОР','МАССИВ','КОНСТАНТА','ПРОЦЕДУРА','БИБЛИОТЕКА'];
  function fanoOk(ws,rev){
    for(var i=0;i<ws.length;i++)for(var j=0;j<ws.length;j++){if(i===j)continue;var a=ws[i],b=ws[j];
      if(a===b)return false;if(rev?b.slice(-a.length)===a&&b.length>=a.length:b.indexOf(a)===0)return false}
    return true}
  function allWords(L){var o=[];for(var i=0;i<(1<<L);i++){var s=i.toString(2);while(s.length<L)s='0'+s;o.push(s)}return o}
  function freeWords(fx,L,rev){return allWords(L).filter(function(w){return fanoOk(fx.concat([w]),rev)})}
  function shortest(fx,rev){for(var L=1;L<=10;L++){var f=freeWords(fx,L,rev);if(f.length)return f[0]}return null}
  function equalLen(fx,k){for(var L=1;L<12;L++)if(freeWords(fx,L,false).length>=k){var s=0;fx.forEach(function(w){s+=w.length});return[L,s+k*L]}return null}
  function minExtra(fx,k,maxlen){maxlen=maxlen||7;var pool=[];for(var L=1;L<=maxlen;L++)pool=pool.concat(freeWords(fx,L,false));
    var best=[1e9,null];
    (function rec(st,ch,tot){
      if(ch.length===k){if(tot<best[0]){best[0]=tot;best[1]=ch.slice()}return}
      var need=k-ch.length;
      for(var i=st;i<pool.length;i++){var w=pool[i];if(tot+w.length*need>=best[0])break;
        if(ch.every(function(c){return fanoOk([w,c],false)})){ch.push(w);rec(i+1,ch,tot+w.length);ch.pop()}}})(0,[],0);
    return best}
  function shortenOpts(code){var r=[];Object.keys(code).forEach(function(ch){var w=code[ch];if(w.length<2)return;var n={};Object.keys(code).forEach(function(c){n[c]=code[c]});n[ch]=w.slice(0,-1);if(fanoOk(Object.keys(n).map(function(c){return n[c]}),false))r.push([ch,w.slice(0,-1)])});return r}
  function encode(msg,code){return msg.split('').map(function(c){return code[c]}).join('')}
  function huff(c){var h=c.slice().sort(function(a,b){return a-b}),t=0;while(h.length>1){var a=h.shift(),b=h.shift();t+=a+b;h.push(a+b);h.sort(function(x,y){return x-y})}return t}
  function genTree(r,nu,nf,md,sib){
    for(var it=0;it<2000;it++){var lv=[''];
      while(lv.length<nu+nf){var cand=lv.filter(function(w){return w.length<md});if(!cand.length)break;var w=exPick(r,cand);lv.splice(lv.indexOf(w),1);lv.push(w+'0',w+'1')}
      if(lv.length<nu+nf)continue;lv.sort();var fr=exShuf(r,lv).slice(0,nf);
      if(!sib){var fs={};fr.forEach(function(x){fs[x]=1});if(fr.some(function(x){return x&&fs[x.slice(0,-1)+(x[x.length-1]==='0'?'1':'0')]}))continue}
      var used=lv.filter(function(x){return fr.indexOf(x)<0}),mn=Math.min.apply(null,used.map(function(x){return x.length}));
      if(mn>=2||nu>6)return[used,fr]}
    return null}
  function rsn(w,fx,rev){for(var i=0;i<fx.length;i++){var x=fx[i];if(w===x)return'совпадает со словом '+x;
    if(rev){if(x.length>=w.length&&x.slice(-w.length)===w)return'является окончанием слова '+x;if(w.length>=x.length&&w.slice(-x.length)===x)return'оканчивается словом '+x}
    else{if(x.indexOf(w)===0)return'является началом слова '+x;if(w.indexOf(x)===0)return'начинается со слова '+x}}return null}
  function maxFree(fx){var o=[];for(var L=1;L<8;L++)freeWords(fx,L,false).forEach(function(w){var p=w.slice(0,-1);if(!p||!fanoOk(fx.concat([p]),false))o.push(w)});return o}
  function pl(n,a){var m=n%10,h=n%100;return n+' '+(m===1&&h!==11?a[0]:m>=2&&m<=4&&(h<10||h>=20)?a[1]:a[2])}
  function byLen(a){return a.slice().sort(function(x,y){return x.length-y.length||(x<y?-1:1)})}
  function num(w){return parseInt(w,2)}
  /* ---------- экземпляр ---------- */
  var SP={'4.1':function(r){return{kind:'one_word',nu:exPick(r,[7,8,9]),nf:exPick(r,[1,2]),minLen:3,md:5,sib:true}},
    '4.2':function(r){var nf=exPick(r,[2,3]);return{kind:'sum_two',nu:exPick(r,[6,7]),nf:nf,k:exPick(r,[2,nf]),md:5,sib:true}},
    '4.3':function(r){return{kind:'equal_len',nu:exPick(r,[3,4]),nf:3,k:exPick(r,[5,6]),md:4,sib:true}},
    '4.4':function(r){return{kind:'shorten',nu:exPick(r,[5,6,7]),nf:1,md:exPick(r,[4,5]),sib:true}},
    '4.5':function(r){return{kind:'decode',nu:exPick(r,[5,6]),nf:0,md:exPick(r,[3,4]),msg:exPick(r,[5,6]),sib:true}},
    '4.6':function(r){return{kind:'huffman'}},
    '4.7':function(r){return{kind:'rev_word',nu:exPick(r,[7,8]),nf:exPick(r,[1,2]),minLen:3,md:5,sib:true}}};
  function build(r,sp){
    var alpha=r()<.5?RU:LAT,k=sp.kind;
    for(var at=0;at<3000;at++){
      if(k==='huffman'){var w=exPick(r,WORDS),cnt={};w.split('').forEach(function(c){cnt[c]=(cnt[c]||0)+1});var ks=Object.keys(cnt);if(ks.length<5)continue;
        var ans=huff(ks.map(function(c){return cnt[c]})),nv=w.length*Math.max(1,Math.ceil(Math.log(ks.length)/Math.LN2-1e-9));if(nv===ans)continue;
        return{kind:k,word:w,counts:cnt,answer:ans,naive:nv,letters:ks.sort(),known:{},unknown:[]}}
      var rev=k==='rev_word',tr=genTree(r,sp.nu,sp.nf,sp.md,sp.sib);if(!tr)continue;var used=tr[0];if(rev)used=used.map(function(x){return x.split('').reverse().join('')});
      var nUnk={one_word:1,rev_word:1,sum_two:sp.k,equal_len:sp.k,shorten:0,decode:0}[k],nL=sp.nu+nUnk;
      var letters=exShuf(r,alpha.slice()).slice(0,nL).sort(function(a,b){return alpha.indexOf(a)-alpha.indexOf(b)});
      var unk=nUnk?exShuf(r,letters).slice(0,nUnk):[],kl=letters.filter(function(c){return unk.indexOf(c)<0});
      used=exShuf(r,used);var code={};kl.forEach(function(c,i){code[c]=used[i]});var fx=kl.map(function(c){return code[c]});
      if(!fanoOk(fx,rev))continue;
      var I={kind:k,letters:letters,known:code,unknown:unk,rev:rev,fixed:fx};
      if(k==='one_word'||k==='rev_word'){var w2=shortest(fx,rev);if(!w2||w2.length<sp.minLen||w2.length>6)continue;I.answer=w2;
        var alt=freeWords(fx,w2.length,rev).filter(function(x){return x!==w2});I.alt=alt[0]||null}
      else if(k==='sum_two'){var me=minExtra(fx,nUnk),nw=[],tmp=fx.slice(),bad=false;
        for(var u=0;u<nUnk;u++){var x=shortest(tmp,false);if(!x){bad=true;break}nw.push(x);tmp.push(x)}
        if(bad||!me[1]||me[0]>12||Math.max.apply(null,me[1].map(function(z){return z.length}))>6)continue;
        var naive=nw.reduce(function(a,z){return a+z.length},0);if(naive===me[0])continue;I.answer=me[0];I.words=me[1];I.naive=naive;I.naiveWords=nw}
      else if(k==='equal_len'){var el=equalLen(fx,nUnk);if(!el||el[0]>5||el[0]<3)continue;var nl=Math.max(1,Math.ceil(Math.log(nUnk)/Math.LN2-1e-9));if(nl===el[0])continue;
        I.answer=el[1];I.L=el[0];I.naiveL=nl;I.naive=fx.reduce(function(a,z){return a+z.length},0)+nUnk*nl}
      else if(k==='shorten'){var o=shortenOpts(code);if(o.length!==1)continue;I.answer=o[0][0]+o[0][1];I.letter=o[0][0];I.newWord=o[0][1]}
      else if(k==='decode'){var msg='',ms=sp.msg;for(var q=0;q<ms;q++)msg+=exPick(r,letters);var us={};msg.split('').forEach(function(c){us[c]=1});if(Object.keys(us).length<Math.min(4,ms))continue;
        var bits=encode(msg,code);if(bits.length>24)continue;I.answer=msg;I.bits=bits}
      return I}
    return null}
  function codeList(I){return I.letters.filter(function(c){return I.known[c]!==undefined}).map(function(c){return c+' — '+I.known[c]}).join(', ')}
  function intro(I){var s='Для кодирования сообщений используются буквы '+I.letters.join(', ')+'. Применяется неравномерный двоичный код, ';
    return s+(I.rev?'удовлетворяющий обратному условию Фано (ни одно кодовое слово не является окончанием другого кодового слова). ':'удовлетворяющий условию Фано (ни одно кодовое слово не является началом другого кодового слова). ')}
  function statement(I){var k=I.kind,u=I.unknown.join(', ');
    if(k==='one_word'||k==='rev_word')return intro(I)+'Для всех букв, кроме '+u+', кодовые слова известны: '+codeList(I)+'. Для буквы '+u+' нужно подобрать кодовое слово наименьшей длины, при котором условие выполняется; если таких слов несколько, выберите слово с наименьшим числовым значением. В ответе запишите кодовое слово.';
    if(k==='sum_two')return intro(I)+'Кодовые слова известны для букв: '+codeList(I)+'. Определите наименьшую возможную суммарную длину кодовых слов для букв '+u+'. В ответе запишите число.';
    if(k==='equal_len')return intro(I)+'Для букв '+I.letters.filter(function(c){return I.known[c]!==undefined}).join(', ')+' слова известны: '+codeList(I)+'. Для всех остальных букв ('+u+') кодовые слова имеют одинаковую длину. Определите наименьшую возможную сумму длин всех кодовых слов. В ответе запишите число.';
    if(k==='shorten')return intro(I)+'Код задан таблицей: '+codeList(I)+'. Для одной из букв можно сократить кодовое слово (отбросить последний символ) так, чтобы условие Фано по-прежнему выполнялось. Укажите эту букву и сокращённое слово; в ответе запишите букву и слово подряд, без пробелов.';
    if(k==='decode')return'Сообщение закодировано неравномерным двоичным кодом, удовлетворяющим условию Фано: '+codeList(I)+'. Передана строка '+I.bits+'. Расшифруйте сообщение; в ответе запишите буквы подряд.';
    return'Сообщение «'+I.word+'» кодируется двоичным кодом, удовлетворяющим условию Фано (код выбирается оптимально). Чему равна наименьшая возможная длина закодированного сообщения (в битах)? В ответе запишите число.'}
  function steps(I){var k=I.kind,S=[],fx=I.fixed;
    if(k==='one_word'||k==='rev_word'){var show=k==='rev_word'?fx.map(function(w){return w.split('').reverse().join('')}):fx,ans=k==='one_word'?I.answer:I.answer.split('').reverse().join('');
      S.push(k==='rev_word'?'Условие обратное: слово не должно быть окончанием другого. Читаем слова справа налево: переворачиваем заданные слова: '+show.join(', ')+'.':'Заданные слова: '+byLen(fx).join(', ')+'. Представь дерево: слова закрывают своё поддерево и пути к себе.');
      for(var L=1;L<=ans.length;L++){var parts=[],ws=allWords(L);for(var i=0;i<ws.length;i++){var rr=rsn(ws[i],show,false);if(rr)parts.push(ws[i]+' ✗ ('+rr+')');else{parts.push(ws[i]+' ✓ свободно');break}}S.push('Длина '+L+': '+parts.join('; ')+'.')}
      if(k==='rev_word')S.push('Найдено слово '+ans+' для перевёрнутой записи; переворачиваем обратно: '+I.answer+'.');
      S.push('Первое свободное слово и есть ответ: '+I.answer+' (кратчайшее, а среди слов этой длины с наименьшим числовым значением).');
      if(I.alt){var al=k==='one_word'?I.alt:I.alt.split('').reverse().join('');S.push('Другие свободные слова той же длины, например '+al+', имеют большее числовое значение: '+num(al)+' > '+num(I.answer)+'.')}}
    else if(k==='sum_two'){S.push('Заданные слова: '+byLen(fx).join(', ')+'. Нужно разместить '+I.unknown.length+' новых слов (буквы '+I.unknown.join(', ')+') с наименьшей суммой длин.');
      S.push('Самые высокие свободные узлы дерева: '+maxFree(fx).map(function(w){return w+' (глубина '+w.length+')'}).join(', ')+'. В свободном узле глубины d помещается одно слово длины d или два слова длины d+1.');
      S.push('«Жадный» путь (каждой букве по очереди самое короткое слово): '+I.naiveWords.join(', ')+', сумма '+I.naive+'.');
      S.push('Оптимальный набор (перебор свободных слов): '+I.words.join(', ')+', сумма '+I.answer+'. Условие Фано для всего кода выполнено.');
      S.push('Вывод: жадный путь даёт '+I.naive+', а лучший ответ '+I.answer+', потому что слова выгоднее разместить так, чтобы не «ломать» высокий свободный узел.')}
    else if(k==='equal_len'){var sm=fx.reduce(function(a,w){return a+w.length},0);S.push('Сумма длин заданных слов: '+fx.map(function(w){return w.length}).join(' + ')+' = '+sm+'. Остальных букв: '+I.unknown.length+', все слова одной длины L.');
      for(var L2=1;L2<=I.L;L2++){var fw=freeWords(fx,L2,false);S.push('L = '+L2+': свободных слов длины '+L2+' — '+fw.length+(fw.length<=10&&fw.length?' ('+fw.join(', ')+')':'')+'. Нужно '+I.unknown.length+' → '+(fw.length>=I.unknown.length?'хватает':'не хватает')+'.')}
      S.push('Наименьшая подходящая L = '+I.L+'. Сумма = '+sm+' + '+I.unknown.length+'·'+I.L+' = '+I.answer+'.');
      S.push('Ловушка: по формуле «⌈log₂ '+I.unknown.length+'⌉ = '+I.naiveL+'» получилось бы '+I.naive+', но часть слов длины '+I.naiveL+' закрыта заданными словами.')}
    else if(k==='shorten'){S.push('Для каждой буквы отбрасываем последний символ слова и проверяем условие Фано для всего кода.');
      I.letters.forEach(function(ch){var w=I.known[ch];if(w.length<2){S.push(ch+': слово '+w+' из одного символа сокращать нельзя.');return}
        var nw=w.slice(0,-1),others=I.letters.filter(function(c){return c!==ch}).map(function(c){return I.known[c]}),r2=rsn(nw,others,false);S.push(ch+': '+w+' → '+nw+': '+(r2?'✗ '+r2:'✓ код остаётся префиксным')+'.')});
      S.push('Подходит ровно одна буква: '+I.letter+'; новое слово '+I.newWord+'.')}
    else if(k==='decode'){var inv={};I.letters.forEach(function(c){inv[I.known[c]]=c});var cur='',pp=[],out='';
      I.bits.split('').forEach(function(b){cur+=b;if(inv[cur]!==undefined){pp.push(cur);out+=inv[cur];cur=''}});
      S.push('Слова: '+codeList(I)+'.');S.push('Читаем строку '+I.bits+' слева направо; как только набранное совпало со словом, записываем букву: '+pp.map(function(p){return p+'→'+inv[p]}).join(' | ')+'.');
      S.push('Сообщение: '+out+'. Проверка: закодируем обратно, получится '+encode(out,I.known)+'.')}
    else{var cn=I.counts,ks=Object.keys(cn).sort();S.push('Частоты букв в «'+I.word+'»: '+ks.map(function(c){return c+': '+cn[c]}).join(', ')+'.');
      var h=ks.map(function(c){return cn[c]}).sort(function(a,b){return a-b}),st=[],sums=[],t=0;
      while(h.length>1){var a=h.shift(),b=h.shift();st.push(a+' + '+b+' = '+(a+b));sums.push(a+b);t+=a+b;h.push(a+b);h.sort(function(x,y){return x-y})}
      S.push('Сливаем два самых лёгких узла, пока не останется один: '+st.join('; ')+'.');S.push('Длина сообщения равна сумме весов слияний: '+sums.join(' + ')+' = '+t+'.');
      S.push('Для сравнения: равномерный код ('+Math.ceil(Math.log(ks.length)/Math.LN2-1e-9)+' бита на букву) дал бы '+I.naive+' бит, код Хаффмана короче.')}
    return S}
  function mistake(I){var k=I.kind;
    return{one_word:'Берут слово, которое является началом заданного, или слово не той длины без перебора по порядку. Верный ответ это первое свободное слово.',
      rev_word:'Применяют прямое условие Фано (проверка по началу). При обратном условии слова сравниваются по окончанию.',
      sum_two:'Дают «жадный» ответ ('+I.naive+') вместо верного ('+I.answer+'): каждой букве по очереди самое короткое слово.',
      equal_len:'Берут длину L по формуле ⌈log₂ k⌉ и не учитывают узлы, закрытые заданными словами: получается '+I.naive+' вместо '+I.answer+'.',
      shorten:'Записывают ответ без буквы или без слова. Нужны буква и сокращённое слово подряд.',
      decode:'Режут строку не с начала или пропускают бит. Проверка: закодируй ответ обратно и сравни со строкой.',
      huffman:'Считают равномерным кодом ('+I.naive+' бит) вместо оптимального ('+I.answer+' бит).'}[k]}
  function hints(I){var k=I.kind;
    if(k==='huffman')return['Посчитай, сколько раз встречается каждая буква.','Возьми два самых редких «узла» и слей их в один (вес равен сумме).','Повторяй, пока не останется один узел. Длина сообщения равна сумме всех полученных весов.'];
    if(k==='decode')return['Выпиши все слова кода.','Читай строку слева направо и отрезай слово, как только набранное совпало с кодовым словом.','Каждое слово заменяй буквой. Проверь: закодируй ответ обратно.'];
    if(k==='equal_len')return['Найди сумму длин заданных слов.','Для длин L = 1, 2, 3… считай, сколько слов длины L ещё свободно (не начинаются с заданных и не являются их началом).','Нужна наименьшая L, при которой свободных слов не меньше, чем остальных букв.'];
    if(k==='shorten')return['Для каждой буквы отбрось последний символ её слова.','Проверь для нового кода условие Фано: нет ли слова, которое стало началом другого?','Подходит ровно одна буква. Запиши её и новое слово подряд.'];
    if(k==='sum_two')return['Найди свободные узлы дерева, пока не думая о буквах.','Оцени «жадный» вариант (каждой букве самое короткое слово), но проверь другие.','Иногда выгоднее занять один высокий свободный узел сразу двумя словами длины d+1.','Проверь выбранные слова условием Фано.'];
    return['Выпиши заданные слова'+(k==='rev_word'?' и переверни их (условие обратное).':'.'),'Перебирай длины 1, 2, 3… Внутри длины слова идут по возрастанию значения: 00, 01, 10, 11.','Для каждого кандидата проверь: он не совпадает с заданным, не является его началом и не начинается с него.','Первое свободное слово и есть ответ.']}
  var FMT={one_word:'Слово из 0 и 1 без пробелов, например 1000.',rev_word:'Слово из 0 и 1 без пробелов, например 1000.',sum_two:'Одно число.',equal_len:'Одно число.',shorten:'Буква и слово подряд, без пробелов, например Г10.',decode:'Буквы подряд, без пробелов.',huffman:'Одно число (биты).'};
  function ct(I){if(I.kind==='huffman')return{hdr:['Буква'].concat(Object.keys(I.counts).sort()),row:['Частота'].concat(Object.keys(I.counts).sort().map(function(c){return I.counts[c]}))};
    return{hdr:['Буква'].concat(I.letters),row:['Код'].concat(I.letters.map(function(c){return I.known[c]!==undefined?I.known[c]:'?'}))}}
  function starter(I){var s='';if(I.kind==='huffman')return'word = '+JSON.stringify(I.word)+'\n';
    s+='known = {'+I.letters.filter(function(c){return I.known[c]!==undefined}).map(function(c){return"'"+c+"': '"+I.known[c]+"'"}).join(', ')+'}\n';
    if(I.kind==='decode')s+="bits = '"+I.bits+"'\n";if(I.kind==='sum_two'||I.kind==='equal_len')s+='k = '+I.unknown.length+'\n';return s}
  window.ex4={build:build,steps:steps,statement:statement,fanoOk:fanoOk,shortest:shortest,equalLen:equalLen,minExtra:minExtra,shortenOpts:shortenOpts,huff:huff,ct:ct,starter:starter,mistake:mistake,hints:hints,FMT:FMT};
  /* достраивает готовое задание по query (kind, known, ...) */
  window.exFill4=function(q){var Q=q.query;if(!Q)return;
    var I={kind:Q.kind,letters:Q.letters,known:Q.known,unknown:Q.unknown||[],rev:Q.kind==='rev_word',fixed:Object.keys(Q.known).map(function(c){return Q.known[c]})};
    if(Q.kind==='huffman'){I.word=Q.word;I.counts={};Q.word.split('').forEach(function(c){I.counts[c]=(I.counts[c]||0)+1});I.letters=Object.keys(I.counts).sort();I.answer=huff(Object.keys(I.counts).map(function(c){return I.counts[c]}));I.naive=Q.word.length*Math.ceil(Math.log(I.letters.length)/Math.LN2-1e-9)}
    if(Q.kind==='decode'){I.bits=Q.bits}
    var ans=q.a;
    if(Q.kind==='one_word'||Q.kind==='rev_word'){I.answer=shortest(I.fixed,I.rev);var al=freeWords(I.fixed,I.answer.length,I.rev).filter(function(x){return x!==I.answer});I.alt=al[0]||null}
    if(Q.kind==='sum_two'){var me=minExtra(I.fixed,I.unknown.length),nw=[],tmp=I.fixed.slice();for(var u=0;u<I.unknown.length;u++){var x=shortest(tmp,false);nw.push(x);tmp.push(x)}I.answer=me[0];I.words=me[1];I.naive=nw.reduce(function(a,z){return a+z.length},0);I.naiveWords=nw}
    if(Q.kind==='equal_len'){var el=equalLen(I.fixed,I.unknown.length);I.answer=el[1];I.L=el[0];I.naiveL=Math.max(1,Math.ceil(Math.log(I.unknown.length)/Math.LN2-1e-9));I.naive=I.fixed.reduce(function(a,z){return a+z.length},0)+I.unknown.length*I.naiveL}
    if(Q.kind==='shorten'){var o=shortenOpts(I.known)[0];I.letter=o[0];I.newWord=o[1];I.answer=o[0]+o[1]}
    if(Q.kind==='decode'){var inv={};Object.keys(Q.known).forEach(function(c){inv[Q.known[c]]=c});var cur='',out='';Q.bits.split('').forEach(function(b){cur+=b;if(inv[cur]){out+=inv[cur];cur=''}});I.answer=out}
    q._v=String(I.answer);
    if(!q.s)q.s=steps(I);if(!q.h)q.h=hints(I);if(!q.ct)q.ct=ct(I);if(!q.starter)q.starter=starter(I)};
  window.exTb4=function(c){return'<table class="exft ct"><tr>'+c.hdr.map(function(x){return'<th>'+esc(x)+'</th>'}).join('')+'</tr><tr>'+c.row.map(function(x,i){return i?'<td>'+esc(String(x))+'</td>':'<th>'+esc(x)+'</th>'}).join('')+'</tr></table>'};
  EXGEN[4]={no:4,name:'Неравномерные коды',types:[{id:'4.1',n:'Кратчайшее слово',d:'Одна неизвестная буква'},{id:'4.2',n:'Сумма длин двух-трёх слов',d:'Выгодно разместить слова'},{id:'4.3',n:'Слова одинаковой длины',d:'Наименьшая сумма длин'},{id:'4.4',n:'Сократить слово',d:'Какая буква и какое слово'},{id:'4.5',n:'Расшифровка сообщения',d:'Разрезать строку на слова'},{id:'4.6',n:'Длина сообщения (Хаффман)',d:'Оптимальный код'},{id:'4.7',n:'Обратное условие Фано',d:'Слова по окончаниям'}],
    make:function(type,r){r=r||exRnd((Date.now()^(Math.random()*4294967296))>>>0);if(type==='any')type=exPick(r,['4.1','4.1','4.2','4.3','4.4','4.5','4.6','4.7']);
      var sp=SP[type](r),I=build(r,sp);if(!I)return null;
      return{q:statement(I),ct:ct(I),f:FMT[I.kind],h:hints(I),s:steps(I),a:String(I.answer),m:mistake(I),type:type,starter:starter(I)}}};
})();
