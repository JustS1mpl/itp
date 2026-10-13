/* v6.4.1: вывод программы без обрезания. Весь вывод хранится кусками, на экране рисуется только видимое окно строк
   (виртуальная прокрутка), поэтому for i in range(10000000): print(i) не вешает страницу. */
function OutView(o){
  var LH=21,PAD=12,MAXH=8000000,PART=32768,LIM=160e6,TXT=20000,THR=300;
  var parts=[],cum=[],tb='',chars=0,dropped=0,virt=false,follow=true,sp=null,win=null,tm=0,busy=false,cI=-1,cL=null;
  function nl(s){var n=0,i=-1;while((i=s.indexOf('\n',i+1))>=0)n++;return n}
  function base(){return cum.length?cum[cum.length-1]:0}
  function total(){return base()+(tb?1+nl(tb):0)}
  function split(i){if(cI!==i){cL=parts[i].slice(0,-1).split('\n');cI=i}return cL}
  function find(a){var lo=0,hi=cum.length;while(lo<hi){var m=(lo+hi)>>1;if(cum[m]>a)hi=m;else lo=m+1}return lo}
  function get(a,b){
    var out=[],need=b-a,ln=a,i=find(a);
    while(i<parts.length&&out.length<need){
      var bs=i?cum[i-1]:0,L=split(i);
      for(var k=Math.max(0,ln-bs);k<L.length&&out.length<need;k++){out.push(L[k]);ln++}
      i++}
    if(out.length<need&&tb){var T=tb.split('\n'),b2=base();for(var k2=Math.max(0,ln-b2);k2<T.length&&out.length<need;k2++){out.push(T[k2]);ln++}}
    return out}
  function addPart(p){
    parts.push(p);cum.push(base()+nl(p));chars+=p.length;
    while(chars>LIM&&parts.length>1){var f=parts.shift(),n=cum[0];cum.shift();for(var i=0;i<cum.length;i++)cum[i]-=n;chars-=f.length;dropped+=n;cI=-1}}
  function text(){return parts.join('')+tb}
  function toVirt(){
    virt=true;o.textContent='';o.classList.add('vo');
    sp=document.createElement('div');sp.className='vs';win=document.createElement('div');win.className='vw';
    o.appendChild(sp);o.appendChild(win);follow=true;
    o.onscroll=function(){if(busy)return;follow=o.scrollTop+o.clientHeight>=o.scrollHeight-LH*1.5;sched()}}
  function render(){
    tm=0;
    if(!virt){
      if(chars+tb.length>TXT||total()>THR)toVirt();else{o.textContent=text();return}}
    var N=total(),H=N*LH+2*PAD,scaled=H>MAXH;if(scaled)H=MAXH;
    sp.style.height=H+'px';
    var ch=o.clientHeight||300,vis=Math.ceil(ch/LH)+3;
    if(follow){busy=true;o.scrollTop=o.scrollHeight;busy=false}
    var st=o.scrollTop,start,top;
    if(!scaled){start=Math.max(0,Math.floor((st-PAD)/LH));top=PAD+start*LH}
    else{var f=Math.min(1,st/Math.max(1,H-ch));start=Math.max(0,Math.round(f*(N-vis+3)));top=st}
    win.style.top=top+'px';win.textContent=get(start,start+vis).join('\n')}
  var frozen=false;
  function sched(){if(!tm&&!frozen)tm=setTimeout(render,45)}
  return{
    push:function(s){
      if(!s)return;tb+=s;
      if(tb.length>=PART){var k=tb.lastIndexOf('\n');if(k>=0){addPart(tb.slice(0,k+1));tb=tb.slice(k+1)}}
      sched()},
    freeze:function(){frozen=true;if(tm){clearTimeout(tm);tm=0}},
    flush:function(){if(tm){clearTimeout(tm);tm=0}render()},
    text:text,virtual:function(){return virt},lines:total,dropped:function(){return dropped},
    empty:function(){return !chars&&!tb}}}
