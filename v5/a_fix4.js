/* v5.1.1: длинные программы не вешают страницу, есть кнопка «Остановить» */
liveRun=function(code){
  var o=$('o'),ir=$('ir'),ii=$('ii'),rs=$('rst'),rb=$('run');o.style.display='block';o.textContent='';ir.classList.remove('on');
  function st(t,c){if(rs){rs.hidden=!t;rs.textContent=t||'';rs.className='mu rst'+(c?' '+c:'')}}
  var le=lint(code);if(le){o.textContent='SyntaxError: '+le;st('✗ Программа не запущена: исправь ошибку в коде','bad');snd('err');return}
  st('⏳ Программа выполняется…');
  var pend=null,oc=rb?rb.onclick:null,lab=rb?rb.innerHTML:'',myT=TK+1,done=false;
  function restore(){if(rb){rb.innerHTML=lab;rb.classList.remove('stp');rb.onclick=oc}}
  if(rb){rb.innerHTML='⏹ Остановить';rb.classList.add('stp');rb.onclick=function(){if(done)return;STOPT=myT;if(pend){var p=pend;pend=null;ir.classList.remove('on');p('')}}}
  var V=OutView(o),used=0;o.classList.remove('vo');o.onscroll=null;
  exec(code,{sink:function(s){used=1;V.push(s)},live:function(t){if(!used&&typeof t==='string'&&t)o.textContent=t;if(!pend&&V.virtual())st('⏳ Программа выполняется… строк вывода: '+V.lines())},alive:function(){return o.isConnected},ask:function(){return new Promise(function(r){
    pend=r;
    ir.classList.add('on');ir.classList.remove('typing');ii.value='';st('⌨️ Программа ждёт ввод: напиши ответ в поле ниже и нажми «Ввод»','wait');snd('tick');ii.oninput=function(){ir.classList.add('typing');var r2=$('rst');if(r2)r2.classList.remove('wait')};ii.focus();
    try{ir.scrollIntoView({block:'nearest'})}catch(e){}
    ir.onsubmit=function(e){e.preventDefault();if(!ir.classList.contains('on'))return;ir.classList.remove('on');pend=null;st('⏳ Программа выполняется…');r(ii.value)};
  })}}).then(function(r){
    done=true;V.freeze();restore();ir.classList.remove('on');
    if(r.err&&!r.stopped)snd('err');
    var tail=r.stopped?'⏹ Программа остановлена вручную':(r.err?fixErr(r.err,code):'');
    if(!used&&r.raw)V.push(r.raw);
    var tx=V.text();
    st(r.stopped?'⏹ Программа остановлена':(r.err?'✗ Программа завершилась с ошибкой':'✓ Программа завершена'),r.stopped||r.err?'bad':'ok');
    if(V.virtual()){
      if(tail)V.push((/\n$/.test(tx)?'':'\n')+tail);
      V.flush();
      if(V.dropped())st('Начало вывода (первые '+V.dropped()+' строк) удалено: не хватает памяти. '+(r.err?'Программа завершилась с ошибкой':'Программа завершена'),'bad')}
    else o.textContent=(tx+(tail?((!tx||/\n$/.test(tx))?'':'\n')+tail:'')).trim()||'(программа ничего не вывела)';
    try{o.scrollIntoView({block:'nearest'})}catch(e){}
  });
};
