'use strict';
var py=null,RUN=null,buf=[],blen=0,lastF=0,dec0=new TextDecoder(),dec1=new TextDecoder(),M=null,GLUE='';
function flush(){if(!buf.length)return;var a=buf;buf=[];blen=0;lastF=Date.now();postMessage({t:'out',a:a})}
function emit(k,s){if(!s)return;buf.push([k,s]);blen+=s.length;if(blen>16384||Date.now()-lastF>40)flush()}
function stdinCb(){
  var r=RUN;if(!r)return null;
  if(r.eof)return null;
  if(r.i<r.lines.length){var l=r.lines[r.i++];if(l==='\x05EOF'){r.eof=1;return null}if(r.echo)emit(0,l+'\n');return l}
  if(r.ask){flush();postMessage({t:'need',n:r.i});for(;;){}}
  r.over=true;return null}
self.onmessage=async function(e){var m=e.data;
  if(m.t==='init'){
    try{
      self.importScripts=function(u){if(/pyodide\.asm\.js$/.test(u)){(0,eval)(m.asm);return}throw new Error('importScripts '+u)};
      self.fetch=async function(u){u=String(u);
        if(/pyodide\.asm\.wasm$/.test(u))return new Response(m.wasm,{headers:{'Content-Type':'application/wasm'}});
        if(/python_stdlib\.zip$/.test(u))return new Response(m.zip);
        throw new Error('fetch '+u)};
      (0,eval)(m.loader);
      var o={indexURL:'https://itp.invalid/',lockFileContents:m.lock,env:{PYTHONHASHSEED:String(m.hseed),HOME:'/home/pyodide'}};
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
      postMessage({t:'ready',v:py.version});
    }catch(err){postMessage({t:'fail',e:String(err&&err.stack||err)})}
  }else if(m.t==='run'){
    RUN={lines:m.lines||[],i:0,ask:!!m.ask,echo:!!m.ask,eof:0,over:false};
    var res=null,fail=null;
    try{
      if(m.files)Object.keys(m.files).forEach(function(n){try{py.FS.writeFile('/home/pyodide/'+n,String(m.files[n]))}catch(x){}});
      var f=py.globals.get('_itp_run');res=f(m.code,!m.ask,String(m.seed));try{f.destroy()}catch(x){}
    }catch(err){fail=String(err&&err.message||err)}
    flush();
    var tu=null;try{tu=py.runPython('_tdump()')}catch(x){}
    try{py.runPython('_itp_reset()')}catch(x){}
    var o=RUN;RUN=null;
    postMessage({t:'done',err:res===undefined?null:res,fail:fail,over:o.over,used:o.i,tu:tu||null})
  }
};
