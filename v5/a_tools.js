/* ===================== служебная панель ===================== */
function xtSha(b){
  var K=[],H=[],i,j,p=2,n=0;
  for(;n<64;p++){for(j=2;j*j<=p;j++)if(p%j===0)break;if(j*j>p){if(n<8)H[n]=(Math.pow(p,.5)%1*4294967296)|0;K[n++]=(Math.pow(p,1/3)%1*4294967296)|0}}
  var l=b.length,tl=(((l+8)>>6)+1)<<6,w=new Uint8Array(tl);w.set(b);w[l]=128;
  var dv=new DataView(w.buffer);dv.setUint32(tl-4,(l*8)>>>0);dv.setUint32(tl-8,Math.floor(l/536870912));
  var W=new Array(64);
  for(var o=0;o<tl;o+=64){
    for(i=0;i<16;i++)W[i]=dv.getUint32(o+i*4);
    for(i=16;i<64;i++){var a=W[i-15],c=W[i-2];W[i]=(W[i-16]+(((a>>>7)|(a<<25))^((a>>>18)|(a<<14))^(a>>>3))+W[i-7]+(((c>>>17)|(c<<15))^((c>>>19)|(c<<13))^(c>>>10)))|0}
    var v=H.slice();
    for(i=0;i<64;i++){var e=v[4],q=v[0],t1=(v[7]+(((e>>>6)|(e<<26))^((e>>>11)|(e<<21))^((e>>>25)|(e<<7)))+((e&v[5])^(~e&v[6]))+K[i]+W[i])|0,t2=((((q>>>2)|(q<<30))^((q>>>13)|(q<<19))^((q>>>22)|(q<<10)))+((q&v[1])^(q&v[2])^(v[1]&v[2])))|0;
      v=[(t1+t2)|0,v[0],v[1],v[2],(v[3]+t1)|0,v[4],v[5],v[6]]}
    for(i=0;i<8;i++)H[i]=(H[i]+v[i])|0}
  return H.map(function(x){return('00000000'+(x>>>0).toString(16)).slice(-8)}).join('')}
var XTN=null,XTV=false,XTC=null;
function XTOK(){
  var n=window.S&&S.nick;
  if(n!==XTN){XTN=n;XTV=false;
    if(n&&window.TextEncoder){var d=n,t=new TextEncoder();for(var i=0;i<1500;i++)d=xtSha(t.encode('itp:'+d));XTV=d==='d679b1510457b6831bcc506b5fbcecea317c52f56baa166ee0a66391f96f1b8c'}}
  return XTV}
(function(){
  var _t=task,_q=quiz,_p=project,_th=theory,_h=home,_a=ansTask,_o=isOpen;
  ansTask=function(i,j,k){XTC={t:'ans',i:i,j:j,k:k};return _a.apply(this,arguments)};
  isOpen=function(i,j){return XTOK()?1:_o(i,j)};
  task=function(i,j,k){XTC={t:'task',i:i,j:j,k:k};return _t.apply(this,arguments)};
  quiz=function(i,j){XTC={t:'quiz',i:i,j:j};return _q.apply(this,arguments)};
  project=function(i,j){XTC={t:'project',i:i,j:j};return _p.apply(this,arguments)};
  theory=function(i,j){XTC={t:'theory',i:i,j:j};return _th.apply(this,arguments)};
  home=function(){XTC=null;return _h.apply(this,arguments)};
})();
function xtEsc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function xtClose(){var o=document.getElementById('xtp');if(o)o.remove()}
function xtDone(i,j){var k=i+'-'+j,it=IT(i,j);if(!it)return;S.d[k]=1;if(it.t==='flash'||it.t==='test'){if(S.es[k]===undefined)S.es[k]=0}save()}
function xtPanel(){
  xtClose();
  var o=document.createElement('div');o.id='xtp';o.className='xtp';
  var h='<div class="xtc"><div class="xth"><b>🛠 Инструменты</b><button class="icon" id="xtx" aria-label="Закрыть">✕</button></div>';
  if(XTC){
    var it=IT(XTC.i,XTC.j),lab=xtEsc(TOPICS[XTC.i].n)+' · '+xtEsc(it.n||'');
    h+='<div class="xts">Сейчас: '+lab+'</div><div class="xtr">';
    if(XTC.t==='task'){var T=it.tasks;
      h+='<button data-a="tp"'+(XTC.k<1?' disabled':'')+'>◀ Задание</button><button data-a="tn"'+(XTC.k>=T.length-1?' disabled':'')+'>Задание ▶</button><button data-a="sol">Вставить решение</button><button data-a="solc">Решение и проверить</button>'}
    if(XTC.t==='project')h+='<button data-a="sol">Вставить решение</button><button data-a="solc">Решение и проверить</button>';
    if(XTC.t==='quiz')h+='<button data-a="ans">Показать верный ответ</button>';
    if(XTC.t==='ans')h+='<button data-a="atp"'+(XTC.k<1?' disabled':'')+'>◀ Задание</button><button data-a="atn"'+(XTC.k>=it.tasks.length-1?' disabled':'')+'>Задание ▶</button><button data-a="aans">Подставить ответ</button>';
    h+='<button data-a="cur">Отметить островок пройденным</button></div>';
  }
  h+='<div class="xts">Опыт и уровень</div><div class="xtr"><button data-a="xp50">+50 ⭐</button><button data-a="xp500">+500 ⭐</button><button data-a="lv">+1 уровень</button></div>';
  h+='<div class="xts">Серия и заморозки</div><div class="xtr"><button data-a="st">Серия +1</button><button data-a="st0">Серия = 0</button><button data-a="fz">Заморозка +1</button><button data-a="fz0">Заморозки = 0</button></div>';
  h+='<div class="xts">Прогресс</div><div class="xtr"><button data-a="all">Все островки пройдены</button><button data-a="none">Сбросить прогресс островков</button><button data-a="gl">Цель дня выполнена</button></div>';
  h+='<div class="xts">Достижения (нажми, чтобы выдать или забрать)</div><div class="xtr"><button data-a="aa">Выдать все</button><button data-a="an">Забрать все</button></div><div class="xta">';
  ACH.forEach(function(a){h+='<button class="xtk'+(S.ach[a.id]?' on':'')+'" data-id="'+a.id+'" title="'+xtEsc(a.d)+'">'+a.e+' '+xtEsc(a.n)+'</button>'});
  h+='</div></div>';
  o.innerHTML=h;document.body.appendChild(o);
  o.onclick=function(e){if(e.target===o)xtClose()};
  document.getElementById('xtx').onclick=xtClose;
  o.querySelectorAll('.xtk').forEach(function(b){b.onclick=function(){var id=b.dataset.id;if(S.ach[id]){delete S.ach[id];save()}else ach(id);xtPanel()}});
  o.querySelectorAll('[data-a]').forEach(function(b){b.onclick=function(){xtAct(b.dataset.a)}});
}
function xtAct(a){
  var c=XTC;
  if(a==='atp'||a==='atn'){xtClose();return ansTask(c.i,c.j,c.k+(a==='atn'?1:-1))}
  if(a==='aans'){var ai=document.getElementById('ai');if(!ai||ai.disabled)return toast('Поле ответа не открыто');ai.value=IT(c.i,c.j).tasks[c.k].a;xtClose();return}
  if(a==='tp'||a==='tn'){xtClose();return task(c.i,c.j,c.k+(a==='tn'?1:-1))}
  if(a==='sol'||a==='solc'){
    var it=IT(c.i,c.j),sol=c.t==='task'?it.tasks[c.k].sol:it.sol,ed=document.getElementById('code');
    if(!sol||!ed)return toast('Решения нет или редактор не открыт');
    ed.value=sol;ed.dispatchEvent(new Event('input',{bubbles:true}));
    xtClose();if(a==='solc'){var b=document.getElementById('chk')||document.getElementById('pchk');if(b)b.click()}return}
  if(a==='ans'){
    var qq=document.querySelector('.q,h2'),Ql=IT(c.i,c.j).q,tx=qq?qq.textContent.trim():'',hit=null;
    Ql.forEach(function(x){if(x.q.trim()===tx&&!hit)hit=x});
    if(!hit)return toast('Вопрос не найден на экране');
    document.querySelectorAll('.opt').forEach(function(b){if(b.textContent.trim()===String(hit.o[hit.a]).trim())b.classList.add('sel')});
    return toast('Верно: '+hit.o[hit.a])}
  if(a==='cur'){xtDone(c.i,c.j);xtClose();return home()}
  if(a==='xp50'){addXp(50);save();toast('+50 ⭐');return}
  if(a==='xp500'){addXp(500);save();toast('+500 ⭐');return}
  if(a==='lv'){var l=lvlInfo(S.xp).l,n=0;while(lvlInfo(S.xp).l===l&&n++<400)addXp(10);save();toast('Уровень: '+lvlInfo(S.xp).l);return}
  if(a==='st'){var t=day(new Date());if(S.last!==t){S.last=t;S.streak=(S.streak||0)+1}else S.streak++;if(S.streak>S.max)S.max=S.streak;save();toast('Серия: '+S.streak);return}
  if(a==='st0'){S.streak=0;save();toast('Серия сброшена');return}
  if(a==='fz'){S.fz.n=Math.min(2,S.fz.n+1);save();toast('Заморозок: '+S.fz.n);return}
  if(a==='fz0'){S.fz.n=0;S.fz.p=0;save();toast('Заморозок: 0');return}
  if(a==='all'){TOPICS.forEach(function(t,i){t.items.forEach(function(x,j){xtDone(i,j)})});toast('Все островки пройдены');xtClose();return home()}
  if(a==='none'){S.d={};S.es={};S.at={};S.dr={};S.tk={};S.hu={};save();toast('Прогресс островков сброшен');xtClose();return home()}
  if(a==='gl'){var t2=day(new Date());S.hist[t2]=S.hist[t2]||{les:0};S.hist[t2].les=Math.max(S.hist[t2].les||0,S.goal);goalCheck();save();toast('Цель дня засчитана');return}
  if(a==='aa'){ACH.forEach(function(x){if(x.id!=='all'&&!S.ach[x.id])ach(x.id)});return xtPanel()}
  if(a==='an'){S.ach={};save();return xtPanel()}
}
(function(){
  function sync(){var b=document.getElementById('xtb');if(XTOK()){if(!b){b=document.createElement('button');b.id='xtb';b.className='xtb';b.setAttribute('aria-label','Инструменты');b.textContent='🛠';b.onclick=xtPanel;document.body.appendChild(b)}}else{if(b)b.remove();xtClose()}}
  setInterval(sync,700);
})();
