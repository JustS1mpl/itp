/* v5.2.0: настоящий CPython (Pyodide) вместо Skulpt. Skulpt остаётся запасным вариантом. */
(function(){
var PY={act:null,spare:null,job:null,data:null,readyP:null,ok:false,bad:false};
var HSEED=String(1+Math.floor(Math.random()*4294967294));
var execOld=exec,skOld=skReady,fixOld=fixErr;
function txt(id){var e=document.getElementById(id);return e?e.textContent:''}
function u8(id){var s=atob(txt(id).replace(/\s+/g,'')),a=new Uint8Array(s.length);for(var i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return a}
function gunzip(a){return new Response(new Blob([a]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer().then(function(b){return new Uint8Array(b)})}
function loadData(){
  if(!PY.data)PY.data=(function(){
    if(!window.Worker||!window.WebAssembly||typeof DecompressionStream==='undefined'||!txt('py-wasm'))return Promise.reject(new Error('no wasm'));
    return Promise.all([gunzip(u8('py-wasm')),gunzip(u8('py-asm'))]).then(function(r){
      return{wasm:r[0],asm:new TextDecoder().decode(r[1]),zip:u8('py-zip'),lock:txt('py-lock'),loader:txt('py-loader'),glue:txt('py-glue'),worker:txt('py-worker')}})})();
  return PY.data}
function spawn(){
  var rec={w:null,dead:false,onmsg:null,state:0,maker:false},maker=false;
  if(!PY.snapP){maker=true;rec.maker=true;PY.snapP=new Promise(function(r){PY.snapRes=r})}
  rec.ready=new Promise(function(res){
    Promise.all([loadData(),maker?Promise.resolve(null):PY.snapP]).then(function(r){
      var D=r[0],snap=r[1];
      var url=URL.createObjectURL(new Blob([D.worker],{type:'text/javascript'})),w=new Worker(url);rec.w=w;
      w.onmessage=function(e){var m=e.data;
        if(m.t==='snap'){if(maker&&PY.snapRes){PY.snapRes(m.sn||null);PY.snapRes=null}}
        else if(m.t==='ready'){rec.state=1;res(true)}
        else if(m.t==='fail'){rec.state=-1;try{console.warn(m.e)}catch(x){}if(maker&&PY.snapRes){PY.snapRes(null);PY.snapRes=null}res(false)}
        else if(rec.onmsg)rec.onmsg(m)};
      w.onerror=function(ev){if(rec.state===0){rec.state=-1;if(maker&&PY.snapRes){PY.snapRes(null);PY.snapRes=null}res(false)}else if(rec.onerr)rec.onerr(ev)};
      w.postMessage({t:'init',wasm:D.wasm,asm:D.asm,zip:D.zip,lock:D.lock,loader:D.loader,glue:D.glue,hseed:HSEED,snap:snap||undefined});
    }).catch(function(){rec.state=-1;if(maker&&PY.snapRes){PY.snapRes(null);PY.snapRes=null}res(false)})});
  return rec}
function kill(rec){if(!rec||rec.dead)return;rec.dead=true;if(rec.maker&&PY.snapRes){PY.snapRes(null);PY.snapRes=null;PY.snapP=null}try{rec.w&&rec.w.terminate()}catch(e){}}
function ensureAct(){if(!PY.act||PY.act.dead)PY.act=spawn();return PY.act}
function pyReady(){
  if(PY.ok)return Promise.resolve(true);if(PY.bad)return Promise.resolve(false);
  if(!PY.readyP)PY.readyP=ensureAct().ready.then(function(ok){if(ok){PY.ok=true;SKOK=true}else PY.bad=true;return ok});
  return PY.readyP}
window.PYINFO=PY;
skReady=function(){return pyReady().then(function(ok){return ok?true:skOld()})};
lint=function(){return null};
fixErr=function(e,code){
  if(e&&(/^Traceback \(most recent call last\):/.test(e)||/^\s+File "[^"\n]+", line \d+/.test(e)))return String(e).replace(/\s+$/,'');
  return fixOld(e,code)};
exec=function(code,src){
  src=src||{};
  return pyReady().then(function(ok){
    if(ok)return pyExec(code,src);
    return skOld().then(function(){return execOld(code,src)})})};
function pyExec(code,src){
  var my=++TK,ask=!!src.ask,lines0=src.lines||[],files=src.files||(typeof FCUR!=='undefined'?FCUR:null)||null;
  return new Promise(function(resolve){
    if(PY.job)stopJob(PY.job);
    var job={my:my,dead:false,rec:null,tm:null,poll:null};PY.job=job;
    var seed=String(Math.floor(Math.random()*2147483647)),CAP=20000,SCAP=200000;
    var raw='',D=0,skip=0,stdout='',marks=[],so=0,cut=false,lines=lines0.slice(),eofMode=/\bstdin\b/.test(code),usesIn=/\binput\b|\bstdin\b/.test(code),used=0,over=false,spare=null,done=false,lt=0;
    function live(){if(src.live&&!job.dead){var n=Date.now();if(n-lt<30)return;lt=n;try{src.live(raw)}catch(e){}}}
    function addRaw(s){
      if(skip>0){if(s.length<=skip){skip-=s.length;return}s=s.slice(skip);skip=0}
      D+=s.length;if(cut)return;
      if(raw.length+s.length>CAP){raw+=s.slice(0,CAP-raw.length);cut=true}else raw+=s}
    function result(extra){
      var o=stdout;marks.slice().reverse().forEach(function(m){o=o.slice(0,m[0])+o.slice(m[0]+m[1])});
      var r={out:o,raw:raw+(cut?'\n…вывод обрезан':''),err:null,over:over,used:used,total:lines0.length};
      for(var k in extra)r[k]=extra[k];return r}
    function finish(r){
      if(done)return;done=true;job.dead=true;clearTimeout(job.tm);clearInterval(job.poll);
      if(PY.job===job)PY.job=null;
      var jr=job.rec;
      if(jr&&!jr.dead&&!r.stopped&&!r.killed){if(PY.act&&PY.act!==jr)kill(PY.act);PY.act=jr;if(spare){kill(spare);spare=null}}
      else if(spare){if(!PY.act||PY.act.dead)PY.act=spare;else kill(spare);spare=null}
      if(src.live){try{src.live(raw)}catch(e){}}
      resolve(r)}
    function stopJob(j){ // отмена старого задания при запуске нового
      if(j.stop)j.stop()}
    job.stop=function(){if(done)return;kill(job.rec);if(PY.act===job.rec)PY.act=null;ensureAct();finish(result({err:null,stopped:true,killed:1}))};
    function onMsg(m){
      if(job.dead)return;
      if(m.t==='out'){
        m.a.forEach(function(x){var k=x[0],s=x[1];
          if(k===2){marks.push([so,s]);return}
          if(k===0&&stdout.length<SCAP){stdout+=s}
          if(k===0)so+=s.length;
          addRaw(s)});
        live()}
      else if(m.t==='need'){onNeed()}
      else if(m.t==='done'){
        used=m.used;over=!!m.over;
        var e=m.fail?'InternalError: '+m.fail:m.err;
        if(e&&!m.fail)e=String(e);
        finish(result({err:e||null,turtle:m.tu||null}))}}
    function attach(rec){job.rec=rec;rec.onmsg=onMsg;rec.onerr=function(){if(done)return;kill(rec);if(PY.act===rec)PY.act=null;ensureAct();finish(result({err:'MemoryError: программа остановлена (не хватило памяти)',killed:1}))}}
    function onNeed(){
      var cur=job.rec;kill(cur);if(PY.act===cur)PY.act=null;
      var nxt=spare||spawn();spare=spawn();
      Promise.resolve(src.ask('')).then(function(v){
        if(job.dead||done)return;
        if(STOPT===my){job.stop();return}
        var echo;v=String(v==null?'':v);
        if(eofMode&&v===''){lines.push('\x05EOF');echo=''}else{lines.push(v);echo=v+'\n'}
        addRaw(echo);if(src.live){try{src.live(raw)}catch(e){}}
        skip=D;stdout='';so=0;marks=[];
        nxt.ready.then(function(ok){
          if(job.dead||done)return;
          if(!ok){finish(result({err:'InternalError: не удалось перезапустить среду Python',killed:1}));return}
          attach(nxt);run(nxt)})})}
    function run(rec){
      rec.w.postMessage({t:'run',code:code,lines:lines,ask:ask,files:files,seed:seed})}
    if(!ask){job.tm=setTimeout(function(){if(done)return;kill(job.rec);if(PY.act===job.rec)PY.act=null;ensureAct();finish(result({err:'TimeLimitError: Program exceeded run-time limit.',killed:1}))},25000)}
    job.poll=setInterval(function(){
      if(done)return;
      if(STOPT===my){job.stop();return}
      if(src.alive&&!src.alive()){kill(job.rec);if(PY.act===job.rec)PY.act=null;ensureAct();finish(result({err:null,stopped:true,killed:1}))}},100);
    var rec=ensureAct();
    if(ask&&usesIn){spare=spawn()}
    rec.ready.then(function(ok){
      if(job.dead||done)return;
      if(!ok){finish(result({err:'InternalError: среда Python недоступна'}));return}
      attach(rec);run(rec)});
  })}
})();
