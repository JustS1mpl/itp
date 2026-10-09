/* ===== v5.1.1: nonlocal, {**a, **b}, eval/exec, порядок множеств ===== */
/* --- общий проход по тексту: пропускает строки и комментарии, f-строки передаёт на обработку --- */
function itpWalk(src,onId,onFexpr){
  // onId(name, start, end, ctx) -> замена или null; ctx: {prev, next, depth}
  var out='',i=0,n=src.length,depth=0,prevSig='';
  function isIdS(c){return /[A-Za-z_\u0400-\u04FF]/.test(c)}
  function isId(c){return /[\w\u0400-\u04FF]/.test(c)}
  while(i<n){
    var c=src[i];
    if(c==='#'){var e=i;while(e<n&&src[e]!=='\n')e++;out+=src.slice(i,e);i=e;continue}
    // строки с префиксами
    if(isIdS(c)||c==='"'||c==="'"){
      var j=i;while(j<n&&isId(src[j]))j++;
      var word=src.slice(i,j);
      if((src[j]==='"'||src[j]==="'")&&/^(?:[rRbBuUfF]|[rR][bBfF]|[bBfF][rR])?$/.test(word)){
        var isF=/[fF]/.test(word),q=src[j],q3=src.substr(j,3)===q+q+q,qq=q3?q+q+q:q,k=j+qq.length,body='';
        var start=k;
        while(k<n){if(src[k]==='\\'&&!/[rR]/.test(word)){k+=2;continue}if(src.substr(k,qq.length)===qq)break;if(!q3&&src[k]==='\n')break;k++}
        body=src.slice(start,k);
        if(isF&&onFexpr)body=onFexpr(body);
        out+=word+qq+body+(src.substr(k,qq.length)===qq?qq:'');i=k+(src.substr(k,qq.length)===qq?qq.length:0);prevSig='"';continue}
      if(isIdS(c)){
        var nx=j;while(nx<n&&(src[nx]===' '||src[nx]==='\t'))nx++;
        var rep=onId(word,i,j,{prev:prevSig,next:src[nx]||'',next2:src[nx+1]||'',depth:depth,before:src.slice(Math.max(0,i-6),i)});
        out+=rep===null||rep===undefined?word:rep;prevSig=word[word.length-1];i=j;continue}
    }
    if(/[0-9]/.test(c)){var j2=i;while(j2<n&&/[\w.]/.test(src[j2]))j2++;out+=src.slice(i,j2);i=j2;prevSig='0';continue}
    if(c==='('||c==='['||c==='{')depth++;
    if(c===')'||c===']'||c==='}')depth=Math.max(0,depth-1);
    out+=c;if(c!==' '&&c!=='\t'&&c!=='\n')prevSig=c;i++}
  return out}
/* --- nonlocal --- */
function nlT(code){
  if(!/\bnonlocal\b/.test(code))return{code:code,map:null};
  var L=code.split('\n'),ind=function(s){return s.match(/^[ \t]*/)[0].length},blank=function(s){return!s.trim()||/^\s*#/.test(s)};
  var map=L.map(function(x,k){return k+1}),ins=[];
  var guard=0;
  while(guard++<40){
    var ni=-1;for(var a=0;a<L.length;a++)if(/^\s*nonlocal\s+[\w\u0400-\u04FF, ]+\s*(#.*)?$/.test(L[a])){ni=a;break}
    if(ni<0)break;
    var names=L[ni].replace(/#.*/,'').trim().slice(8).split(',').map(function(x){return x.trim()}).filter(Boolean);
    var base=ind(L[ni]),di=-1;
    for(var b=ni-1;b>=0;b--){if(blank(L[b]))continue;if(ind(L[b])<base&&/^\s*(async\s+)?def\s/.test(L[b])){di=b;break}if(ind(L[b])<base&&!/^\s*(@|#)/.test(L[b])&&/^\s*(def|class)\s/.test(L[b])===false)continue}
    var oi=-1;
    if(di>=0){var dind=ind(L[di]);for(var b2=di-1;b2>=0;b2--){if(blank(L[b2]))continue;if(ind(L[b2])<dind&&/^\s*(async\s+)?def\s/.test(L[b2])){oi=b2;break}}}
    if(oi<0){L[ni]=L[ni].replace(/nonlocal.*$/,'pass');continue}
    var oind=ind(L[oi]),end=oi+1;
    while(end<L.length&&(blank(L[end])||ind(L[end])>oind))end++;
    // конец заголовка внешней функции
    var he=oi,dd=0;
    for(;he<end;he++){var t=L[he].replace(/#.*/,'');for(var z=0;z<t.length;z++){if('([{'.indexOf(t[z])>=0)dd++;if(')]}'.indexOf(t[z])>=0)dd--}if(dd<=0&&/:\s*$/.test(t))break}
    var hdr=L.slice(oi,he+1).join(' '),pm=/\(([^)]*)\)/.exec(hdr),params=pm?pm[1].split(',').map(function(x){return x.split('=')[0].split(':')[0].replace(/[*]/g,'').trim()}):[];
    var bodyInd=ind(L[he+1]||'')||oind+4;
    var inits=[];
    names.forEach(function(nm){inits.push(' '.repeat(bodyInd)+'__nl_'+nm+' = ['+(params.indexOf(nm)>=0?nm:'None')+']')});
    var body=L.slice(he+1,end).map(function(x,k){return L[he+1+k]});
    // замены имён в теле
    var txt=body.join('\n'),set={};names.forEach(function(nm){set[nm]=1});
    var ren=function(s){return itpWalk(s,function(w,st,en,cx){
        if(!set[w])return null;
        if(cx.prev==='.')return null;
        if(/def\s*$/.test(cx.before)||/class\s*$/.test(cx.before))return null;
        if(cx.depth>0&&(cx.prev==='('||cx.prev===',')&&cx.next==='='&&cx.next2!=='=')return null;
        return '__nl_'+w+'[0]'},function(fb){
        // выражения внутри {..} f-строки
        var o='',i=0;while(i<fb.length){if(fb[i]==='{'){if(fb[i+1]==='{'){o+='{{';i+=2;continue}var d=1,j=i+1;while(j<fb.length&&d>0){if(fb[j]==='{')d++;else if(fb[j]==='}')d--;j++}
            var inner=fb.slice(i+1,j-1),m=/^(.*?)(![rsa])?(:.*)?$/.exec(inner);o+='{'+ren(m[1])+(m[2]||'')+(m[3]||'')+'}';i=j;continue}o+=fb[i];i++}return o})};
    // заголовки вложенных def: не трогаем параметры (itpWalk увидит def NAME(..); параметры совпадающие с именем остаются глобальными для этой функции)
    var newTxt=ren(txt).split('\n');
    for(var q=0;q<newTxt.length;q++)L[he+1+q]=newTxt[q];
    // убрать все nonlocal строки внутри диапазона для этих имён
    for(var r=he+1;r<end;r++)if(/^\s*nonlocal\s/.test(L[r]))L[r]=L[r].replace(/nonlocal.*$/,'pass');
    var at=he+1;Array.prototype.splice.apply(L,[at,0].concat(inits));Array.prototype.splice.apply(map,[at,0].concat(inits.map(function(){return map[he]})));
  }
  return{code:L.join('\n'),map:map}}
/* --- {**a, **b} --- */
function dmT(code){
  if(code.indexOf('**')<0)return{code:code,map:null};
  function split(s){var r=[],d=0,cur='',q=null;for(var k=0;k<s.length;k++){var c=s[k];if(q){cur+=c;if(c==='\\'){cur+=s[++k]||''}else if(c===q)q=null;continue}if(c==='"'||c==="'"){q=c;cur+=c;continue}if('([{'.indexOf(c)>=0)d++;if(')]}'.indexOf(c)>=0)d--;if(c===','&&d===0){r.push(cur);cur=''}else cur+=c}if(cur.trim())r.push(cur);return r}
  var guard=0;
  while(guard++<60){
    // найти самую правую открывающую { , внутри которой первый элемент или элемент после запятой начинается с **
    var st=[],found=null,i=0,n=code.length;
    while(i<n){
      var c=code[i];
      if(c==='#'){while(i<n&&code[i]!=='\n')i++;continue}
      if(c==='"'||c==="'"){var q3=code.substr(i,3)===c+c+c,q=q3?c+c+c:c;i+=q.length;while(i<n){if(code[i]==='\\'){i+=2;continue}if(code.substr(i,q.length)===q){i+=q.length;break}if(!q3&&code[i]==='\n')break;i++}continue}
      if('([{'.indexOf(c)>=0){st.push({c:c,at:i,u:false});i++;continue}
      if(')]}'.indexOf(c)>=0){var o=st.pop();if(c==='}'&&o&&o.c==='{'&&o.u)found={a:o.at,b:i};i++;if(found)break;continue}
      if(c==='*'&&code[i+1]==='*'&&st.length&&st[st.length-1].c==='{'){var k=i-1;while(k>=0&&/\s/.test(code[k]))k--;if(code[k]==='{'||code[k]===',')st[st.length-1].u=true;i+=2;continue}
      i++}
    if(!found)break;
    var inner=code.slice(found.a+1,found.b),items=split(inner),parts=[],cur=[];
    items.forEach(function(it){var t=it.trim();if(t.slice(0,2)==='**'){if(cur.length){parts.push('{'+cur.join(', ')+'}');cur=[]}parts.push('('+t.slice(2).trim()+')')}else if(t)cur.push(t)});
    if(cur.length)parts.push('{'+cur.join(', ')+'}');
    code=code.slice(0,found.a)+'__itp_dm(('+parts.join(', ')+',))'+code.slice(found.b+1)}
  return{code:code,map:null}}
function itpDm(){
  Sk.builtins.__itp_dm=new Sk.builtin.func(function(t){
    var d=new Sk.builtin.dict([]),up=Sk.abstr.gattr(d,new Sk.builtin.str('update'));
    t.v.forEach(function(m){
      if(!(m instanceof Sk.builtin.dict)){
        if(!m.tp$getattr||!m.tp$getattr(new Sk.builtin.str('keys')))throw new Sk.builtin.TypeError("'"+Sk.abstr.typeName(m)+"' object is not a mapping")}
      Sk.misceval.callsimArray(up,[m])});
    return d})}
/* --- eval / exec --- */
function itpEx(){
  function glob(){return Sk.sysmodules.mp$subscript(new Sk.builtin.str('__main__')).$d}
  function toObj(dict,into){if(!dict||dict===Sk.builtin.none.none$)return into;if(!(dict instanceof Sk.builtin.dict))throw new Sk.builtin.TypeError('globals must be a dict');
    dict.$items().forEach(function(kv){if(kv[0] instanceof Sk.builtin.str)into[kv[0].$jsstr()]=kv[1]});return into}
  function back(obj,dict){if(!dict||dict===Sk.builtin.none.none$)return;Object.keys(obj).forEach(function(k){if(k.indexOf('__')===0)return;var v=obj[k];if(v&&v.ob$type)dict.mp$ass_subscript(new Sk.builtin.str(k),v)})}
  function run(src,mode,g,l,nm){
    if(!(src instanceof Sk.builtin.str))throw new Sk.builtin.TypeError(nm+'() arg 1 must be a string')
    var code=src.$jsstr();
    if(mode==='eval')code='__itp_ev__ = (\n'+code.replace(/^\s+|\s+$/g,'')+'\n)';else code=code.replace(/^[ \t]+(?=\S)/,function(m){return''});
    code=wal(code).code;
    var ns,pyG=g,pyL=l,own=false;
    if(!g||g===Sk.builtin.none.none$){ns=glob()}else{ns={};toObj(g,ns);if(l&&l!==Sk.builtin.none.none$&&l!==g)toObj(l,ns);own=true}
    var before={};Object.keys(ns).forEach(function(k){before[k]=ns[k]});
    var comp=Sk.compile(code,'<string>','exec',true),fn=Sk.global.eval(comp.code+'\n'+comp.funcname+';');
    Sk.misceval.retryOptionalSuspensionOrThrow(fn(ns));
    var res=Sk.builtin.none.none$;
    if(mode==='eval'){res=ns.__itp_ev__;delete ns.__itp_ev__}
    if(own){var target=(l&&l!==Sk.builtin.none.none$)?l:g;back(ns,target)}
    return res}
  Sk.builtins['eval_$rw$']=Sk.builtins.eval_=Sk.builtins.eval=new Sk.builtin.func(function(s,g,l){return run(s,'eval',g,l,'eval')});
  Sk.builtins.exec=new Sk.builtin.func(function(s,g,l){run(s,'exec',g,l,'exec');return Sk.builtin.none.none$});
}
/* --- порядок элементов множества как в CPython (для целых чисел) --- */
function itpSets(){
  var P=Sk.builtin.set.prototype;if(P.$itpo)return;P.$itpo=1;
  var M=(1n<<61n)-1n;
  function hashOf(x){var v;if(x===Sk.builtin.bool.true$)v=1n;else if(x===Sk.builtin.bool.false$)v=0n;else v=BigInt(x.v.toString());
    var neg=v<0n,a=neg?-v:v;a%=M;var h=neg?-a:a;if(h===-1n)h=-2n;return h}
  function ins(tbl,mask,h,item){var perturb=BigInt.asUintN(64,h),i=Number(perturb&BigInt(mask));
    for(;;){var pr=(i+9<=mask)?9:0;for(var k=i;k<=i+pr;k++)if(tbl[k]===null){tbl[k]=[h,item];return}
      perturb>>=5n;i=Number((BigInt(i)*5n+1n+perturb)&BigInt(mask))}}
  function order(arr){
    if(arr.length<2)return arr;
    for(var q=0;q<arr.length;q++){var t=arr[q];if(!(t instanceof Sk.builtin.int_)&&t!==Sk.builtin.bool.true$&&t!==Sk.builtin.bool.false$)return arr}
    var size=8,tbl=new Array(size).fill(null),used=0;
    arr.forEach(function(x){
      ins(tbl,size-1,hashOf(x),x);used++;
      if(used*5>=(size-1)*3){var minused=used>50000?used*2:used*4,ns=8;while(ns<=minused)ns<<=1;
        var nt=new Array(ns).fill(null);tbl.forEach(function(e){if(e)ins(nt,ns-1,e[0],e[1])});tbl=nt;size=ns}});
    return tbl.filter(function(e){return e}).map(function(e){return e[1]})}
  var as0=P.sk$asarray;
  P.sk$asarray=function(){return order(as0.call(this))};
  P.tp$iter=function(){var a=this.sk$asarray();return Sk.abstr.iter(new Sk.builtin.list(a))};
  if(P.pop&&P.pop.$meth){P.pop.$meth=function(){var a=this.sk$asarray();if(!a.length)throw new Sk.builtin.KeyError('pop from an empty set');this.set$discard(a[0]);return a[0]}}
}
var skPatch4=skPatch;skPatch=function(){skPatch4();try{itpDm()}catch(e){}try{itpEx()}catch(e){}try{itpSets()}catch(e){}
  if(!Sk.configure.$itp){var c0=Sk.configure;Sk.configure=function(){var r=c0.apply(this,arguments);try{itpDm();itpEx()}catch(e){}return r};Sk.configure.$itp=1}};
var wal1=wal;
wal=function(code){
  code=code.replace(/\bint\.from_bytes\s*\(/g,'__itp_ifb(');
  var A=nlT(code),B=dmT(A.code),W=wal1(B.code);
  if(A.map&&W.map)W.map=W.map.map(function(x){return A.map[x-1]||x});else if(A.map)W.map=A.map;
  return W};

function itpInt(){
  var M=Sk.builtin.int_.prototype;if(M.$itpb)return;M.$itpb=1;
  var proto=M.bit_length||M.conjugate;if(!proto)return;
  function add(name,fl,fn){var d=Object.assign(Object.create(Object.getPrototypeOf(proto)),proto);d.$meth=fn;d.$flags=fl;d.d$name=name;d.$name=name;if(d.d$def){d.d$def=Object.assign({},proto.d$def);d.d$def.$meth=fn;d.d$def.$flags=fl;d.d$def.$name=name}M[name]=d}
  add('to_bytes',{NamedArgs:['length','byteorder','signed'],Defaults:[new Sk.builtin.int_(1),new Sk.builtin.str('big'),Sk.builtin.bool.false$]},function(len,order,signed){
    var v=BigInt(this.v.toString()),L=Number(len.v.toString()),sg=Sk.misceval.isTrue(signed),o=order.$jsstr();
    if(o!=='big'&&o!=='little')throw new Sk.builtin.ValueError("byteorder must be either 'little' or 'big'");
    if(v<0n&&!sg)throw new Sk.builtin.OverflowError("can't convert negative int to unsigned");
    var mod=1n<<BigInt(8*L);if(sg){if(v>=(mod>>1n)||v<-(mod>>1n))throw new Sk.builtin.OverflowError('int too big to convert');if(v<0n)v+=mod}else if(v>=mod)throw new Sk.builtin.OverflowError('int too big to convert');
    var a=[];for(var i=0;i<L;i++){a.push(Number(v&255n));v>>=8n}
    if(o==='big')a.reverse();
    return new Sk.builtin.bytes(new Uint8Array(a))})}
var skPatch5=skPatch;skPatch=function(){skPatch5();try{itpInt()}catch(e){}};
