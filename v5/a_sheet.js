/* ===================== v5.1.3: встроенная электронная таблица для задания №3 (формулы Excel/LibreOffice, фильтр, ВПР, СУММЕСЛИМН) ===================== */
(function(){
  var CY={'А':'A','В':'B','С':'C','Е':'E','Н':'H','К':'K','М':'M','О':'O','Р':'P','Т':'T','а':'a','в':'b','с':'c','е':'e','н':'h','к':'k','м':'m','о':'o','р':'p','т':'t'};
  function colName(c){var s='';c++;while(c>0){var m=(c-1)%26;s=String.fromCharCode(65+m)+s;c=Math.floor((c-1)/26)}return s}
  function colNum(s){s=s.toUpperCase();var n=0;for(var i=0;i<s.length;i++)n=n*26+s.charCodeAt(i)-64;return n-1}
  function lat(s){return s.replace(/[А-Яа-я]/g,function(ch){return CY[ch]||ch})}
  function serial(y,m,d){return Math.round((Date.UTC(y,m-1,d)-Date.UTC(1899,11,30))/86400000)}
  function fromSerial(n){var d=new Date(Date.UTC(1899,11,30)+n*86400000);return{y:d.getUTCFullYear(),m:d.getUTCMonth()+1,d:d.getUTCDate()}}
  function p2(n){return(n<10?'0':'')+n}
  function dateStr(n){var o=fromSerial(n);return p2(o.d)+'.'+p2(o.m)+'.'+o.y}
  function parseDate(s){var m=/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/.exec(String(s).trim());return m?serial(+m[3],+m[2],+m[1]):null}
  function ERR(e){return{xl:e}}
  var FN={};
  function alias(ru,en,f){FN[ru.replace(/Ё/g,'Е')]=f;FN[en]=f}
  /* ---------- токенайзер ---------- */
  var RE_SHEET="(?:'[^']+'|[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_.]*)!";
  var RE_REF="\\$?[A-Za-zАВСЕНКМОРТавсенкморт]{1,3}\\$?\\d+";
  var RX_REF=new RegExp('^('+RE_SHEET+')?('+RE_REF+')(?::('+RE_REF+'))?(?![A-Za-zА-Яа-яЁё0-9_(])');
  function tok(src,semi){var t=[],i=0;
    while(i<src.length){var ch=src[i],m,rest=src.slice(i);
      if(/\s/.test(ch)){i++;continue}
      if(ch==='"'){var j=i+1,s='';while(j<src.length){if(src[j]==='"'){if(src[j+1]==='"'){s+='"';j+=2;continue}break}s+=src[j++]}if(j>=src.length)throw ERR('#ИМЯ?');t.push({k:'s',v:s});i=j+1;continue}
      if((m=RX_REF.exec(rest))){t.push({k:'r',sh:m[1]?m[1].slice(0,-1).replace(/^'|'$/g,''):null,a:m[2],b:m[3]||null});i+=m[0].length;continue}
      if((m=/^\d+(?:[.,]\d+)?|^[.,]\d+/.exec(rest))&&(!/^,/.test(m[0])||semi)&&(/^\d/.test(m[0])||semi)){t.push({k:'n',v:parseFloat(m[0].replace(',','.'))});i+=m[0].length;continue}
      if((m=/^[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_.]*/.exec(rest))){var nm=m[0],after=src.slice(i+nm.length).trim()[0];i+=nm.length;
        if(after==='(')t.push({k:'f',v:nm.toUpperCase().replace(/Ё/g,'Е')});else{var u=nm.toUpperCase();if(u==='ИСТИНА'||u==='TRUE')t.push({k:'b',v:true});else if(u==='ЛОЖЬ'||u==='FALSE')t.push({k:'b',v:false});else throw ERR('#ИМЯ?')}continue}
      if((m=/^(<>|<=|>=|[<>=+\-*\/^&(),;:])/.exec(rest))){t.push({k:'o',v:m[1]});i++;if(m[1].length>1)i++;continue}
      throw ERR('#ИМЯ?')}
    return t}
  /* ---------- парсер ---------- */
  function parse(src){var semi=src.indexOf(';')>=0,t=tok(src,semi),p=0;
    function pk(){return t[p]}function isO(v){return t[p]&&t[p].k==='o'&&t[p].v===v}
    function cmp(){var l=cat();while(t[p]&&t[p].k==='o'&&/^(=|<>|<=|>=|<|>)$/.test(t[p].v)){var o=t[p++].v;l={k:'bin',o:o,l:l,r:cat()}}return l}
    function cat(){var l=add();while(isO('&')){p++;l={k:'bin',o:'&',l:l,r:add()}}return l}
    function add(){var l=mul();while(isO('+')||isO('-')){var o=t[p++].v;l={k:'bin',o:o,l:l,r:mul()}}return l}
    function mul(){var l=pw();while(isO('*')||isO('/')){var o=t[p++].v;l={k:'bin',o:o,l:l,r:pw()}}return l}
    function pw(){var l=un();while(isO('^')){p++;l={k:'bin',o:'^',l:l,r:un()}}return l}
    function un(){if(isO('-')){p++;return{k:'neg',e:un()}}if(isO('+')){p++;return un()}return prim()}
    function prim(){var x=t[p++];if(!x)throw ERR('#ИМЯ?');
      if(x.k==='n'||x.k==='s'||x.k==='b')return{k:'c',v:x.v};
      if(x.k==='r')return{k:'r',sh:x.sh,a:x.a,b:x.b};
      if(x.k==='f'){p++;var args=[];if(isO(')')){p++;return{k:'f',n:x.v,a:args}}
        for(;;){if(isO(';')||isO(',')){args.push({k:'c',v:null});p++;continue}args.push(cmp());if(isO(';')||isO(',')){p++;continue}if(isO(')')){p++;break}throw ERR('#ИМЯ?')}
        return{k:'f',n:x.v,a:args}}
      if(x.k==='o'&&x.v==='('){var e=cmp();if(!isO(')'))throw ERR('#ИМЯ?');p++;return e}
      throw ERR('#ИМЯ?')}
    var r=cmp();if(p<t.length)throw ERR('#ИМЯ?');return r}
  /* ---------- книга ---------- */
  function Book(sheets){this.sheets=sheets;this.memo={};this.stack={};this.ast={}}
  Book.prototype.idx=function(n){for(var i=0;i<this.sheets.length;i++)if(this.sheets[i].n.toLowerCase()===n.toLowerCase())return i;throw ERR('#ССЫЛКА!')};
  Book.prototype.dirty=function(){this.memo={};this.stack={}};
  Book.prototype.raw=function(s,r,c){return this.sheets[s].cells[r+','+c]};
  Book.prototype.get=function(s,r,c){var cell=this.sheets[s].cells[r+','+c];if(cell===undefined||cell===null)return null;
    if(typeof cell==='object'&&cell.f){var key=s+','+r+','+c;if(key in this.memo)return this.memo[key];if(this.stack[key])return{e:'#ССЫЛКА!'};this.stack[key]=1;var v;
      try{var ast=this.ast[cell.f]||(this.ast[cell.f]=parse(cell.f.slice(1)));v=this.ev(ast,s,r,c);if(v&&v.rng)v=this.get(v.s,v.r1,v.c1)}catch(e){v=e&&e.xl?{e:e.xl}:{e:'#ЗНАЧ!'}}
      delete this.stack[key];this.memo[key]=v;return v}
    return cell};
  function sc(b,v){if(v&&v.rng)v=b.get(v.s,v.r1,v.c1);if(v&&v.e)throw ERR(v.e);return v}
  function num(b,v){v=sc(b,v);if(v===null||v==='')return 0;if(typeof v==='boolean')return v?1:0;if(typeof v==='number')return v;var n=Number(String(v).replace(',','.'));if(isNaN(n)){var d=parseDate(v);if(d!==null)return d;throw ERR('#ЗНАЧ!')}return n}
  function str(b,v){v=sc(b,v);if(v===null)return'';if(typeof v==='boolean')return v?'ИСТИНА':'ЛОЖЬ';return typeof v==='number'?fmtNum(v):String(v)}
  function fmtNum(n){if(Math.abs(n-Math.round(n))<1e-9)return String(Math.round(n));return String(parseFloat(n.toPrecision(12))).replace('.',',')}
  function rngOf(b,x,s0){var s=x.sh?b.idx(x.sh):s0,a=/^\$?([A-Za-z]+)\$?(\d+)$/.exec(lat(x.a)),c=x.b?/^\$?([A-Za-z]+)\$?(\d+)$/.exec(lat(x.b)):a,r1=+a[2]-1,c1=colNum(a[1]),r2=+c[2]-1,c2=colNum(c[1]);
    return{rng:1,s:s,r1:Math.min(r1,r2),c1:Math.min(c1,c2),r2:Math.max(r1,r2),c2:Math.max(c1,c2)}}
  function cells(b,R){var out=[],m=Math.min(R.r2,b.sheets[R.s].maxR-1);for(var r=R.r1;r<=m;r++)for(var c=R.c1;c<=R.c2;c++)out.push(b.get(R.s,r,c));return out}
  function flat(b,args){var o=[];args.forEach(function(a){if(a&&a.rng)cells(b,a).forEach(function(v){o.push(v)});else o.push(a)});return o}
  function cmpv(a,b){if(typeof a==='string'&&typeof b==='string'){a=a.toLowerCase();b=b.toLowerCase()}return a<b?-1:a>b?1:0}
  function ev2(b,o,l,r){l=sc(b,l);r=sc(b,r);if(l===null)l=typeof r==='string'?'':0;if(r===null)r=typeof l==='string'?'':0;
    var rk=function(v){return typeof v==='number'?0:typeof v==='string'?1:2};var d=rk(l)!==rk(r)?rk(l)-rk(r):cmpv(l,r);
    return o==='='?d===0:o==='<>'?d!==0:o==='<'?d<0:o==='>'?d>0:o==='<='?d<=0:d>=0}
  Book.prototype.ev=function(n,s,r,c){var b=this;
    switch(n.k){case'c':return n.v;case'r':return rngOf(b,n,s);
      case'neg':return-num(b,b.ev(n.e,s,r,c));
      case'bin':{var l=b.ev(n.l,s,r,c),rr=b.ev(n.r,s,r,c),o=n.o;
        if(/^(=|<>|<=|>=|<|>)$/.test(o))return ev2(b,o,l,rr);if(o==='&')return str(b,l)+str(b,rr);
        var x=num(b,l),y=num(b,rr);if(o==='+')return x+y;if(o==='-')return x-y;if(o==='*')return x*y;if(o==='^')return Math.pow(x,y);if(y===0)throw ERR('#ДЕЛ/0!');return x/y}
      case'f':{var f=FN[n.n];if(!f)throw ERR('#ИМЯ?');return f(b,n.a,s,r,c)}}};
  function ea(b,a,i,s,r,c){return b.ev(a[i],s,r,c)}
  function critFn(b,cv){cv=sc(b,cv);
    if(typeof cv==='number')return function(v){return typeof v==='number'&&v===cv};
    if(cv===null)cv='';var m=/^(<=|>=|<>|<|>|=)?([\s\S]*)$/.exec(String(cv)),op=m[1]||'=',rest=m[2],nu=null;
    if(rest!==''){var dd=parseDate(rest);nu=dd!==null?dd:(!isNaN(Number(rest.replace(',','.')))?Number(rest.replace(',','.')):null)}
    if(nu!==null)return function(v){if(typeof v!=='number'){return op==='<>'}return op==='='?v===nu:op==='<>'?v!==nu:op==='<'?v<nu:op==='>'?v>nu:op==='<='?v<=nu:v>=nu};
    var rx=new RegExp('^'+rest.replace(/[.+^${}()|[\]\\]/g,'\\$&').replace(/\*/g,'.*').replace(/\?/g,'.')+'$','i');
    return function(v){var t=v===null?'':typeof v==='number'?fmtNum(v):String(v);if(op==='=')return rx.test(t);if(op==='<>')return!rx.test(t);return false}}
  function ifs(b,a,s,r,c,from,fn){var sumR=from?b.ev(a[0],s,r,c):null,pairs=[];
    for(var i=from;i+1<a.length;i+=2){var R=b.ev(a[i],s,r,c);if(!R||!R.rng)throw ERR('#ЗНАЧ!');pairs.push([R,critFn(b,b.ev(a[i+1],s,r,c))])}
    if(!pairs.length)throw ERR('#ЗНАЧ!');var base=pairs[0][0],H=Math.min(base.r2,b.sheets[base.s].maxR-1)-base.r1,W=base.c2-base.c1;
    for(var dr=0;dr<=H;dr++)for(var dc=0;dc<=W;dc++){var ok=true;for(var q=0;q<pairs.length&&ok;q++){var P=pairs[q][0];ok=pairs[q][1](b.get(P.s,P.r1+dr,P.c1+dc))}
      if(ok)fn(sumR?b.get(sumR.s,sumR.r1+dr,sumR.c1+dc):null)}}
  alias('СУММ','SUM',function(b,a,s,r,c){var t=0;flat(b,a.map(function(x){return b.ev(x,s,r,c)})).forEach(function(v){if(v&&v.e)throw ERR(v.e);if(typeof v==='number')t+=v;else if(typeof v==='boolean')t+=v?1:0});return t});
  alias('СЧЁТ','COUNT',function(b,a,s,r,c){var t=0;flat(b,a.map(function(x){return b.ev(x,s,r,c)})).forEach(function(v){if(typeof v==='number')t++});return t});
  alias('СЧЁТЗ','COUNTA',function(b,a,s,r,c){var t=0;flat(b,a.map(function(x){return b.ev(x,s,r,c)})).forEach(function(v){if(v!==null&&v!=='')t++});return t});
  alias('МАКС','MAX',function(b,a,s,r,c){var m=null;flat(b,a.map(function(x){return b.ev(x,s,r,c)})).forEach(function(v){if(typeof v==='number'&&(m===null||v>m))m=v});return m===null?0:m});
  alias('МИН','MIN',function(b,a,s,r,c){var m=null;flat(b,a.map(function(x){return b.ev(x,s,r,c)})).forEach(function(v){if(typeof v==='number'&&(m===null||v<m))m=v});return m===null?0:m});
  alias('СРЗНАЧ','AVERAGE',function(b,a,s,r,c){var t=0,n=0;flat(b,a.map(function(x){return b.ev(x,s,r,c)})).forEach(function(v){if(typeof v==='number'){t+=v;n++}});if(!n)throw ERR('#ДЕЛ/0!');return t/n});
  alias('ЕСЛИ','IF',function(b,a,s,r,c){var t=ea(b,a,0,s,r,c);t=sc(b,t);var ok=typeof t==='number'?t!==0:typeof t==='boolean'?t:(function(){throw ERR('#ЗНАЧ!')})();if(ok)return a[1]?sc(b,ea(b,a,1,s,r,c)):true;return a[2]?sc(b,ea(b,a,2,s,r,c)):false});
  alias('ЕСЛИОШИБКА','IFERROR',function(b,a,s,r,c){try{return sc(b,ea(b,a,0,s,r,c))}catch(e){return sc(b,ea(b,a,1,s,r,c))}});
  alias('И','AND',function(b,a,s,r,c){return flat(b,a.map(function(x){return b.ev(x,s,r,c)})).every(function(v){return v===true||(typeof v==='number'&&v!==0)})});
  alias('ИЛИ','OR',function(b,a,s,r,c){return flat(b,a.map(function(x){return b.ev(x,s,r,c)})).some(function(v){return v===true||(typeof v==='number'&&v!==0)})});
  alias('НЕ','NOT',function(b,a,s,r,c){var v=sc(b,ea(b,a,0,s,r,c));return!(v===true||(typeof v==='number'&&v!==0))});
  alias('ДАТА','DATE',function(b,a,s,r,c){return serial(num(b,ea(b,a,0,s,r,c)),num(b,ea(b,a,1,s,r,c)),num(b,ea(b,a,2,s,r,c)))});
  alias('ГОД','YEAR',function(b,a,s,r,c){return fromSerial(num(b,ea(b,a,0,s,r,c))).y});alias('МЕСЯЦ','MONTH',function(b,a,s,r,c){return fromSerial(num(b,ea(b,a,0,s,r,c))).m});alias('ДЕНЬ','DAY',function(b,a,s,r,c){return fromSerial(num(b,ea(b,a,0,s,r,c))).d});
  alias('ОКРУГЛ','ROUND',function(b,a,s,r,c){var k=Math.pow(10,a[1]?num(b,ea(b,a,1,s,r,c)):0);return Math.round(num(b,ea(b,a,0,s,r,c))*k)/k});
  alias('ДЛСТР','LEN',function(b,a,s,r,c){return str(b,ea(b,a,0,s,r,c)).length});
  alias('ЛЕВСИМВ','LEFT',function(b,a,s,r,c){return str(b,ea(b,a,0,s,r,c)).slice(0,a[1]?num(b,ea(b,a,1,s,r,c)):1)});
  alias('СЦЕПИТЬ','CONCATENATE',function(b,a,s,r,c){return a.map(function(x){return str(b,b.ev(x,s,r,c))}).join('')});
  alias('ВПР','VLOOKUP',function(b,a,s,r,c){var key=sc(b,ea(b,a,0,s,r,c)),T=ea(b,a,1,s,r,c),ix=num(b,ea(b,a,2,s,r,c)),ex=a[3]?sc(b,ea(b,a,3,s,r,c)):true;if(!T.rng)throw ERR('#ЗНАЧ!');
    ex=(ex===false||ex===0);if(ix<1||T.c1+ix-1>T.c2)throw ERR('#ССЫЛКА!');var m=Math.min(T.r2,b.sheets[T.s].maxR-1),best=-1;
    for(var i=T.r1;i<=m;i++){var v=b.get(T.s,i,T.c1);if(v===null)continue;if(ex?(typeof v===typeof key&&cmpv(v,key)===0):(typeof v===typeof key&&cmpv(v,key)<=0)){best=i;if(ex)break}}
    if(best<0)throw ERR('#Н/Д');return b.get(T.s,best,T.c1+ix-1)});
  alias('СУММЕСЛИМН','SUMIFS',function(b,a,s,r,c){var t=0;ifs(b,a,s,r,c,1,function(v){if(typeof v==='number')t+=v});return t});
  alias('СЧЁТЕСЛИМН','COUNTIFS',function(b,a,s,r,c){var t=0;ifs(b,a,s,r,c,0,function(){t++});return t});
  alias('СУММЕСЛИ','SUMIF',function(b,a,s,r,c){var t=0,args=a.length>2?[a[2],a[0],a[1]]:[a[0],a[0],a[1]];ifs(b,args,s,r,c,1,function(v){if(typeof v==='number')t+=v});return t});
  alias('СЧЁТЕСЛИ','COUNTIF',function(b,a,s,r,c){var t=0;ifs(b,a,s,r,c,0,function(){t++});return t});
  alias('СУММПРОИЗВ','SUMPRODUCT',function(b,a,s,r,c){var R=a.map(function(x){return b.ev(x,s,r,c)}),base=R[0],t=0,H=Math.min(base.r2,b.sheets[base.s].maxR-1)-base.r1;
    for(var i=0;i<=H;i++){for(var j=0;j<=base.c2-base.c1;j++){var p=1;R.forEach(function(X){var v=b.get(X.s,X.r1+i,X.c1+j);p*=typeof v==='number'?v:0});t+=p}}return t});
  alias('ПРОМЕЖУТОЧНЫЕ.ИТОГИ','SUBTOTAL',function(b,a,s,r,c){var f=num(b,ea(b,a,0,s,r,c)),R=ea(b,a,1,s,r,c),vis=[];if(!R.rng)throw ERR('#ЗНАЧ!');var sh=b.sheets[R.s],m=Math.min(R.r2,sh.maxR-1);
    for(var i=R.r1;i<=m;i++)if(!(sh.hidden&&sh.hidden[i]))for(var j=R.c1;j<=R.c2;j++){var v=b.get(R.s,i,j);if(typeof v==='number')vis.push(v)}
    var code=f%100,t=0;vis.forEach(function(x){t+=x});return code===9?t:code===1?(vis.length?t/vis.length:0):code===2||code===3?vis.length:code===4?Math.max.apply(null,vis):code===5?Math.min.apply(null,vis):t});
  /* ---------- сдвиг формулы при заполнении вниз ---------- */
  function shiftF(f,dr,dc){return f.split(/("(?:[^"]|"")*")/).map(function(p,i){if(i%2)return p;
    return p.replace(new RegExp('('+RE_SHEET+')?(\\$?)([A-Za-zАВСЕНКМОРТавсенкморт]{1,3})(\\$?)(\\d+)(?![A-Za-zА-Яа-яЁё0-9_(])','g'),function(m,sh,d1,cl,d2,rw){
      var col=cl;if(!d1&&dc)col=colName(Math.max(0,colNum(lat(cl))+dc));var row=d2?rw:String(Math.max(1,+rw+dr));return(sh||'')+d1+col+d2+row})}).join('')}
  function parseRaw(t){t=String(t);if(t.charAt(0)==='=')return{f:t};if(t==='')return null;
    var d=parseDate(t);if(d!==null)return d;var n=Number(t.replace(',','.'));return(t.trim()!==''&&!isNaN(n))?n:t}
  function mkBook(db){var sheets=db.map(function(t){var cs={},R=t.r.length+1;
    t.h.forEach(function(h,c){cs['0,'+c]=h});
    var fmt={};t.r.forEach(function(row,i){row.forEach(function(v,c){if(typeof v==='string'){var d=parseDate(v);if(d!==null){cs[(i+1)+','+c]=d;fmt[c]='d';return}}cs[(i+1)+','+c]=v})});
    return{n:t.n,cells:cs,fmt:fmt,dataR:R,maxR:R+6,maxC:Math.max(t.h.length+7,12),nc:t.h.length,hidden:{},filters:[]}});
    return new Book(sheets)}
  function disp(b,s,r,c){var v=b.get(s,r,c);if(v===null)return'';if(v.e)return v.e;if(typeof v==='boolean')return v?'ИСТИНА':'ЛОЖЬ';
    if(typeof v==='number'){var sh=b.sheets[s];var cell=sh.cells[r+','+c];if(sh.fmt[c]==='d'&&r>0&&!(cell&&cell.f))return dateStr(v);return fmtNum(v)}return String(v)}
  window.exXl={mkBook:mkBook,parseRaw:parseRaw,shiftF:shiftF,disp:disp,colName:colName,parse:parse,serial:serial,dateStr:dateStr,parseDate:parseDate};
  /* ---------- интерфейс ---------- */
  var EXSH={},HAS=typeof document!=='undefined';
  function applyFilters(b,sh){sh.hidden={};sh.filters.forEach(function(f){for(var r=1;r<sh.dataR;r++){var v=b.get(b.sheets.indexOf(sh),r,f.c);if(!passF(f,v))sh.hidden[r]=1}})}
  function passF(f,v){var t=v===null?'':typeof v==='number'?fmtNum(v):String(v),n=typeof v==='number'?v:null,a=pv(f.v1),z=pv(f.v2);
    if(f.op==='eq')return a.n!==null&&n!==null?n===a.n:t.toLowerCase()===String(f.v1).toLowerCase();
    if(f.op==='st')return t.toLowerCase().indexOf(String(f.v1).toLowerCase())===0;
    if(f.op==='ct')return t.toLowerCase().indexOf(String(f.v1).toLowerCase())>=0;
    if(n===null)return false;if(f.op==='ge')return n>=a.n;if(f.op==='le')return n<=a.n;if(f.op==='bw')return n>=a.n&&n<=z.n;return true}
  function pv(s){s=String(s||'').trim();var d=parseDate(s);if(d!==null)return{n:d};var n=Number(s.replace(',','.'));return{n:(s!==''&&!isNaN(n))?n:null}}
  var OPS=[['eq','равно'],['st','начинается с'],['ct','содержит'],['ge','не меньше (≥)'],['le','не больше (≤)'],['bw','между']];
  /* ---------- подсказки по функциям ---------- */
  var FNH=[
    ['СУММ','SUM','число1; число2; …','Складывает числа и диапазоны'],
    ['СЧЁТ','COUNT','диапазон','Сколько в диапазоне чисел'],
    ['СЧЁТЗ','COUNTA','диапазон','Сколько непустых ячеек'],
    ['МАКС','MAX','диапазон','Наибольшее число'],
    ['МИН','MIN','диапазон','Наименьшее число'],
    ['СРЗНАЧ','AVERAGE','диапазон','Среднее арифметическое'],
    ['ЕСЛИ','IF','условие; если_да; если_нет','Выбирает одно из двух значений'],
    ['ЕСЛИОШИБКА','IFERROR','значение; если_ошибка','Подставляет значение, если получилась ошибка'],
    ['И','AND','условие1; условие2; …','ИСТИНА, если верны все условия'],
    ['ИЛИ','OR','условие1; условие2; …','ИСТИНА, если верно хотя бы одно'],
    ['НЕ','NOT','условие','Меняет ИСТИНА на ЛОЖЬ и наоборот'],
    ['ДАТА','DATE','год; месяц; день','Собирает дату из трёх чисел'],
    ['ГОД','YEAR','дата','Год из даты'],
    ['МЕСЯЦ','MONTH','дата','Номер месяца из даты'],
    ['ДЕНЬ','DAY','дата','День месяца из даты'],
    ['ОКРУГЛ','ROUND','число; знаков','Округляет до нужного числа знаков'],
    ['ДЛСТР','LEN','текст','Длина текста'],
    ['ЛЕВСИМВ','LEFT','текст; сколько','Первые символы текста'],
    ['СЦЕПИТЬ','CONCATENATE','текст1; текст2; …','Склеивает текст'],
    ['ВПР','VLOOKUP','что_искать; таблица; номер_столбца; ЛОЖЬ','Ищет значение в первом столбце таблицы и берёт данные из нужного столбца той же строки'],
    ['СУММЕСЛИМН','SUMIFS','что_суммировать; диапазон1; условие1; …','Сумма по нескольким условиям'],
    ['СЧЁТЕСЛИМН','COUNTIFS','диапазон1; условие1; …','Сколько строк подходит под все условия'],
    ['СУММЕСЛИ','SUMIF','диапазон; условие; что_суммировать','Сумма по одному условию'],
    ['СЧЁТЕСЛИ','COUNTIF','диапазон; условие','Сколько ячеек подходит под условие'],
    ['СУММПРОИЗВ','SUMPRODUCT','массив1; массив2; …','Сумма попарных произведений'],
    ['ПРОМЕЖУТОЧНЫЕ.ИТОГИ','SUBTOTAL','9; диапазон','Итог по видимым строкам (9 — сумма)']
  ];
  function nrm(s){return s.toUpperCase().replace(/Ё/g,'Е')}
  function quoteSh(n){return /^[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_.]*$/.test(n)?n:"'"+n+"'"}
  function fixParens(t){var d=0,q=false;for(var i=0;i<t.length;i++){var ch=t[i];if(ch==='"')q=!q;else if(!q){if(ch==='(')d++;else if(ch===')'&&d>0)d--}}if(q)t+='"';while(d-->0)t+=')';return t}
  var ICO_FILL='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v11M6 9l6 6 6-6M5 20h14"/></svg>';
  var ICO_ALL='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4l6 6 6-6M6 12l6 6 6-6"/></svg>';
  var ICO_FILT='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h18l-7 8v6l-4 2v-8z"/></svg>';
  var ICO_RST='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5"/></svg>';
  window.exSheetInit=function(key,q){if(!HAS)return;var box=$('exsh'),btn=$('exbs');if(!box||!btn||!q.db)return;
    var st=EXSH[key];if(!st){st={book:mkBook(q.db),si:0,sel:[1,0],end:[1,0],fo:false,ed:null,pt:null,ins:null};EXSH[key]=st}
    st.ed=null;st.pt=null;st.ins=null;
    var B=st.book,inp,hint,gr,tdl=[],drag=null,down=null,scrollT=null,lastP=null,built=false;
    function sh(i){return B.sheets[i==null?st.si:i]}
    function rawAt(si,r,c){var S=sh(si),x=S.cells[r+','+c];return x===undefined||x===null?'':(typeof x==='object'?x.f:(S.fmt[c]==='d'&&r>0&&typeof x==='number'?dateStr(x):String(x)))}
    function setCell(si,r,c,text){var S=sh(si),v=parseRaw(text);if(v===null)delete S.cells[r+','+c];else S.cells[r+','+c]=v;if(r>0&&typeof v==='number')delete S.fmt[c]}
    function rg(){var a=st.sel,b2=st.end;return{r1:Math.min(a[0],b2[0]),r2:Math.max(a[0],b2[0]),c1:Math.min(a[1],b2[1]),c2:Math.max(a[1],b2[1])}}
    function selSi(){return st.ed?st.ed.si:st.si}
    function addr(r,c){return colName(c)+(r+1)}
    /* ---------- каркас (строится один раз, поле ввода не пересоздаётся) ---------- */
    function build(){
      box.innerHTML='<div id="xz1"></div><div id="xz2"></div>'+
        '<div class="exxbar"><span class="exxad" id="xad"></span><input id="xin" class="exxin" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="done" placeholder="Значение или =формула" aria-label="Строка формул">'+
        '<button class="exxi sm" id="xab" title="Закрепить ссылку ($)" aria-label="Закрепить ссылку" hidden>$</button>'+
        '<button class="exxi sm" id="xall" title="Записать во все выделенные ячейки" aria-label="Записать во все выделенные ячейки" hidden>'+ICO_ALL+'</button>'+
        '<button class="exxi sm ok" id="xok" title="Готово" aria-label="Готово" hidden>✓</button></div>'+
        '<div class="exxhint" id="xhint" hidden></div><div id="xz4"></div><div id="xz5"></div>';
      inp=$('xin');hint=$('xhint');built=true;
      ['xab','xall','xok'].forEach(function(id){$(id).addEventListener('mousedown',function(e){e.preventDefault()})});
      hint.addEventListener('mousedown',function(e){e.preventDefault()});
      inp.addEventListener('focus',function(){beginEdit();updateHint();syncBtns()});
      inp.addEventListener('input',function(){beginEdit();st.ins=null;updateHint();syncBtns()});
      inp.addEventListener('keyup',function(e){if(e.key.indexOf('Arrow')===0||e.key==='Home'||e.key==='End')updateHint()});
      inp.addEventListener('click',function(){st.ins=null;updateHint()});
      inp.addEventListener('blur',function(){setTimeout(function(){if(document.activeElement===inp)return;if(st.inBox&&Date.now()-st.inBox<500)return;if(st.ed){finish(true,false);drawGrid();syncBar()}hideHint();syncBtns()},60)});
      inp.addEventListener('keydown',function(e){
        if(e.key==='Enter'){e.preventDefault();if(e.ctrlKey||e.metaKey){fillAll()}else{finish(true,true);move(1,0)}}
        else if(e.key==='Escape'){cancelEdit();inp.blur()}
        else if(e.key==='Tab'){e.preventDefault();finish(true,true);move(0,e.shiftKey?-1:1)}
        else if(e.key==='F4'){e.preventDefault();toggleAbs()}});
      $('xok').onclick=function(){finish(true,true);drawGrid();syncBar();inp.blur()};
      $('xall').onclick=fillAll;$('xab').onclick=toggleAbs;
      hint.addEventListener('click',function(e){var b2=e.target.closest('.exxs');if(!b2)return;pickFn(+b2.dataset.i,b2.dataset.nm)})}
    function beginEdit(){if(!st.ed)st.ed={si:st.si,r:st.sel[0],c:st.sel[1]}}
    function cancelEdit(){if(!st.ed)return;var e=st.ed;st.ed=null;st.pt=null;st.ins=null;st.si=e.si;st.sel=[e.r,e.c];st.end=[e.r,e.c];hideHint();draw()}
    function finish(apply,goBack){var e=st.ed;if(!e)return;
      if(apply){var old=rawAt(e.si,e.r,e.c),v=inp.value;if(v!==old){if(v.charAt(0)==='=')v=fixParens(v);setCell(e.si,e.r,e.c,v)}}
      st.ed=null;st.pt=null;st.ins=null;if(goBack&&st.si!==e.si){st.si=e.si;draw()}
      if(goBack){st.sel=[e.r,e.c];st.end=[e.r,e.c];st.colSel=false}
      hideHint()}
    function move(dr,dc){var S=sh();st.sel=[Math.max(0,Math.min(S.maxR-1,st.sel[0]+dr)),Math.max(0,Math.min(S.maxC-1,st.sel[1]+dc))];st.end=st.sel.slice();st.colSel=false;draw();inp.value=rawAt(st.si,st.sel[0],st.sel[1]);if(!/Mobi|Android/i.test(navigator.userAgent))inp.focus()}
    /* ---------- отрисовка ---------- */
    function draw(){B.dirty();B.sheets.forEach(function(x){applyFilters(B,x)});B.dirty();drawTabs();drawFilter();drawGrid();syncBar()}
    function drawTabs(){var z=$('xz1');z.innerHTML='<div class="exxtabs">'+B.sheets.map(function(x,i){return'<button class="exxt'+(i===st.si?' on':'')+'" data-s="'+i+'">'+esc(x.n)+'</button>'}).join('')+'</div>';
      z.querySelectorAll('.exxt').forEach(function(b2){b2.addEventListener('mousedown',function(e){if(st.ed)e.preventDefault()});b2.onclick=function(){st.inBox=Date.now();if(st.ed){st.si=+b2.dataset.s;B.dirty();drawTabs();drawFilter();drawGrid();return}
        st.si=+b2.dataset.s;st.sel=[1,0];st.end=[1,0];st.colSel=false;draw();inp.value=rawAt(st.si,1,0)}})}
    function drawFilter(){var S=sh(),R=rg(),z=$('xz2'),h='';
      if(st.fo){h+='<div class="exxfp"><select id="xfc">'+Array.apply(null,{length:S.nc}).map(function(_,c){return'<option value="'+c+'"'+(R.c1===c?' selected':'')+'>'+colName(c)+': '+esc(String(S.cells['0,'+c]))+'</option>'}).join('')+'</select><select id="xfp">'+OPS.map(function(o){return'<option value="'+o[0]+'">'+o[1]+'</option>'}).join('')+'</select><input id="xf1" placeholder="значение"><input id="xf2" placeholder="и до" hidden><button class="exxb" id="xfa">Добавить</button></div>'}
      if(S.filters.length)h+='<div class="exxfl">'+S.filters.map(function(f,i){return'<span class="exxch">'+colName(f.c)+' '+OPS.filter(function(o){return o[0]===f.op})[0][1]+' '+esc(f.v1)+(f.op==='bw'?' … '+esc(f.v2):'')+' <button data-x="'+i+'" aria-label="Убрать фильтр">×</button></span>'}).join('')+'</div>';
      z.innerHTML=h;
      if(st.fo){var fp=$('xfp');fp.onchange=function(){$('xf2').hidden=fp.value!=='bw'};
        $('xfa').onclick=function(){var v1=$('xf1').value;if(!v1)return;S.filters.push({c:+$('xfc').value,op:fp.value,v1:v1,v2:$('xf2').value});draw()}}
      z.querySelectorAll('.exxch button').forEach(function(b2){b2.onclick=function(){S.filters.splice(+b2.dataset.x,1);draw()}})}
    function drawGrid(){var S=sh(),h='';
      h+='<div class="exxgrid" id="xgr" tabindex="0"><div class="exxwrap"><table class="exxtab"><tr><th class="c0"></th>'+Array.apply(null,{length:S.maxC}).map(function(_,c){return'<th class="ch" data-c="'+c+'">'+colName(c)+'</th>'}).join('')+'</tr>';
      for(var r=0;r<S.maxR;r++){if(S.hidden[r])continue;h+='<tr><th class="rh" data-r="'+r+'">'+(r+1)+'</th>';
        for(var c=0;c<S.maxC;c++){var v=B.get(st.si,r,c),cls=(r===0?'hd ':'')+(typeof v==='number'?'nu ':'')+(v&&v.e?'er':'');
          h+='<td class="'+cls+'" data-r="'+r+'" data-c="'+c+'">'+esc(disp(B,st.si,r,c))+'</td>'}h+='</tr>'}
      h+='</table><div class="exxhd" id="xhd" hidden></div></div></div>';
      $('xz4').innerHTML=h;gr=$('xgr');
      tdl=[];gr.querySelectorAll('td').forEach(function(t){tdl.push({el:t,r:+t.dataset.r,c:+t.dataset.c})});
      var z5='<div class="exxbot"><div class="exxst" id="xst"></div><div class="exxtool"><button class="exxi" id="xfo" aria-pressed="'+st.fo+'" title="Фильтр" aria-label="Фильтр">'+ICO_FILT+'</button><button class="exxi" id="xfd" title="Заполнить вниз" aria-label="Заполнить вниз">'+ICO_FILL+'</button><button class="exxi" id="xrs" title="Сбросить" aria-label="Сбросить">'+ICO_RST+'</button></div></div>'+
        '<details class="exxh"><summary>Как пользоваться</summary><p>Тап по ячейке — выбрать; значение или формулу вводи в строке сверху. Пока пишешь формулу, подсказка предложит функции и покажет аргументы. После «(» или «;» тапай ячейки или тяни за уголок — ссылка подставится сама; можно переключать листы. «$» закрепляет ссылку. Тап по букве столбца выделяет столбец; формулу из строки можно записать во все выделенные ячейки (кнопка «⇊»). Потяни за уголок выделенной ячейки вниз или вправо — заполнение, как в Excel.</p></details>';
      $('xz5').innerHTML=z5;
      $('xfo').onclick=function(){finishKeep();st.fo=!st.fo;drawFilter();$('xfo').setAttribute('aria-pressed',st.fo)};
      $('xrs').onclick=function(){if(confirm('Сбросить все изменения таблицы в этом задании?')){delete EXSH[key];exSheetInit(key,q)}};
      $('xfd').onclick=fillDown;
      ['xfo','xfd','xrs'].forEach(function(id){$(id).addEventListener('mousedown',function(e){if(st.ed)e.preventDefault()})});
      bindGrid();paint()}
    function finishKeep(){if(st.ed){finish(true,false);drawGrid()}}
    function syncBar(){var e=st.ed,a=e?addr(e.r,e.c):addr(st.sel[0],st.sel[1]);$('xad').textContent=a;if(!e&&document.activeElement!==inp)inp.value=rawAt(st.si,st.sel[0],st.sel[1]);syncBtns()}
    function syncBtns(){var ed=!!st.ed&&(document.activeElement===inp||st.pt),R=rg(),multi=R.r1!==R.r2||R.c1!==R.c2;
      $('xok').hidden=!ed;$('xab').hidden=!(ed&&inp.value.charAt(0)==='=');$('xall').hidden=!(ed&&multi&&!st.pt)}
    /* ---------- выделение ---------- */
    function activeRange(){if(st.ed&&st.pt)return st.pt;return st.si===selSi()?Object.assign({si:st.si},rg()):null}
    function paint(){var showSel=st.si===selSi(),R=rg(),P=st.pt&&st.pt.si===st.si?st.pt:null,i;
      for(i=0;i<tdl.length;i++){var o=tdl[i],e=o.el,inR=showSel&&o.r>=R.r1&&o.r<=R.r2&&o.c>=R.c1&&o.c<=R.c2,isS=showSel&&o.r===st.sel[0]&&o.c===st.sel[1],inP=P&&o.r>=P.r1&&o.r<=P.r2&&o.c>=P.c1&&o.c<=P.c2;
        e.classList.toggle('rg',!!inR);e.classList.toggle('sel',!!isS);e.classList.toggle('pt',!!inP)}
      gr.querySelectorAll('th.ch').forEach(function(t){var c=+t.dataset.c;t.classList.toggle('on',!!(showSel&&st.colSel&&c>=R.c1&&c<=R.c2))});
      var A=activeRange(),S=sh(),nums=[],cnt=0;
      if(A&&A.si===st.si){for(var rr=A.r1;rr<=A.r2;rr++){if(S.hidden[rr])continue;for(var cc=A.c1;cc<=A.c2;cc++){var vv=B.get(st.si,rr,cc);if(vv!==null&&vv!==''&&!(vv&&vv.e)){cnt++;if(typeof vv==='number')nums.push(vv)}}}}
      var tot=0;nums.forEach(function(x){tot+=x});var hid=Object.keys(S.hidden).length;
      $('xst').innerHTML=(nums.length?'<span>Знач. <b>'+cnt+'</b></span><span>Σ <b>'+fmtNum(tot)+'</b></span><span>Среднее <b>'+fmtNum(Math.round(tot/nums.length*1000)/1000)+'</b></span>':'<span>Знач. <b>'+cnt+'</b></span>')+(hid?'<span>скрыто <b>'+hid+'</b></span>':'');
      placeHandle(A)}
    function tdAt(r,c){return gr.querySelector('td[data-r="'+r+'"][data-c="'+c+'"]')}
    function placeHandle(A){var hd=$('xhd');if(!hd)return;var t=A&&A.si===st.si?tdAt(A.r2,A.c2):null;if(!t){hd.hidden=true;return}
      var wr=gr.firstChild.getBoundingClientRect(),tr=t.getBoundingClientRect();hd.hidden=false;hd.style.left=(tr.right-wr.left)+'px';hd.style.top=(tr.bottom-wr.top)+'px';hd.classList.toggle('pt',!!(st.ed&&st.pt))}
    function selectCell(r,c,extend){if(extend){st.end=[r,c]}else{st.sel=[r,c];st.end=[r,c]}st.colSel=false;paint();if(!extend){inp.value=rawAt(st.si,r,c);syncBar()}else syncBtns()}
    /* ---------- режим выбора ссылок для формулы ---------- */
    function inStr(s){var n=0;for(var i=0;i<s.length;i++)if(s[i]==='"')n++;return n%2===1}
    function caret(){return inp.selectionStart==null?inp.value.length:inp.selectionStart}
    function ptOK(){if(!st.ed||inp.value.charAt(0)!=='=')return false;var p=document.activeElement===inp?caret():(st.ins?st.ins.end:inp.value.length),b2=inp.value.slice(0,p);
      if(st.ins&&st.ins.end===p)return true;if(inStr(b2))return false;var ch=b2.replace(/\s+$/,'').slice(-1);return !!ch&&'=(;,+-*/^&<>:'.indexOf(ch)>=0}
    function refText(R){var pre=R.si!==st.ed.si?quoteSh(sh(R.si).n)+'!':'',a=addr(R.r1,R.c1);return pre+(R.r1===R.r2&&R.c1===R.c2?a:a+':'+addr(R.r2,R.c2))}
    function insertRef(R){var v=inp.value,p=(document.activeElement===inp)?caret():(st.ins?st.ins.end:v.length),t=refText(R),s0=p,e0=p;
      if(st.ins&&st.ins.end===p){s0=st.ins.start;e0=st.ins.end}
      inp.value=v.slice(0,s0)+t+v.slice(e0);var np=s0+t.length;st.ins={start:s0,end:np};
      try{inp.focus({preventScroll:true});inp.setSelectionRange(np,np)}catch(x){}
      updateHint();syncBtns()}
    function mkPt(r1,c1,r2,c2,ar,ac){return{si:st.si,r1:Math.min(r1,r2),c1:Math.min(c1,c2),r2:Math.max(r1,r2),c2:Math.max(c1,c2),ar:ar,ac:ac}}
    function toggleAbs(){var v=inp.value,p=caret(),rx=/((?:'[^']+'|[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_.]*)!)?(\$?[A-Za-zА-Яа-я]{1,3}\$?\d+)(?::(\$?[A-Za-zА-Яа-я]{1,3}\$?\d+))?/g,m,hit=null;
      while((m=rx.exec(v))){if(m.index<=p&&p<=m.index+m[0].length){hit=m;if(m.index+m[0].length===p)break}}
      if(!hit)return;function cyc(x){var q2=/^(\$?)([A-Za-zА-Яа-я]+)(\$?)(\d+)$/.exec(x);if(!q2)return x;var cl=!!q2[1],rw=!!q2[3],ns=!cl&&!rw?[1,1]:cl&&rw?[0,1]:!cl&&rw?[1,0]:[0,0];return(ns[0]?'$':'')+q2[2]+(ns[1]?'$':'')+q2[4]}
      var a=cyc(hit[2]),b2=hit[3]?cyc(hit[3]):null;if(b2&&hit[2]){var f1=/^(\$?)[A-Za-zА-Яа-я]+(\$?)/.exec(a);b2=b2.replace(/^\$?([A-Za-zА-Яа-я]+)\$?(\d+)$/,function(_,L,D){return(f1[1]?'$':'')+L+(f1[2]?'$':'')+D})}
      var t=(hit[1]||'')+a+(b2?':'+b2:'');inp.value=v.slice(0,hit.index)+t+v.slice(hit.index+hit[0].length);var np=hit.index+t.length;st.ins={start:hit.index,end:np};
      inp.focus();inp.setSelectionRange(np,np);updateHint()}
    /* ---------- подсказка функций ---------- */
    function hideHint(){if(hint){hint.hidden=true;hint.innerHTML=''}}
    function updateHint(){if(!hint)return;var v=inp.value;if(v.charAt(0)!=='='||document.activeElement!==inp){hideHint();return}
      var p=caret(),b2=v.slice(0,p);if(inStr(b2)){hideHint();return}
      var m=/([A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё0-9_.]*)$/.exec(b2),h='';
      if(m&&!/[!A-Za-zА-Яа-яЁё0-9_.$']/.test(b2.charAt(m.index-1)||' ')&&!/^[A-Za-zА-Яа-я]{1,3}\d+$/.test(m[1])){
        var tk=nrm(m[1]),cyr=/[А-Яа-яЁё]/.test(m[1].charAt(0)),list=[];
        FNH.forEach(function(f,i){var nm=cyr?f[0]:f[1];if(nrm(nm).indexOf(tk)===0&&nrm(nm)!==tk)list.push(i)});
        if(list.length){h=list.slice(0,5).map(function(i){var f=FNH[i],nm=cyr?f[0]:f[1];return'<button class="exxs" data-i="'+i+'" data-nm="'+esc(nm)+'"><b>'+esc(nm)+'</b><span>'+esc(f[3])+'</span></button>'}).join('')}}
      if(!h){var stack=[],q2=false,tok2='';
        for(var i2=0;i2<b2.length;i2++){var ch=b2[i2];if(ch==='"'){q2=!q2;continue}if(q2)continue;
          if(ch==='('){var mm=/([A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё0-9_.]*)\s*$/.exec(b2.slice(0,i2));stack.push({n:mm?nrm(mm[1]):'',arg:0})}
          else if(ch===')'){stack.pop()}else if((ch===';'||ch===',')&&stack.length)stack[stack.length-1].arg++}
        var top=stack[stack.length-1];
        if(top&&top.n){var fi=-1,en=false;FNH.forEach(function(f,i){if(nrm(f[0])===top.n)fi=i;else if(f[1]===top.n){fi=i;en=true}});
          if(fi>=0){var f2=FNH[fi],parts=f2[2].split('; '),ai=Math.min(top.arg,parts.length-1);
            h='<div class="exxsig"><b>'+esc(en?f2[1]:f2[0])+'</b>('+parts.map(function(x,i){return i===ai?'<u>'+esc(x)+'</u>':esc(x)}).join('; ')+')</div><div class="exxsd">'+esc(f2[3])+'</div>'}}}
      if(h){hint.innerHTML=h;hint.hidden=false}else hideHint()}
    function pickFn(i,nm){var v=inp.value,p=caret(),b2=v.slice(0,p),m=/([A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё0-9_.]*)$/.exec(b2);if(!m)return;
      var s0=m.index,after=v.slice(p);if(after.charAt(0)==='(')after=after.slice(1);inp.value=v.slice(0,s0)+nm+'('+after;var np=s0+nm.length+1;st.ins=null;inp.focus();inp.setSelectionRange(np,np);updateHint();syncBtns()}
    /* ---------- заполнение ---------- */
    function fillCells(S,P){ /* S — исходный диапазон, P — [r,c] до куда тянут */
      var T=sh(),cnt=0,i,j,r,c;
      if(P[0]>S.r2&&(P[0]-S.r2>=P[1]-S.c2||P[1]<=S.c2)){var h2=S.r2-S.r1+1;
        for(c=S.c1;c<=S.c2;c++)for(r=S.r2+1;r<=P[0];r++){var sr=S.r1+((r-S.r1)%h2),src=T.cells[sr+','+c];setOrDel(T,r,c,src,r-sr,0);cnt++}}
      else if(P[1]>S.c2){var w2=S.c2-S.c1+1;
        for(r=S.r1;r<=S.r2;r++)for(c=S.c2+1;c<=P[1];c++){var sc2=S.c1+((c-S.c1)%w2),src2=T.cells[r+','+sc2];setOrDel(T,r,c,src2,0,c-sc2);cnt++}}
      return cnt}
    function setOrDel(T,r,c,src,dr,dc){var k=r+','+c;if(src===undefined||src===null){delete T.cells[k];return}
      if(typeof src==='object'&&src.f)T.cells[k]={f:shiftF(src.f,dr,dc)};else{T.cells[k]=src;if(T.fmt[c]==='d'&&typeof src==='number'){}}}
    function fillDown(){finishKeep();var R=rg(),T=sh(),single=R.r1===R.r2&&R.c1===R.c2;
      if(single){var src=T.cells[R.r1+','+R.c1];if(src===undefined){toast('Сначала введи значение или формулу в ячейку');return}
        if(R.r1===0){toast('Выдели ячейку под заголовком');return}
        fillCells({r1:R.r1,r2:R.r1,c1:R.c1,c2:R.c1},[T.dataR-1,R.c1]);st.sel=[R.r1,R.c1];st.end=[T.dataR-1,R.c1]}
      else{var hasSrc=false;for(var c=R.c1;c<=R.c2;c++)if(T.cells[R.r1+','+c]!==undefined)hasSrc=true;if(!hasSrc){toast('В первой строке выделения пусто');return}
        for(var c2=R.c1;c2<=R.c2;c2++)for(var r=R.r1+1;r<=R.r2;r++)setOrDel(T,r,c2,T.cells[R.r1+','+c2],r-R.r1,0)}
      B.dirty();drawGrid();syncBar()}
    function fillAll(){var e=st.ed||{si:st.si,r:st.sel[0],c:st.sel[1]},R=rg(),text=inp.value,T=sh(e.si),n=0;if(!text){toast('Сначала введи значение или формулу');return}
      if(text.charAt(0)==='=')text=fixParens(text);
      for(var r=R.r1;r<=R.r2;r++)for(var c=R.c1;c<=R.c2;c++){if(r===0&&R.r2>0)continue;var k=r+','+c;
        if(text.charAt(0)==='=')T.cells[k]={f:shiftF(text,r-e.r,c-e.c)};else setCell(e.si,r,c,text);n++}
      st.ed=null;st.pt=null;st.ins=null;hideHint();st.si=e.si;B.dirty();draw();inp.blur();toast('Записано в ячеек: '+n)}
    /* ---------- нажатия и протяжка ---------- */
    function cellFrom(x,y){var els=document.elementsFromPoint(x,y);for(var i=0;i<els.length;i++){var t=els[i].closest&&els[i].closest('td');if(t&&gr.contains(t))return[+t.dataset.r,+t.dataset.c]}return null}
    function cellAct(r,c,shift){ /* возвращает 'pt' или 'sel' */
      if(ptOK()){var P=st.pt;if(shift&&P&&P.si===st.si)st.pt=mkPt(P.ar,P.ac,r,c,P.ar,P.ac);else st.pt=mkPt(r,c,r,c,r,c);insertRef(st.pt);paint();return'pt'}
      finishKeep();if(shift&&st.si===selSi())selectCell(r,c,true);else selectCell(r,c,false);
      if(!/Mobi|Android/i.test(navigator.userAgent)&&!shift)setTimeout(function(){if(!st.ed&&gr&&document.activeElement!==inp){try{inp.focus({preventScroll:true})}catch(x){}}},0);
      return'sel'}
    function headerAct(t){var S=sh();
      if(t.classList.contains('ch')){var c=+t.dataset.c;if(ptOK()){st.pt=mkPt(1,c,S.dataR-1,c,1,c);insertRef(st.pt);paint();return}
        finishKeep();st.sel=[1,c];st.end=[S.dataR-1,c];st.colSel=true;paint();inp.value=rawAt(st.si,1,c);syncBar()}
      else if(t.classList.contains('rh')){var r=+t.dataset.r;if(ptOK()){st.pt=mkPt(r,0,r,S.nc-1,r,0);insertRef(st.pt);paint();return}
        finishKeep();st.sel=[r,0];st.end=[r,S.nc-1];st.colSel=false;paint();inp.value=rawAt(st.si,r,0);syncBar()}}
    function bindGrid(){
      gr.addEventListener('mousedown',function(e){st.inBox=Date.now();if(st.ed)e.preventDefault()});
      gr.addEventListener('pointerdown',function(e){st.inBox=Date.now();
        if(e.target.closest('.exxhd')){e.preventDefault();startHandle(e);return}
        var t=e.target.closest('td,th');if(!t)return;
        if(t.tagName==='TH'){if(e.pointerType==='mouse')headerAct(t);else down={th:t,x:e.clientX,y:e.clientY};return}
        var r=+t.dataset.r,c=+t.dataset.c;
        if(e.pointerType==='mouse'){var md=cellAct(r,c,e.shiftKey);drag={mode:md,sx:r,sy:c};document.addEventListener('pointermove',onMove);document.addEventListener('pointerup',onUp,{once:true})}
        else down={r:r,c:c,x:e.clientX,y:e.clientY}});
      gr.addEventListener('pointermove',function(e){if(down&&Math.abs(e.clientX-down.x)+Math.abs(e.clientY-down.y)>10)down=null});
      gr.addEventListener('pointercancel',function(){down=null});
      gr.addEventListener('pointerup',function(e){if(!down)return;var d=down;down=null;if(Math.abs(e.clientX-d.x)+Math.abs(e.clientY-d.y)>10)return;if(d.th)headerAct(d.th);else cellAct(d.r,d.c,false)});
      gr.onkeydown=function(e){var k=e.key;if(k==='ArrowDown'){e.preventDefault();move(1,0)}else if(k==='ArrowUp'){e.preventDefault();move(-1,0)}else if(k==='ArrowLeft'){e.preventDefault();move(0,-1)}else if(k==='ArrowRight'){e.preventDefault();move(0,1)}
        else if(k==='Delete'){var R=rg(),S=sh();for(var r=R.r1;r<=R.r2;r++)for(var c=R.c1;c<=R.c2;c++)if(r>0)delete S.cells[r+','+c];B.dirty();drawGrid();syncBar()}
        else if(k.length===1&&!e.ctrlKey&&!e.metaKey){beginEdit();inp.value=k;inp.focus();e.preventDefault();updateHint();syncBtns()}}}
    function onMove(e){if(!drag||drag.mode==null||!(e.buttons&1)){return}var P=cellFrom(e.clientX,e.clientY);if(!P)return;
      if(drag.mode==='pt'){var A=st.pt;st.pt=mkPt(A.ar,A.ac,P[0],P[1],A.ar,A.ac);insertRef(st.pt);paint()}else{st.end=[P[0],P[1]];st.colSel=false;paint()}}
    function onUp(){document.removeEventListener('pointermove',onMove);drag=null;syncBtns()}
    function startHandle(e){var edit=!!(st.ed&&st.pt),S0=edit?null:Object.assign({},rg()),T=sh(),hasSrc=false,touch=e.pointerType!=='mouse';
      if(!edit)for(var rr=S0.r1;rr<=S0.r2;rr++)for(var cc=S0.c1;cc<=S0.c2;cc++)if(T.cells[rr+','+cc]!==undefined&&S0.r1>0)hasSrc=true;
      var hd=$('xhd'),last=null;hd.classList.add('drag');
      function mv(ev){lastP=[ev.clientX,ev.clientY];var P=cellFrom(ev.clientX,ev.clientY-(touch?22:0));if(!P)return;last=P;
        if(edit){var A=st.pt;st.pt=mkPt(A.ar,A.ac,P[0],P[1],A.ar,A.ac);insertRef(st.pt);paint()}
        else if(hasSrc){var PP=[Math.max(P[0],S0.r2),Math.max(P[1],S0.c2)];if(PP[0]-S0.r2>=PP[1]-S0.c2)PP[1]=S0.c2;else PP[0]=S0.r2;st.sel=[S0.r1,S0.c1];st.end=[PP[0],PP[1]];paint()}
        else{st.end=[P[0],P[1]];paint()}}
      function up(){document.removeEventListener('pointermove',mv);document.removeEventListener('pointerup',up);document.removeEventListener('pointercancel',up);clearInterval(scrollT);hd.classList.remove('drag');
        if(!edit&&hasSrc&&last){var P2=[st.end[0],st.end[1]];if(P2[0]>S0.r2||P2[1]>S0.c2){fillCells(S0,P2);B.dirty();drawGrid();syncBar()}}syncBtns()}
      document.addEventListener('pointermove',mv);document.addEventListener('pointerup',up);document.addEventListener('pointercancel',up);
      clearInterval(scrollT);scrollT=setInterval(function(){if(!lastP)return;var b2=gr.getBoundingClientRect(),x=lastP[0],y=lastP[1],d=12;
        if(y>b2.bottom-34)gr.scrollTop+=d;else if(y<b2.top+34)gr.scrollTop-=d;if(x>b2.right-34)gr.scrollLeft+=d;else if(x<b2.left+34)gr.scrollLeft-=d},40)}
    document.addEventListener('pointerdown',function(e){if(box.contains(e.target))st.inBox=Date.now()},true);
    btn.onclick=function(){var open=box.hidden;box.hidden=!open;btn.classList.toggle('on',open);btn.setAttribute('aria-pressed',open);if(open){if(!built)build();draw()}};
  };
})();
