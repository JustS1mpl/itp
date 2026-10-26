'use strict';
/* PYV — версия Pyodide (как в pyo/pyodide): сторонние пакеты докачиваются с её CDN, если программа их импортирует */
var PYV='0.29.3',PKGURL='https://cdn.jsdelivr.net/pyodide/v'+PYV+'/full/',IMGS=[],rfetch=self.fetch.bind(self);
var py=null,RUN=null,buf=[],blen=0,lastF=0,dec0=new TextDecoder(),dec1=new TextDecoder(),M=null,GLUE='';
function flush(){if(!buf.length)return;var a=buf;buf=[];blen=0;lastF=Date.now();postMessage({t:'out',a:a})}
function emit(k,s){if(!s)return;buf.push([k,s]);blen+=s.length;if(blen>16384||Date.now()-lastF>40)flush()}
function stdinCb(){
  var r=RUN;if(!r)return null;
  if(r.eof)return null;
  if(r.i<r.lines.length){var l=r.lines[r.i++];if(l==='\x05EOF'){r.eof=1;return null}if(r.echo)emit(0,l+'\n');return l}
  if(r.ask){flush();postMessage({t:'need',n:r.i});for(;;){}}
  r.over=true;return null}
/* недостающие библиотеки: сначала каталог Pyodide (numpy, pandas, matplotlib, scipy, …), потом PyPI через micropip.
   Пока качается, страница знает об этом (t:'pkg') и не обрывает программу по времени. Без интернета — понятное сообщение */
function missing(code){try{var l=py.globals.get('_itp_missing')(code),a=l.toJs();l.destroy();return a}catch(x){return[]}}
async function needPkgs(code){
  var miss=missing(code),q={messageCallback:function(){},errorCallback:function(){}};
  if(miss.length){
    postMessage({t:'pkg',n:miss});
    try{await py.loadPackagesFromImports(code,q)}catch(x){}
    var left=missing(code);
    if(left.length){try{await py.loadPackage('micropip',q);var mp=py.pyimport('micropip');for(var i=0;i<left.length;i++){try{await mp.install(left[i])}catch(x){}}}catch(x){}}
    try{var pi=py.globals.get('_itp_preimport');pi(py.toPy(miss));pi.destroy()}catch(x){}
    var fin=missing(code);
    /* библиотеки окон операционной системы: в браузере окон нет, объясняем по-человечески */
    if(fin.indexOf('tkinter')>=0){fin.splice(fin.indexOf('tkinter'),1);emit(1,'tkinter открывает окна на компьютере, а в браузере их нет, поэтому в ИТП он не работает. Рисовать можно через turtle (рисунок появится под выводом) или matplotlib (график).\n')}
    if(fin.length)emit(1,'Библиотеку '+fin.join(', ')+' не удалось загрузить. Она не встроена в ИТП: чтобы скачать её, нужен интернет (или такой библиотеки нет).\n');
    postMessage({t:'pkg',n:[]})}
  if(/matplotlib/.test(code)){try{py.runPython('_itp_preimport(["matplotlib"]);_itp_mpl()')}catch(x){}}}
self.onmessage=async function(e){var m=e.data;
  if(m.t==='init'){
    try{
      self.importScripts=function(u){if(/pyodide\.asm\.js$/.test(u)){(0,eval)(m.asm);return}throw new Error('importScripts '+u)};
      self.fetch=async function(u){u=String(u);
        if(/pyodide\.asm\.wasm$/.test(u))return new Response(m.wasm,{headers:{'Content-Type':'application/wasm'}});
        if(/python_stdlib\.zip$/.test(u))return new Response(m.zip);
        /* в сеть — только за пакетами: CDN Pyodide и PyPI (micropip); остальное ИТП не нужно */
        if(u.indexOf(PKGURL)===0||/^https:\/\/(pypi\.org|files\.pythonhosted\.org)\//.test(u))return rfetch(u);
        throw new Error('fetch '+u)};
      (0,eval)(m.loader);
      var o={indexURL:'https://itp.invalid/',packageBaseUrl:PKGURL,lockFileContents:m.lock,env:{PYTHONHASHSEED:String(m.hseed),HOME:'/home/pyodide'}};
      if(m.snap)o._loadSnapshot=m.snap;else o._makeSnapshot=true;
      py=await loadPyodide(o);
      py.setStdout({write:function(u){var s=dec0.decode(u,{stream:true});emit(0,s);return u.length},isatty:false});
      py.setStderr({write:function(u){var s=dec1.decode(u,{stream:true});emit(1,s);return u.length},isatty:false});
      py.setStdin({stdin:stdinCb,isatty:false});
      if(!m.snap){
        py.runPython(m.glue,{filename:'<itp>'});
        try{var sn=py.makeMemorySnapshot();postMessage({t:'snap',sn:sn},[sn.buffer])}catch(x){postMessage({t:'snap',sn:null})}
      }
      py.globals.set('_mark',function(n){buf.push([2,n]);});
      py.globals.set('_img',function(b){IMGS.push(String(b))});
      postMessage({t:'ready',v:py.version});
    }catch(err){postMessage({t:'fail',e:String(err&&err.stack||err)})}
  }else if(m.t==='run'){
    IMGS=[];
    if(m.code&&/(^|\n)\s*(import|from)\s/.test(m.code))await needPkgs(m.code);
    RUN={lines:m.lines||[],i:0,ask:!!m.ask,echo:!!m.ask,eof:0,over:false};
    var res=null,fail=null;
    try{
      if(m.files)Object.keys(m.files).forEach(function(n){try{py.FS.writeFile('/home/pyodide/'+n,String(m.files[n]))}catch(x){}});
      var f=py.globals.get('_itp_run');res=f(m.code,!m.ask,String(m.seed));try{f.destroy()}catch(x){}
    }catch(err){fail=String(err&&err.message||err)}
    /* pygame пытается открыть окно (SDL ищет экран страницы), а в фоновом процессе браузера окна нет */
    /* после такой ошибки (и любой «fatal») Python в этом процессе мёртв: страница выбросит процесс и запустит свежий (dead) */
    var dead=!!(fail&&/fatal|screen is not defined/i.test(fail));
    if(fail&&/screen is not defined|canvas/i.test(fail)&&/pygame/.test(m.code||'')){fail=null;res='RuntimeError: окно pygame в ИТП не открывается: программа работает в браузере без отдельного окна. Вычисления и логику pygame проверить можно, а рисовать лучше через turtle.'}
    if(dead){postMessage({t:'done',err:res===undefined?null:res,fail:fail,over:false,used:RUN?RUN.i:0,tu:null,im:null,dead:1});RUN=null;return}
    /* рисунок черепахи и графики забираем ДО очистки: _itp_reset выгружает модули, и черепаха исчезала вместе с turtle */
    var tu=null;try{tu=py.runPython('_tdump()')}catch(x){}
    try{py.runPython('_itp_mpl_flush()')}catch(x){}
    flush();
    try{py.runPython('_itp_reset()')}catch(x){}
    var o=RUN;RUN=null;
    postMessage({t:'done',err:res===undefined?null:res,fail:fail,over:o.over,used:o.i,tu:tu||null,im:IMGS.length?IMGS:null})
  }
};
