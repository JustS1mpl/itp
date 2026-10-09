/* ===== v5.1.1: тексты ошибок как в CPython, форматирование, sys.exit, деление на ноль ===== */
var ITP_TR=[];
(function(){
  var STR='upper|lower|strip|lstrip|rstrip|title|capitalize|swapcase|isdigit|isalpha|isalnum|isspace|isupper|islower|isdecimal|isnumeric|casefold|splitlines|isidentifier|isprintable|istitle|isascii';
  var LST='append|extend|insert|reverse|sort|clear|copy';
  var DCT='keys|values|items|popitem|setdefault|update|fromkeys';
  function own(n){return new RegExp('^('+n+')\\(\\) (takes (?:no arguments|exactly one argument|exactly (?:\\d+) arguments?|at most (?:\\d+) arguments?|at least (?:\\d+) arguments?) \\(\\d+ given\\))$')}
  ITP_TR.push([own(STR),'str.$1() $2'],[own(LST),'list.$1() $2'],[own(DCT),'dict.$1() $2']);
  ITP_TR.push(
    [/^replace\(\) takes at least 2 arguments \((\d+) given\)$/,'replace() takes at least 2 positional arguments ($1 given)'],
    [/^input\(\) takes at most 1 arguments \((\d+) given\)$/,'input expected at most 1 argument, got $1'],
    [/^(\w+)\(\) takes at least (\d+) arguments? \((\d+) given\)$/,function(m,n,a,g){return n+' expected at least '+a+' argument'+(a==1?'':'s')+', got '+g}],
    [/^(\w+)\(\) takes at most (\d+) arguments? \((\d+) given\)$/,function(m,n,a,g){return n+' expected at most '+a+' argument'+(a==1?'':'s')+', got '+g}],
    [/^(\S+?)\(\) missing 1 required argument: (\w+)$/,"$1() missing 1 required positional argument: '$2'"],
    [/^(\S+?)\(\) missing (\d+) required arguments: (.+)$/,function(m,f,n,l){var a=l.split(', ');var q=a.map(function(x){return"'"+x+"'"});var s=q.length>2?q.slice(0,-1).join(', ')+', and '+q[q.length-1]:q.join(' and ');return f+'() missing '+n+' required positional arguments: '+s}],
    [/ were  given$/,' were given'],
    [/^(\w+)\(\) got an unexpected keyword argument '(\w+)'$/,function(m,f,k){var s=null;if(f==='print'){['sep','end','file','flush'].forEach(function(c){if(!s&&c.indexOf(k.slice(0,2))===0&&Math.abs(c.length-k.length)<=2)s=c})}return f+"() got an unexpected keyword argument '"+k+"'"+(s?". Did you mean '"+s+"'?":'')}],
    [/real number, not '(\w+)'/,"real number, not '$1'"],
    [/a bytes-like object or a number, not/,'a bytes-like object or a real number, not'],
    [/^can only concatenate tuple \(not '(\w+)'\) to tuple$/,'can only concatenate tuple (not "$1") to tuple'],
    [/^sequence item (\d+): expected str, (\w+) found$/,'sequence item $1: expected str instance, $2 found'],
    [/^%([a-z]) format: a number is required, not (\w+)$/,'%$1 format: a real number is required, not $2'],
    [/^range\(\) step argument must not be zero$/,'range() arg 3 must not be zero'],
    [/as an index$/,'as an integer'],
    [/^int\(\) base must be >= 2 and <= 36$/,'int() base must be >= 2 and <= 36, or 0'],
    [/^isinstance\(\) arg 2 must be a class, type, or tuple of classes and types$/,'isinstance() arg 2 must be a type, a tuple of types, or a union'],
    [/^factorial\(\) not defined for negative numbers$/,'factorial() not defined for negative values'],
    [/^local variable '(\w+)' referenced before assignment$/,"cannot access local variable '$1' where it is not associated with a value"],
    [/^cannot convert float inf to integer$/,'cannot convert float infinity to integer'],
    [/^cannot convert float nan to integer$/,'cannot convert float NaN to integer'],
    [/^Numerical result out of range$/,"(34, 'Numerical result out of range')"],
    [/^a str instance is required not '(\w+)'$/,'must be str or None, not $1']
  );
})();
function itpTr(m){for(var i=0;i<ITP_TR.length;i++){var r=ITP_TR[i];if(r[0].test(m)){m=m.replace(r[0],r[1]);}}return m}
function itpTrFull(e){ // «Тип: сообщение on line N»
  var mm=/^((?:External)?Error: )?(\w+Error|\w+): ([\s\S]*?)((?: on line \d+| в строке \d+)?)$/.exec(e);
  if(!mm)return e;
  var t=mm[2],msg=mm[3];
  if(mm[1]==='ExternalError: ')mm[1]='';
  return t+': '+itpTr(msg)+mm[4]}
function itpErrs(){
  var B=Sk.builtin.BaseException.prototype;
  if(!B.$itpt){B.$itpt=1;var old=B.tp$str;B.tp$str=function(){var r=old.call(this);try{if(r&&r.v!==undefined&&this.args&&this.args.v&&this.args.v.length===1&&this.args.v[0] instanceof Sk.builtin.str)return new Sk.builtin.str(itpTr(r.v))}catch(e){}return r}}
  // деление на ноль
  [Sk.builtin.int_,Sk.builtin.float_].forEach(function(C){
    var P=C.prototype;if(P.$itpz)return;P.$itpz=1;
    function wrap(name,rev,kind){var o=P[name];if(!o)return;P[name]=function(x){
      try{return o.apply(this,arguments)}catch(e){
        if(e instanceof Sk.builtin.ZeroDivisionError){var fl=(this instanceof Sk.builtin.float_)||(x instanceof Sk.builtin.float_);
          var msg={d:fl?'float division by zero':'division by zero',f:fl?'float floor division by zero':'integer division or modulo by zero',r:fl?'float modulo by zero':'integer modulo by zero',m:fl?'float divmod()':'integer division or modulo by zero'}[kind];
          throw new Sk.builtin.ZeroDivisionError(msg)}
        throw e}}}
    wrap('nb$divide',0,'d');wrap('nb$reflected_divide',1,'d');wrap('nb$floor_divide',0,'f');wrap('nb$reflected_floor_divide',1,'f');wrap('nb$remainder',0,'r');wrap('nb$reflected_remainder',1,'r');wrap('nb$divmod',0,'m');wrap('nb$reflected_divmod',1,'m')});
  (function(){var P=Sk.builtin.int_.prototype,o=P.nb$power;if(o&&!P.$itpp){P.$itpp=1;P.nb$power=function(e,m){try{if(e instanceof Sk.builtin.int_&&m===undefined&&this.v!==undefined&&Number(this.v.toString())===0&&Number(e.v.toString())<0)throw new Sk.builtin.ZeroDivisionError('0.0 cannot be raised to a negative power')}catch(x){if(x instanceof Sk.builtin.ZeroDivisionError)throw x}return o.apply(this,arguments)}}})();
  // list + не-список, tuple + не-кортеж
  [['list',Sk.builtin.list],['tuple',Sk.builtin.tuple]].forEach(function(p){var P=p[1].prototype,o=P.sq$concat;if(!o||P.$itpc)return;P.$itpc=1;
    P.sq$concat=function(x){if(!(x instanceof p[1]))throw new Sk.builtin.TypeError('can only concatenate '+p[0]+' (not "'+Sk.abstr.typeName(x)+'") to '+p[0]);return o.apply(this,arguments)}});
  // «in» по не-итерируемому
  if(!Sk.abstr.$itpin){Sk.abstr.$itpin=1;var sc=Sk.abstr.sequenceContains;Sk.abstr.sequenceContains=function(a,b,c){try{return sc.apply(this,arguments)}catch(e){if(e instanceof Sk.builtin.TypeError&&/object is not iterable/.test(String(e.args&&e.args.v&&e.args.v[0]&&e.args.v[0].v)))throw new Sk.builtin.TypeError("argument of type '"+Sk.abstr.typeName(a)+"' is not iterable");throw e}}}
  // форматирование: str % args
  (function(){var P=Sk.builtin.str.prototype,o=P.nb$remainder;if(!o||P.$itpf)return;P.$itpf=1;
    P.nb$remainder=function(a){
      try{var f=this.$jsstr(),isT=a instanceof Sk.builtin.tuple,isD=a instanceof Sk.builtin.dict;
        if(!isD){var need=0,rx=/%(\([^)]*\))?([#0\- +]*)(\*|\d+)?(\.(\*|\d+))?[hlL]?([diouxXeEfFgGcrsab%])/g,m;
          while((m=rx.exec(f))){if(m[6]==='%')continue;need++;if(m[3]==='*')need++;if(m[5]==='*')need++}
          var n=isT?a.v.length:1;
          if(n<need)throw new Sk.builtin.TypeError('not enough arguments for format string');
          if(n>need&&!(need===0&&false))throw new Sk.builtin.TypeError('not all arguments converted during string formatting')}
      }catch(e){if(e instanceof Sk.builtin.TypeError)throw e}
      return o.apply(this,arguments)}})();
  // str.format
  (function(){var F=Sk.builtin.str.prototype.format;if(!F||F.$itpf)return;F.$itpf=1;var o=F.$meth;
    F.$meth=function(args,kw){
      try{var s=this.v,nA=args.length,kws={};kw=kw||[];for(var i=0;i<kw.length;i+=2)kws[kw[i]]=1;
        var auto=0,i2=0;
        while(i2<s.length){var c=s[i2];
          if(c==='{'){if(s[i2+1]==='{'){i2+=2;continue}var d=1,j=i2+1;while(j<s.length&&d>0){if(s[j]==='{')d++;else if(s[j]==='}')d--;j++}
            var fld=s.slice(i2+1,j-1),nm=/^[^!:]*/.exec(fld)[0],base=/^[^.\[]*/.exec(nm)[0];
            if(base===''){var ix=auto++;if(ix>=nA)throw new Sk.builtin.IndexError('Replacement index '+ix+' out of range for positional args tuple')}
            else if(/^\d+$/.test(base)){if(+base>=nA)throw new Sk.builtin.IndexError('Replacement index '+base+' out of range for positional args tuple')}
            else if(!kws[base])throw new Sk.builtin.KeyError(new Sk.builtin.str(base));
            i2=j;continue}
          i2++}
      }catch(e){if(e instanceof Sk.builtin.IndexError||e instanceof Sk.builtin.KeyError)throw e}
      return o.apply(this,arguments)}})();
  // ModuleNotFoundError
  if(!Sk.builtin.ModuleNotFoundError){Sk.builtin.ModuleNotFoundError=Sk.abstr.buildNativeClass('ModuleNotFoundError',{constructor:function(){Sk.builtin.ImportError.apply(this,arguments)},base:Sk.builtin.ImportError})}
  if(!Sk.builtin.__import__.$itpm){var imp=Sk.builtin.__import__,nw=function(){try{return imp.apply(this,arguments)}catch(e){if(e instanceof Sk.builtin.ImportError&&!(e instanceof Sk.builtin.ModuleNotFoundError)&&/^No module named/.test(String(e.args&&e.args.v&&e.args.v[0]&&e.args.v[0].v)))throw new Sk.builtin.ModuleNotFoundError(e.args.v[0].v);throw e}};nw.$itpm=1;for(var k in imp)nw[k]=imp[k];Sk.builtin.__import__=nw}
}
function itpBuiltins(){
  var B=Sk.builtins,tn=function(a){return Sk.abstr.typeName(a)};
  var F=function(fn){return new Sk.builtin.func(fn)};
  var abs0=B.abs;B.abs=F(function(a){if(!a||!a.nb$abs)throw new Sk.builtin.TypeError("bad operand type for abs(): '"+tn(a)+"'");return a.nb$abs()});
  var chr0=B.chr;B.chr=F(function(a){if(!Sk.builtin.checkInt(a))throw new Sk.builtin.TypeError("'"+tn(a)+"' object cannot be interpreted as an integer");return Sk.misceval.callsimArray(chr0,[a])});
  var rd0=B.round;B.round=F(function(a,n){if(a===undefined)throw new Sk.builtin.TypeError("round() missing required argument 'number' (pos 1)");
    if(!Sk.builtin.checkNumber(a)&&!(a.tp$getattr&&a.tp$getattr(new Sk.builtin.str('__round__'))))throw new Sk.builtin.TypeError("type "+tn(a)+" doesn't define __round__ method");
    if(n!==undefined&&n!==Sk.builtin.none.none$&&!Sk.builtin.checkInt(n))throw new Sk.builtin.TypeError("'"+tn(n)+"' object cannot be interpreted as an integer");
    return Sk.misceval.callsimArray(rd0,n===undefined?[a]:[a,n])});
  var ex=F(function(c){var e=new Sk.builtin.SystemExit(c===undefined?Sk.builtin.none.none$:c);throw e});
  B.exit=ex;B.quit=ex;
  B.__itp_ex__=ex;
}
function itpAfterImport(){
  var prev=Sk.onAfterImport;
  Sk.onAfterImport=function(nm){
    try{
      var m=Sk.sysmodules.mp$subscript(new Sk.builtin.str(nm)),d=m.$d,S=function(x){return new Sk.builtin.str(x)};
      if(nm==='sys'){
        d.exit=Sk.builtins.__itp_ex__;
        d.version_info=new Sk.builtin.tuple([3,12,0].map(function(x){return new Sk.builtin.int_(x)}).concat([S('final'),new Sk.builtin.int_(0)]));
        d.version=S('3.12.0 (ИТП)');
        d.maxsize=Sk.misceval.callsimArray(Sk.builtin.int_,[S('9223372036854775807')]);
      }
      if(nm==='math'){
        ['acos','asin'].forEach(function(f){var o=d[f];if(!o)return;d[f]=new Sk.builtin.func(function(x){var v=Number(Sk.builtin.asnum$(x));if(v>1||v<-1)throw new Sk.builtin.ValueError('math domain error');return Sk.misceval.callsimArray(o,[x])})});
      }
    }catch(e){}
    if(typeof prev==='function')return prev.apply(this,arguments)}
}
var skPatch6=skPatch;skPatch=function(){skPatch6();try{itpErrs()}catch(e){console.log(e)}try{itpBuiltins()}catch(e){}try{itpAfterImport()}catch(e){}
  if(!Sk.configure.$itp3){var c1=Sk.configure;Sk.configure=function(){var r=c1.apply(this,arguments);try{itpBuiltins();itpAfterImport()}catch(e){}return r};Sk.configure.$itp3=1;if(Sk.configure.$itp)Sk.configure.$itp=1}};
