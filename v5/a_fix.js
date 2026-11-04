/* --- := в любом месте (v5.1.0) ---
   Skulpt не знает :=. Переписываем (имя := выражение) в равносильное выражение
   ([имя for имя in [выражение]][0]), которое присваивает имя там же, где стоит оператор. */
function wal(code){
  if(code.indexOf(':=')<0)return{code:code,map:null};
  function scan(src){ // позиции := вне строк и комментариев + маска «внутри строки»
    var pos=[],n=src.length,i=0;
    while(i<n){
      var c=src[i];
      if(c==='#'){while(i<n&&src[i]!=='\n')i++;continue}
      if(c==='"'||c==="'"){
        var q3=src.substr(i,3)===c+c+c,q=q3?c+c+c:c;i+=q.length;
        while(i<n){if(src[i]==='\\'){i+=2;continue}if(src.substr(i,q.length)===q){i+=q.length;break}if(!q3&&src[i]==='\n')break;i++}
        continue}
      if(c===':'&&src[i+1]==='='){pos.push(i);i+=2;continue}
      i++}
    return pos}
  var guard=0;
  while(guard++<200){
    var P=scan(code);if(!P.length)break;
    var k=P[P.length-1],left=code.slice(0,k),m=/([A-Za-z_\u0400-\u04FF][\w\u0400-\u04FF]*)\s*$/.exec(left);
    if(!m)break; // не наш случай, пусть Python сам скажет об ошибке
    var name=m[1],st=k-m[0].length+(m[0].length-m[0].replace(/\s+$/,'').length)*0;
    var s=k+2,j=s,d=0,n=code.length,q2='';
    while(j<n){
      var c=code[j];
      if(c==='"'||c==="'"){var t3=code.substr(j,3)===c+c+c,qq=t3?c+c+c:c;j+=qq.length;
        while(j<n){if(code[j]==='\\'){j+=2;continue}if(code.substr(j,qq.length)===qq){j+=qq.length;break}if(!t3&&code[j]==='\n')break;j++}continue}
      if(c==='#')break;
      if(c==='('||c==='['||c==='{')d++;
      else if(c===')'||c===']'||c==='}'){if(d===0)break;d--}
      else if(d===0&&(c===','||c===':'||c==='\n'||c===';'))break;
      else if(d===0&&/\sfor\s/.test(code.substr(j-1,5)))break;
      j++}
    var ex=code.slice(s,j).replace(/\s+$/,''),tail=code.slice(s+ex.length,j);
    var rep='([%n for %n in [%e]][0])'.replace(/%n/g,name).replace('%e',function(){return ex.trim()});
    code=code.slice(0,st)+rep+tail+code.slice(j);
  }
  return{code:code,map:null};
}

/* --- ползунок в переключателях (плавно и ровно) --- */
function segPos(sc,anim){
  var b=sc.querySelector('button.on'),p=sc.querySelector('.segp');
  if(!p){p=document.createElement('i');p.className='segp';sc.insertBefore(p,sc.firstChild)}
  if(!b||!b.offsetWidth){p.style.opacity=0;return}
  p.style.opacity=1;
  if(!anim||RM())sc.classList.add('nt');
  p.style.width=b.offsetWidth+'px';p.style.transform='translateX('+b.offsetLeft+'px)';
  if(!anim||RM()){void p.offsetWidth;sc.classList.remove('nt')}
}
function segInit(root){
  (root||app).querySelectorAll('.segc').forEach(function(sc){
    segPos(sc,false);
    if(window.ResizeObserver&&!sc._ro){sc._ro=new ResizeObserver(function(){segPos(sc,false)});sc._ro.observe(sc)}
  });
}
/* --- каждый новый экран открывается сверху --- */
var KEEPSCR=0,show0=show;
show=function(h,tab){show0(h,tab);if(KEEPSCR)KEEPSCR=0;else window.scrollTo(0,0);segInit();};
/* --- счётчик верных ответов в случайных режимах --- */
function rcInc(){S.cn.rc=Math.min(99999,(S.cn.rc||0)+1);save();if(S.cn.rc>=50)ach('rnd50')}
/* --- пасхалка: 12 нажатий на версию --- */
var EGGN=0,EGGT=0;
function eggBind(){
  var r=document.getElementById('egv');if(!r)return;var row=r.closest('.li');if(!row)return;
  row.style.cursor='pointer';
  row.onclick=function(){
    clearTimeout(EGGT);EGGT=setTimeout(function(){EGGN=0},1600);
    if(++EGGN<12){if(!RM())row.animate([{transform:'scale(1)'},{transform:'scale(.985)'},{transform:'scale(1)'}],{duration:120});return}
    EGGN=0;ach('egg');snd('fanfare');vib([20,30,20,30,60]);
    modal('<div class="egg"><div class="eggi">🪄</div><h2>Ты нашёл секрет!</h2><p>ИТП создал Адрианов Владислав для индивидуального школьного проекта.</p><p class="mu">Спасибо, что дошёл до самого конца настроек.</p></div>',[['Класс!',null,1]]);
  }
}
/* --- копирование кода из теории --- */
/* 7.1.1: «Отправить» картинку с подписью. Telegram, WhatsApp и окно «Поделиться» Windows, получив картинку, текст
   выбрасывают — уходила одна картинка без подписи (владелец). Поэтому подпись заранее копируется в буфер: её остаётся
   вставить в сообщение. share() — сразу, в том же нажатии, иначе браузер не откроет окно «Поделиться» */
/* 7.2.0: в APK у WebView нет navigator.share — отправляем через плагин Share: файл картинки и (если есть) текст.
   Раньше там была только «Скачать картинку» с title: имя файла, и Telegram подставлял «itp-progress.png» в подпись */
function natShare(){var C=window.Capacitor,P=C&&C.Plugins;return C&&C.isNativePlatform&&C.isNativePlatform()&&P&&P.Filesystem&&P.Share?P:null}
function natSend(name,blob,tx,dlg){var P=natShare();return new Promise(function(res,rej){var fr=new FileReader();
  fr.onload=function(){P.Filesystem.writeFile({path:name,data:String(fr.result).split(',')[1],directory:'CACHE'}).then(function(r){
    var o={files:[r.uri],dialogTitle:dlg||'Отправить'};if(tx)o.text=tx;return P.Share.share(o)}).then(res,rej)};
  fr.onerror=rej;fr.readAsDataURL(blob)})}
function canSend(){return!!(navigator.share||natShare())}
(function(){var _sf=saveFile;saveFile=function(name,blob){
  if(natShare()&&/\.png$/.test(name)){natSend(name,blob,'','Сохранить или отправить').catch(function(){});return true}
  return _sf(name,blob)}})();
function shareImg(name,blob,tx){
  if(natShare())return natSend(name,blob,tx).then(function(){ach('share')}).catch(function(){});
  var f;try{f=new File([blob],name,{type:'image/png'})}catch(e){}
  var withFile=!!(f&&navigator.canShare&&navigator.canShare({files:[f]}));
  /* без tx — только картинка (карточка «Я могу…»: владелец — подписи под ней быть не должно) */
  if(!withFile&&!tx){toast('Отправить картинку отсюда нельзя — сохрани её и отправь как фото');return Promise.resolve()}
  if(withFile&&tx)copyText(tx).then(function(){toast('Подпись скопирована — вставь её в сообщение')},function(){});
  return navigator.share(withFile?(tx?{files:[f],text:tx}:{files:[f]}):{text:tx}).then(function(){ach('share')}).catch(function(){})}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText)return navigator.clipboard.writeText(t);
  return new Promise(function(res,rej){var a=document.createElement('textarea');a.value=t;a.style.cssText='position:fixed;opacity:0;top:0';document.body.appendChild(a);a.select();try{document.execCommand('copy')?res():rej()}catch(e){rej()}a.remove()});
}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.cp');if(!b)return;
  var pre=b.parentNode.querySelector('pre');if(!pre)return;
  copyText(pre.textContent.replace(/\n$/,'')).then(function(){b.classList.add('ok');snd('tick');setTimeout(function(){b.classList.remove('ok')},1400)},function(){toast('Не получилось скопировать')});
});

/* пример кода под объяснением вопроса */
function xm(q){
  if(!q||!q.x)return '';
  var inp=q.xi&&q.xi.length?'<div class="xl">Ввод: '+esc(q.xi.join(', '))+'</div>':'';
  return '<div class="xw"><div class="xl">Пример</div>'+inp+'<pre>'+hl(q.x)+'</pre><pre class="out">'+esc(q.xo||'')+'</pre></div>';
}

/* ===== движок: файлы, stdin, json, csv, pprint, strptime, eval, timeit ===== */
var ITPY=/*ITPY*/{};
function fsOf(f){return !f?null:typeof f==='string'?(typeof FILESETS!=='undefined'&&FILESETS[f])||null:f}
var FCUR=null,ITPNEED=/\b(strict|open|stdin|eval|getsizeof|perf_counter|perf_counter_ns|monotonic|OSError|IOError|FileNotFoundError|FileExistsError|timeit|bytearray|from_bytes)\b/;
function itpReg(){
  var F=Sk.builtinFiles.files,K={json:'json/__init__',csv:'csv',pprint:'pprint',_strptime:'_strptime',timeit:'timeit',itpshim:'itpshim',io:'io',functools:'functools',heapq:'heapq',statistics:'statistics'};
  Object.keys(K).forEach(function(k){if(ITPY[k])F['src/lib/'+K[k]+'.py']=ITPY[k]});
}
var skPatch0=skPatch;skPatch=function(){skPatch0();try{itpReg()}catch(e){}};
(function(){var t0=task,p0=project;
  task=function(i,j,k){var r=t0(i,j,k);try{FCUR=fsOf((IT(i,j).tasks[k]||{}).f)}catch(e){FCUR=null}return r};
  project=function(i,j){var r=p0(i,j);try{FCUR=fsOf(IT(i,j).f)}catch(e){FCUR=null}return r};
  var s0=show;show=function(h,tab){FCUR=null;return s0(h,tab)};
})();

/* ===== math: недостающие функции; float: repr как в CPython; round с ndigits ===== */
function itpMath(){
  var F=Sk.builtinFiles.files,o=F['src/lib/math.js'];
  if(!o||o.indexOf('$itpx')>=0||o.indexOf('const $builtinmodule=function(){')!==0)return;
  var X='\n;/*$itpx*/const $builtinmodule=function(){var l=$mo();'
  +'var N=function(a){return Number(Sk.builtin.asnum$(a))},B=function(a){return BigInt(String(Sk.builtin.asnum$(a)))},I=function(b){return new Sk.builtin.int_(Number(b))},Fl=function(x){return new Sk.builtin.float_(x)};'
  +'var E={};'
  +'E.isqrt={$meth:function(a){var n=B(a);if(n<0n)throw new Sk.builtin.ValueError("isqrt() argument must be nonnegative");if(n<2n)return I(n);var x=BigInt(Math.floor(Math.sqrt(Number(n))));while(x*x>n)x--;while((x+1n)*(x+1n)<=n)x++;return I(x)},$flags:{OneArg:true}};'
  +'E.comb={$meth:function(a,b){var n=B(a),k=B(b);if(n<0n||k<0n)throw new Sk.builtin.ValueError("n must be a non-negative integer");if(k>n)return I(0n);if(k>n-k)k=n-k;var r=1n;for(var i=1n;i<=k;i++){r=r*(n-k+i)/i}return I(r)},$flags:{MinArgs:2,MaxArgs:2}};'
  +'E.perm={$meth:function(a,b){var n=B(a),k=b===undefined||b===Sk.builtin.none.none$?n:B(b);if(n<0n||k<0n)throw new Sk.builtin.ValueError("n must be a non-negative integer");if(k>n)return I(0n);var r=1n;for(var i=0n;i<k;i++)r*=n-i;return I(r)},$flags:{MinArgs:1,MaxArgs:2}};'
  +'E.lcm={$meth:function(a,b){var x=B(a),y=B(b);if(x<0n)x=-x;if(y<0n)y=-y;if(x===0n||y===0n)return I(0n);var p=x,q=y;while(q){var t=p%q;p=q;q=t}return I(x/p*y)},$flags:{MinArgs:2,MaxArgs:2}};'
  +'E.prod={$meth:function(it,st){var r=st===undefined?new Sk.builtin.int_(1):st;var xs=Sk.misceval.arrayFromIterable(it);for(var i=0;i<xs.length;i++)r=Sk.abstr.numberBinOp(r,xs[i],"Mult");return r},$flags:{MinArgs:1,MaxArgs:2}};'
  +'E.cbrt={$meth:function(a){return Fl(Math.cbrt(N(a)))},$flags:{OneArg:true}};'
  +'E.dist={$meth:function(p,q){var a=Sk.misceval.arrayFromIterable(p),b=Sk.misceval.arrayFromIterable(q);if(a.length!==b.length)throw new Sk.builtin.ValueError("both points must have the same number of dimensions");var s=0;for(var i=0;i<a.length;i++){var d=N(a[i])-N(b[i]);s+=d*d}return Fl(Math.sqrt(s))},$flags:{MinArgs:2,MaxArgs:2}};'
  +'Sk.abstr.setUpModuleMethods("math",l,E);return l};';
  F['src/lib/math.js']=o.replace('const $builtinmodule=function(){','const $mo=function(){')+X;
}
function itpFloat(){
  if(!Number.prototype.toFixed.$itp){var tf=Number.prototype.toFixed;
    Number.prototype.toFixed=function(d){var s=tf.call(this,d);d=d|0;if(d<0||d>70||!isFinite(this)||Math.abs(this)>=1e21)return s;
      var e=tf.call(this,d+30),i=e.indexOf('.'),fr=e.slice(i+1);
      if(fr[d]==='5'&&/^0*$/.test(fr.slice(d+1))){var t=e.slice(0,i+(d?1+d:0));if((+t[t.length-1])%2===0)return t}
      return s};
    Number.prototype.toFixed.$itp=1}
  var P=Sk.builtin.float_.prototype;if(P.$itp)return;P.$itp=1;var old=P.str$;
  P.str$=function(base,sign){
    if(base!==undefined&&base!==10)return old.call(this,base,sign);
    var v=this.v;if(isNaN(v))return'nan';if(v===Infinity)return'inf';if(v===-Infinity)return sign===false?'inf':'-inf';
    if(v===0)return(1/v<0&&sign!==false)?'-0.0':'0.0';
    var neg=v<0&&sign!==false,a=Math.abs(v),m=/^(\d)(?:\.(\d+))?e([+-]\d+)$/.exec(a.toExponential());
    var dg=m[1]+(m[2]||''),ex=+m[3],r;
    if(ex<-4||ex>=16){r=dg[0]+(dg.length>1?'.'+dg.slice(1):'')+'e'+(ex<0?'-':'+')+(Math.abs(ex)<10?'0':'')+Math.abs(ex)}
    else if(ex>=0){r=dg.length<=ex+1?dg+'0'.repeat(ex+1-dg.length)+'.0':dg.slice(0,ex+1)+'.'+dg.slice(ex+1)}
    else r='0.'+'0'.repeat(-ex-1)+dg;
    return(neg?'-':'')+r};
  var oldR=Sk.builtins.round;
  Sk.builtins.round=new Sk.builtin.func(function(num,nd){
    if(nd!==undefined&&nd!==Sk.builtin.none.none$&&num instanceof Sk.builtin.float_){
      var n=Sk.builtin.asnum$(nd),x=num.v;
      if(isFinite(x)&&n>=0&&n<=20&&Math.abs(x)<1e15){
        var neg=x<0,s=Math.abs(x).toFixed(Math.min(100,n+40)),dot=s.indexOf('.'),ip=s.slice(0,dot),fr=s.slice(dot+1),kept=ip+fr.slice(0,n),c=fr[n],rest=fr.slice(n+1),
        up=c>'5'||(c==='5'&&(/[1-9]/.test(rest)||(+kept[kept.length-1])%2===1));
        var big=BigInt(kept)+(up?1n:0n),t=big.toString();
        if(n>0){t=t.padStart(n+1,'0');t=t.slice(0,-n)+'.'+t.slice(-n)}
        return new Sk.builtin.float_((neg?-1:1)*parseFloat(t))}
    }
    return Sk.misceval.callsimArray(oldR,nd===undefined?[num]:[num,nd])});
}
var skPatch1=skPatch;skPatch=function(){skPatch1();try{itpMath()}catch(e){}try{itpFloat()}catch(e){}};

/* ===== методы строк, которых нет в Skulpt ===== */
function itpStr(){
  var M=Sk.builtin.str.prototype;if(M.$itps)return;M.$itps=1;
  function add(name,fl,fn){if(M[name])return;var d=Object.assign(Object.create(Object.getPrototypeOf(M.lower)),M.lower);d.$meth=fn;d.$flags=fl;d.d$name=name;d.$name=name;if(d.d$def){d.d$def=Object.assign({},M.lower.d$def);d.d$def.$meth=fn;d.d$def.$flags=fl;d.d$def.$name=name}M[name]=d}
  var S=function(x){return new Sk.builtin.str(x)};
  add('casefold',{NoArgs:true},function(){return S(this.v.toLowerCase().replace(/ß/g,'ss'))});
  add('removeprefix',{OneArg:true},function(p){var v=this.v,q=p.v;return S(q&&v.startsWith(q)?v.slice(q.length):v)});
  add('removesuffix',{OneArg:true},function(p){var v=this.v,q=p.v;return S(q&&v.endsWith(q)?v.slice(0,v.length-q.length):v)});
  add('isidentifier',{NoArgs:true},function(){return /^[\p{L}_][\p{L}\p{Nd}_]*$/u.test(this.v)?Sk.builtin.bool.true$:Sk.builtin.bool.false$});
}
var skPatch2=skPatch;skPatch=function(){skPatch2();try{itpStr()}catch(e){}};

/* ===== f"{x=}" и match/case: переписываем исходный код в равносильный ===== */
function eqFix(code){
  return code.replace(/\b([fF][rR]?|[rR][fF])(?=(["']))("""|'''|"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')/g,function(m){
    return m.replace(/\{([^{}!:=\n]+?)(\s*=\s*)(![rsa])?(:[^{}\n]*)?\}/g,function(x,e,eq,cv,fm){
      if(/^\s*$/.test(e))return x;
      return e+eq+'{'+e+(cv||(fm?'':'!r'))+(fm||'')+'}'})})}
function matchT(code){
  var L=code.split('\n'),map=[],o=[],i,n=0;
  for(i=0;i<L.length;i++)map.push(i+1);
  function ind(l){return l.match(/^[ ]*/)[0].length}
  function blank(l){return /^\s*(#.*)?$/.test(l)}
  function splitTop(s,ch){var r=[],d=0,q=null,cur='';for(var k=0;k<s.length;k++){var c=s[k];if(q){cur+=c;if(c==='\\'){cur+=s[++k]}else if(c===q)q=null;continue}if(c==='"'||c==="'"){q=c;cur+=c;continue}if('([{'.indexOf(c)>=0)d++;if(')]}'.indexOf(c)>=0)d--;if(c===ch&&d===0){r.push(cur);cur=''}else cur+=c}r.push(cur);return r}
  var uid=0;
  function pat(p,S){ // возвращает условие (строка); захваты через :=
    p=p.trim();
    var alts=splitTop(p,'|');
    if(alts.length>1)return '('+alts.map(function(a){return pat(a,S)}).join(' or ')+')';
    var m=/^(.*\S)\s+as\s+([A-Za-z_]\w*)$/.exec(p);
    if(m)return '('+pat(m[1],S)+' and ((('+m[2]+' := '+S+')) or True))';
    if(p==='_')return 'True';
    if(/^[A-Za-z_]\w*$/.test(p)&&p!=='None'&&p!=='True'&&p!=='False')return '((('+p+' := '+S+')) or True)';
    if(p==='None'||p==='True'||p==='False')return '('+S+' is '+p+')';
    if(/^\(.*\)$/.test(p)||/^\[.*\]$/.test(p)){
      var inner=p.slice(1,-1),parts=splitTop(inner,',').map(function(x){return x.trim()}).filter(function(x){return x!==''});
      var st=-1,k;for(k=0;k<parts.length;k++)if(parts[k][0]==='*'){st=k;break}
      var c='isinstance('+S+', (list, tuple))';
      if(st<0){c+=' and len('+S+') == '+parts.length;parts.forEach(function(x,j){c+=' and '+pat(x,S+'['+j+']')})}
      else{var after=parts.length-st-1;c+=' and len('+S+') >= '+(parts.length-1);
        parts.forEach(function(x,j){if(j<st)c+=' and '+pat(x,S+'['+j+']');else if(j>st)c+=' and '+pat(x,S+'[len('+S+')-'+(parts.length-j)+']');else{var nm=x.slice(1).trim();if(nm!=='_')c+=' and ((('+nm+' := list('+S+'['+st+':len('+S+')-'+after+'])) ) or True)'}})}
      return '('+c+')'}
    if(/^\{.*\}$/.test(p)){
      var items=splitTop(p.slice(1,-1),',').map(function(x){return x.trim()}).filter(Boolean),c2='isinstance('+S+', dict)';
      items.forEach(function(it){if(it.slice(0,2)==='**'){var nm=it.slice(2).trim();return}var kv=splitTop(it,':');c2+=' and ('+kv[0].trim()+') in '+S+' and '+pat(kv.slice(1).join(':'),S+'['+kv[0].trim()+']')});
      return '('+c2+')'}
    var cm=/^([A-Za-z_][\w.]*)\((.*)\)$/.exec(p);
    if(cm){var cls=cm[1],args=splitTop(cm[2],',').map(function(x){return x.trim()}).filter(Boolean),c3='isinstance('+S+', '+cls+')';
      args.forEach(function(a,j){var kw=/^([A-Za-z_]\w*)\s*=\s*(.*)$/.exec(a);if(kw)c3+=' and hasattr('+S+', "'+kw[1]+'") and '+pat(kw[2],'getattr('+S+', "'+kw[1]+'")');else if(args.length===1&&/^(int|str|float|bool|list|tuple|dict|set)$/.test(cls))c3+=' and '+pat(a,S);else c3+=' and '+pat(a,S+'['+j+']')});
      return '('+c3+')'}
    return '('+S+' == '+p+')'}
  function one(){
    var k,mi=-1;
    for(k=L.length-1;k>=0;k--){if(/^\s*match\s+.+:\s*(#.*)?$/.test(L[k])&&!/^\s*match\s*[=.,)\[]/.test(L[k])){var j=k+1;while(j<L.length&&blank(L[j]))j++;if(j<L.length&&ind(L[j])>ind(L[k])&&/^\s*case\s.+:\s*(#.*)?$/.test(L[j])){mi=k;break}}}
    if(mi<0)return false;
    var mind=ind(L[mi]),subj=/^\s*match\s+(.+?):\s*(#.*)?$/.exec(L[mi])[1],j2=mi+1;
    while(j2<L.length&&blank(L[j2]))j2++;
    var cind=ind(L[j2]),shift=cind-mind,end=j2,cases=[];
    while(end<L.length){
      if(blank(L[end])){end++;continue}
      if(ind(L[end])<=mind)break;
      if(ind(L[end])===cind&&/^\s*case\s/.test(L[end])){cases.push({h:end,b:[]});end++;continue}
      if(ind(L[end])<cind)break;
      if(cases.length)cases[cases.length-1].b.push(end);end++}
    while(end>mi&&blank(L[end-1]))end--;
    var S='_m'+(uid++),pad=' '.repeat(mind),out=[],om=[],first=true;
    out.push(pad+S+' = '+subj);om.push(map[mi]);
    cases.forEach(function(c,ci){
      var h=/^\s*case\s+(.+?):\s*(#.*)?$/.exec(L[c.h])[1],g='',gm=splitTop(h,' ');
      var gi=h.search(/\s+if\s+(?![^()\[\]{}]*[)\]}])/);
      if(gi>=0){g=h.slice(gi).replace(/^\s+if\s+/,'');h=h.slice(0,gi)}
      var cond=pat(h,S);if(g)cond='('+cond+') and ('+g+')';
      var last=ci===cases.length-1&&cond==='True'&&!g;
      out.push(pad+(last?(first?'if True':'else'):(first?'if ':'elif ')+cond)+':');om.push(map[c.h]);first=false;
      var any=false;
      c.b.forEach(function(b){out.push(L[b].slice(Math.min(shift,ind(L[b]))));om.push(map[b]);any=true});
      if(!any){out.push(pad+'    pass');om.push(map[c.h])}});
    L.splice.apply(L,[mi,end-mi].concat(out));map.splice.apply(map,[mi,end-mi].concat(om));
    return true}
  var guard=0;while(guard++<50&&one());
  return{code:L.join('\n'),map:map}}
var wal0=wal;
wal=function(code){
  var c1=eqFix(code),M=/\bmatch\b/.test(c1)?matchT(c1):{code:c1,map:null},W=wal0(M.code);
  if(M.map&&W.map)W.map=W.map.map(function(x){return M.map[x-1]||x});
  else if(M.map)W.map=M.map;
  return W};

function itpKey(){var K=Sk.builtin.KeyError.prototype;if(K.$itpk)return;K.$itpk=1;var old=K.tp$str;K.tp$str=function(){try{var a=this.args&&this.args.v;if(a&&a.length===1)var r=Sk.misceval.objectRepr(a[0]);return new Sk.builtin.str(typeof r==='string'?r:r.v)}catch(e){}return old.call(this)}}
var skPatch3=skPatch;skPatch=function(){skPatch3();try{itpKey()}catch(e){}};
