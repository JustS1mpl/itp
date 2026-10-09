/* v5.1.1: длинные программы не вешают страницу, есть кнопка «Остановить» */
liveRun=function(code){
  var o=$('o'),ir=$('ir'),ii=$('ii'),rs=$('rst'),rb=$('run');o.style.display='block';o.textContent='';ir.classList.remove('on');
  function st(t,c){if(rs){rs.hidden=!t;rs.textContent=t||'';rs.className='mu rst'+(c?' '+c:'')}}
  var le=lint(code);if(le){o.textContent='SyntaxError: '+le;st('✗ Программа не запущена: исправь ошибку в коде','bad');return}
  st('⏳ Программа выполняется…');
  var pend=null,oc=rb?rb.onclick:null,lab=rb?rb.innerHTML:'',myT=TK+1,done=false;
  function restore(){if(rb){rb.innerHTML=lab;rb.classList.remove('stp');rb.onclick=oc}}
  if(rb){rb.innerHTML='⏹ Остановить';rb.classList.add('stp');rb.onclick=function(){if(done)return;STOPT=myT;if(pend){var p=pend;pend=null;ir.classList.remove('on');p('')}}}
  exec(code,{live:function(t){o.textContent=t},alive:function(){return o.isConnected},ask:function(){return new Promise(function(r){
    pend=r;
    ir.classList.add('on');ir.classList.remove('typing');ii.value='';st('⌨️ Программа ждёт ввод: напиши ответ в поле ниже и нажми «Ввод»','wait');snd('tick');ii.oninput=function(){ir.classList.add('typing');var r2=$('rst');if(r2)r2.classList.remove('wait')};ii.focus();
    try{ir.scrollIntoView({block:'nearest'})}catch(e){}
    ir.onsubmit=function(e){e.preventDefault();if(!ir.classList.contains('on'))return;ir.classList.remove('on');pend=null;st('⏳ Программа выполняется…');r(ii.value)};
  })}}).then(function(r){
    done=true;restore();ir.classList.remove('on');
    var tx=r.raw;
    if(r.stopped){o.textContent=(tx+'\n⏹ Программа остановлена вручную').trim();st('⏹ Программа остановлена','bad')}
    else{o.textContent=(tx+(r.err?((!tx||/\n$/.test(tx))?'':'\n')+fixErr(r.err,code):'')).trim()||'(программа ничего не вывела)';st(r.err?'✗ Программа завершилась с ошибкой':'✓ Программа завершена',r.err?'bad':'ok')}
    try{o.scrollIntoView({block:'nearest'})}catch(e){}
  });
};
