/* ===================== v5.1.2: генератор заданий ЕГЭ (бесконечная тренировка) =====================
   Реестр EXGEN: номер задания -> {no, name, types:[{id,n,d}], make(typeId, rnd) -> задача}
   Задача: {q, svg, f, h:[подсказки], s:[шаги разбора], a:'ответ', m:'частая ошибка'}
   Чтобы добавить новое задание ЕГЭ, достаточно дописать запись в EXGEN (см. промт для нейросетей). */
var EXGEN={};
function exRnd(seed){var a=seed>>>0;return function(){a=(a+0x6D2B79F5)>>>0;var t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296}}
function exPick(r,a){return a[Math.floor(r()*a.length)]}
function exShuf(r,a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
(function(){
  var LAT='ABCDEFGHI'.split(''),CYR='АБВГДЕЖЗИ'.split('');
  /* ---------- плоский граф с рисунком ---------- */
  function ccw(a,b,c){return(c[1]-a[1])*(b[0]-a[0])-(b[1]-a[1])*(c[0]-a[0])}
  function cross(p1,p2,p3,p4){var d1=ccw(p1,p2,p3),d2=ccw(p1,p2,p4),d3=ccw(p3,p4,p1),d4=ccw(p3,p4,p2);return d1*d2<0&&d3*d4<0}
  function pdist(p,a,b){var dx=b[0]-a[0],dy=b[1]-a[1],L=dx*dx+dy*dy,t=L?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/L)):0;return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)}
  function genGraph(r,n,m){
    for(var att=0;att<400;att++){
      var pts=[],tr=0;
      while(pts.length<n&&tr++<500){var p=[.05+r()*.9,.07+r()*.86];if(pts.every(function(q){return Math.hypot((p[0]-q[0])*1.3,p[1]-q[1])>.21}))pts.push(p)}
      if(pts.length<n)continue;
      var cand=[];for(var i=0;i<n;i++)for(var j=i+1;j<n;j++)cand.push([i,j,Math.hypot((pts[i][0]-pts[j][0])*1.3,pts[i][1]-pts[j][1])*(.75+.6*r())]);
      cand.sort(function(a,b){return a[2]-b[2]});
      var E=[],deg=[];for(i=0;i<n;i++)deg.push(0);
      var par=[];for(i=0;i<n;i++)par.push(i);function f(x){return par[x]===x?x:(par[x]=f(par[x]))}
      function ok(a,b){
        if(deg[a]>=5||deg[b]>=5)return false;
        for(var k=0;k<E.length;k++){var e=E[k];if(e[0]!==a&&e[0]!==b&&e[1]!==a&&e[1]!==b&&cross(pts[a],pts[b],pts[e[0]],pts[e[1]]))return false}
        for(k=0;k<n;k++)if(k!==a&&k!==b&&pdist(pts[k],pts[a],pts[b])<.075)return false;
        var ends=[[a,b],[b,a]];
        for(var q=0;q<2;q++){var v=ends[q][0],u=ends[q][1],d0=Math.atan2(pts[u][1]-pts[v][1],pts[u][0]-pts[v][0]);
          for(k=0;k<E.length;k++){var e2=E[k],w=e2[0]===v?e2[1]:e2[1]===v?e2[0]:-1;if(w<0)continue;
            var d1=Math.atan2(pts[w][1]-pts[v][1],pts[w][0]-pts[v][0]),d=Math.abs(d0-d1)%(2*Math.PI);d=Math.min(d,2*Math.PI-d);
            if(d<.4||d>2.9)return false}}
        return true}
      cand.forEach(function(c){if(f(c[0])!==f(c[1])&&ok(c[0],c[1])){E.push([c[0],c[1]]);deg[c[0]]++;deg[c[1]]++;par[f(c[0])]=f(c[1])}});
      var roots={};for(i=0;i<n;i++)roots[f(i)]=1;if(Object.keys(roots).length>1)continue;
      var rest=exShuf(r,cand.filter(function(c){return!E.some(function(e){return e[0]===c[0]&&e[1]===c[1]})}));
      rest.forEach(function(c){if(E.length<m&&ok(c[0],c[1])){E.push([c[0],c[1]]);deg[c[0]]++;deg[c[1]]++}});
      if(E.length===m)return{pts:pts,E:E}
    }
    return null}
  /* ---------- решатель ---------- */
  function adjOf(n,E){var a=[];for(var i=0;i<n;i++)a.push({});E.forEach(function(e){a[e[0]][e[1]]=1;a[e[1]][e[0]]=1});return a}
  function isos(ag,at){
    var n=ag.length,res=[],dg=ag.map(function(a){return Object.keys(a).length}),dt=at.map(function(a){return Object.keys(a).length});
    function rec(i,m,used){
      if(i===n){res.push(m.slice());return}
      for(var c=0;c<n;c++){if(used[c]||dt[c]!==dg[i])continue;var ok=true;
        for(var j=0;j<i;j++)if(!!ag[i][j]!==!!at[c][m[j]]){ok=false;break}
        if(ok){m.push(c);used[c]=1;rec(i+1,m,used);m.pop();used[c]=0}}}
    rec(0,[],[]);return res}
  function fmt(a){return'('+a.join(', ')+')'}
  function staged(ag,at,ng,nt,focus){
    var n=ag.length,dg=ag.map(function(a){return Object.keys(a).length}),dt=at.map(function(a){return Object.keys(a).length});
    function nb(adj,deg){return adj.map(function(a){return Object.keys(a).map(function(k){return deg[+k]}).sort(function(x,y){return x-y})})}
    var bg=nb(ag,dg),bt=nb(at,dt),map={},steps=[],mx=0;
    function same(x,y){return x.length===y.length&&x.every(function(v,i){return v===y[i]})}
    function cands(i,st,used){var o=[];for(var c=0;c<n;c++){if(used[c]||dt[c]!==dg[i])continue;if(st>=2&&!same(bt[c],bg[i]))continue;
      if(st===3){var bad=false;for(var j in map)if(!!ag[i][j]!==!!at[c][map[j]]){bad=true;break}if(bad)continue}o.push(c)}return o}
    for(var guard=0;guard<40&&Object.keys(map).length<n;guard++){
      if(focus&&focus.every(function(f){return map[f]!==undefined}))break;
      var used={};for(var k in map)used[map[k]]=1;var prog=false;
      for(var st=1;st<=3;st++){
        var nw=[];for(var i=0;i<n;i++){if(map[i]!==undefined)continue;var cs=cands(i,st,used);if(cs.length===1)nw.push([i,cs[0]])}
        var seen={},clean=[];nw.forEach(function(p){if(seen[p[1]])return;seen[p[1]]=1;clean.push(p)});
        if(!clean.length)continue;
        var sm={};for(k in map)sm[k]=map[k];var su={};for(k in used)su[k]=1;
        clean.forEach(function(p){
          var i2=p[0],c=p[1],rg=[],rt=[];
          for(var x=0;x<n;x++){if(dg[x]===dg[i2]&&sm[x]===undefined)rg.push(ng[x]);if(dt[x]===dg[i2]&&!su[x])rt.push(nt[x])}
          if(st===1)steps.push('Степень '+dg[i2]+' встречается один раз: в графе у '+rg.join(', ')+', в таблице у '+rt.join(', ')+'. Значит '+ng[i2]+' = '+nt[c]+'.');
          else if(st===2)steps.push('Степень '+dg[i2]+' у нескольких вершин графа ('+rg.join(', ')+') и таблицы ('+rt.join(', ')+'). Смотрим степени соседей: у '+ng[i2]+' соседи имеют степени '+fmt(bg[i2])+'; такой набор в таблице только у '+nt[c]+'. Значит '+ng[i2]+' = '+nt[c]+'.');
          else{
            var kn=[],kx=[];for(var j in sm){j=+j;var s=ng[j]+'(='+nt[sm[j]]+')';if(ag[i2][j])kn.push(s);else kx.push(s)}
            var parts=[];if(kn.length)parts.push('соединена с '+kn.join(', '));if(kx.length)parts.push('не соединена с '+kx.join(', '));
            steps.push('Вершина '+ng[i2]+' '+parts.join('; ')+'. Среди кандидатов с теми же степенями такие же связи только у '+nt[c]+'. Значит '+ng[i2]+' = '+nt[c]+'.')}
          map[i2]=c;used[c]=1});
        mx=Math.max(mx,st);prog=true;break}
      if(!prog)break}
    return{steps:steps,map:map,stage:mx}}
  function dijkstra(t,s,d){var n=t.length,dist=[],i;for(i=0;i<n;i++)dist.push(1e9);dist[s]=0;var done={};
    for(var it=0;it<n;it++){var u=-1;for(i=0;i<n;i++)if(!done[i]&&(u<0||dist[i]<dist[u]))u=i;if(u<0||dist[u]>=1e9)break;done[u]=1;for(i=0;i<n;i++)if(t[u][i]>0&&dist[u]+t[u][i]<dist[i])dist[i]=dist[u]+t[u][i]}return dist[d]}
  function paths(t,s,d){var n=t.length,out=[];(function rec(v,p,l){if(v===d){out.push([l,p.slice()]);return}for(var u=0;u<n;u++)if(t[v][u]>0&&p.indexOf(u)<0){p.push(u);rec(u,p,l+t[v][u]);p.pop()}})(s,[s],0);out.sort(function(a,b){return a[0]-b[0]});return out}
  /* ---------- рисунок (SVG, белый фон, как в экзамене) ---------- */
  var FF='font-family="DejaVu Sans,Arial,sans-serif"';
  function svgOf(G,names,T,o){
    var n=T.length,cs=n>=9?44:48,W0=o.noGraph?0:560,tx=W0+(o.noGraph?20:30),ty=o.plain?60:30;
    var tw=(n+1)*cs,H=Math.max(o.noGraph?0:430,ty+tw+20),W=tx+tw+(o.plain?40:20);
    var s='<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Схема дорог и таблица" style="width:100%;height:auto;display:block;background:#fff"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
    if(!o.noGraph){
      var P=G.pts.map(function(p){return[24+p[0]*500,30+p[1]*370]});
      G.E.forEach(function(e){s+='<line x1="'+P[e[0]][0].toFixed(1)+'" y1="'+P[e[0]][1].toFixed(1)+'" x2="'+P[e[1]][0].toFixed(1)+'" y2="'+P[e[1]][1].toFixed(1)+'" stroke="#111" stroke-width="3"/>'});
      P.forEach(function(p,i){
        var vx=0,vy=0;G.E.forEach(function(e){var w=e[0]===i?e[1]:e[1]===i?e[0]:-1;if(w<0)return;var dx=P[w][0]-p[0],dy=P[w][1]-p[1],l=Math.hypot(dx,dy);vx+=dx/l;vy+=dy/l});
        var l2=Math.hypot(vx,vy)||1,ox=-vx/l2*26,oy=-vy/l2*26;if(l2<.3){ox=0;oy=-26}
        s+='<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="6" fill="#111"/><text x="'+(p[0]+ox).toFixed(1)+'" y="'+(p[1]+oy+10).toFixed(1)+'" text-anchor="middle" font-size="30" fill="#111" '+FF+'>'+names[i]+'</text>'})}
    var hd=o.hdr;
    if(o.plain){s+='<text x="'+(tx+(n+1)*cs/2+cs/2)+'" y="30" text-anchor="middle" font-size="22" fill="#111" '+FF+'>Номер пункта</text><text transform="translate(18,'+(ty+tw/2+cs/2)+') rotate(-90)" text-anchor="middle" font-size="22" fill="#111" '+FF+'>Номер пункта</text>'}
    var x0=tx+(o.plain?cs/2:0),y0=ty;
    for(var i=0;i<=n;i++)for(var j=0;j<=n;j++){
      if(i===0&&j===0)continue;
      var x=x0+j*cs,y=y0+i*cs,fill='#fff',txt='';
      if(i===0)txt=hd[j-1];else if(j===0)txt=hd[i-1];else if(i===j)fill='#bbb';else if(T[i-1][j-1]>0)txt=o.stars?'*':String(T[i-1][j-1]);
      s+='<rect x="'+x+'" y="'+y+'" width="'+cs+'" height="'+cs+'" fill="'+fill+'" stroke="#111" stroke-width="1.5"/>';
      if(txt)s+='<text x="'+(x+cs/2)+'" y="'+(y+cs/2+(o.stars&&i&&j?11:8))+'" text-anchor="middle" font-size="'+(o.stars&&i&&j?32:(hd[0].length>1&&(i===0||j===0)?20:24))+'" fill="#111" '+FF+'>'+txt+'</text>'}
    return s+'</svg>'}
  /* ---------- сборка задания ---------- */
  var QM={'1.1':'Записать номера в порядке букв из вопроса, а не по возрастанию.','1.2':'Собрать буквы по алфавиту вместо порядка П1…Пn.','1.3':'Прочитать клетку не для той пары пунктов или перепутать соответствие двух похожих пунктов.','1.4':'Найти только одну из двух длин или сложить не те дороги.','1.5':'Не применить условие «длиннее» и взять длину из подходящей по степеням, но неверной расстановки.','1.6':'Остановиться на первом найденном пути и не проверить остальные.'};
  var FM={'1.1':'Два номера слитно по возрастанию, например 35.','1.2':'Строка букв без пробелов в порядке П1, П2, …','1.3':'Целое число километров.','1.4':'Целое число километров.','1.5':'Целое число километров.','1.6':'Целое число километров.'};
  function gen1(type,r){
    var spec={'1.1':{n:[6,7],dm:[1,3]},'1.2':{n:[7,9],dm:[2,3]},'1.3':{n:[6,7],dm:[1,3]},'1.4':{n:[6,7],dm:[1,3]},'1.5':{n:[6,7],dm:[1,2]},'1.6':{n:[6,7],dm:[1,3]}}[type];
    var stars=type==='1.1'||type==='1.2';
    for(var att=0;att<3000;att++){
      var n=spec.n[0]+Math.floor(r()*(spec.n[1]-spec.n[0]+1)),m=n+spec.dm[0]+Math.floor(r()*(spec.dm[1]-spec.dm[0]+1));
      if(m>3*n-6)continue;
      var cyr=!stars&&type!=='1.6'&&r()<.5,alpha=cyr?CYR:LAT,plain=stars?(r()<.7):false;
      if(type==='1.6'){var res=gen16(r,n,m);if(res)return res;continue}
      var G=genGraph(r,n,m);if(!G)continue;
      var w=exShuf(r,(function(){var a=[];for(var i=2;i<=40;i++)a.push(i);return a})()).slice(0,m);
      var perm=exShuf(r,(function(){var a=[];for(var i=1;i<=n;i++)a.push(i);return a})());
      var T=[];for(var i=0;i<n;i++){T.push([]);for(var j=0;j<n;j++)T[i].push(0)}
      G.E.forEach(function(e,k){var a=perm[e[0]]-1,b=perm[e[1]]-1;T[a][b]=w[k];T[b][a]=w[k]});
      var ag=adjOf(n,G.E),at=T.map(function(row){var o={};row.forEach(function(v,j){if(v>0)o[j]=1});return o});
      var I=isos(ag,at);if(!I.length)continue;
      var hdr=[];for(i=1;i<=n;i++)hdr.push(plain?String(i):'П'+i);
      var ng=alpha.slice(0,n),nt=hdr.slice();
      var ans,focus,qtxt,extra=null;
      function A(f,list){return Array.from(new Set((list||I).map(f)))}
      if(type==='1.1'){var q=exShuf(r,[0,1,2,3,4,5,6,7,8].slice(0,n)).slice(0,2).sort();focus=q;
        ans=A(function(m2){return[m2[q[0]]+1,m2[q[1]]+1].sort(function(x,y){return x-y}).join('')});
        qtxt='Определите, какие номера в таблице соответствуют пунктам '+ng[q[0]]+' и '+ng[q[1]]+' на схеме. В ответе запишите эти два номера по возрастанию, без пробелов и других символов.'}
      else if(type==='1.2'){focus=null;
        ans=A(function(m2){var inv={};m2.forEach(function(c,i){inv[c]=i});var s='';for(var j=0;j<n;j++)s+=ng[inv[j]];return s});
        qtxt='Выпишите без пробелов буквы схемы, соответствующие пунктам '+(plain?'1…'+n:'П1…П'+n)+', в порядке возрастания их номеров.'}
      else if(type==='1.3'){var e=exPick(r,G.E),a2=r()<.5?e[0]:e[1],b2=a2===e[0]?e[1]:e[0];focus=[a2,b2];
        ans=A(function(m2){return T[m2[a2]][m2[b2]]});qtxt='Определите длину дороги из пункта '+ng[a2]+' в пункт '+ng[b2]+'. В ответе запишите целое число.';extra={e1:[a2,b2]}}
      else if(type==='1.4'){var es=exShuf(r,G.E).slice(0,2);focus=Array.from(new Set([es[0][0],es[0][1],es[1][0],es[1][1]]));
        ans=A(function(m2){return T[m2[es[0][0]]][m2[es[0][1]]]+T[m2[es[1][0]]][m2[es[1][1]]]});
        qtxt='Определите сумму длин дорог из пункта '+ng[es[0][0]]+' в пункт '+ng[es[0][1]]+' и из пункта '+ng[es[1][0]]+' в пункт '+ng[es[1][1]]+'. В ответе запишите целое число.';extra={es:es}}
      else{ /* 1.5: нужна симметрия (ровно два соответствия) */
        if(I.length!==2)continue;
        var e0=exPick(r,G.E),a5=e0[0],b5=e0[1];
        if(A(function(m2){return T[m2[a5]][m2[b5]]}).length<2)continue;
        var found=null;
        for(var z=0;z<80&&!found;z++){var p2=exShuf(r,G.E).slice(0,2),x=p2[0][0],y=p2[0][1],zz=p2[1][0],ww=p2[1][1];if(r()<.5){var tt=x;x=y;y=tt}
          var okI=I.filter(function(m2){return T[m2[x]][m2[y]]>T[m2[zz]][m2[ww]]});
          if(okI.length===1)found={x:x,y:y,z:zz,w:ww,ok:okI[0]}}
        if(!found)continue;
        focus=null;extra={c:found,a:a5,b:b5};ans=[T[found.ok[a5]][found.ok[b5]]];
        qtxt='Известно, что дорога '+ng[found.x]+ng[found.y]+' длиннее дороги '+ng[found.z]+ng[found.w]+'. Определите длину дороги '+ng[a5]+ng[b5]+'. В ответе запишите целое число.'}
      if(ans.length!==1)continue;
      var S2=staged(ag,at,ng,nt,type==='1.5'?null:focus);
      if(focus&&!focus.every(function(f){return S2.map[f]!==undefined}))continue;
      if(type==='1.2'&&Object.keys(S2.map).length<n-1)continue;
      if(type==='1.5'){var df=0;for(var q5=0;q5<n;q5++)if(I[0][q5]!==I[1][q5])df++;if(df!==2||Object.keys(S2.map).length!==n-2)continue}
      if(type!=='1.5'&&S2.steps.length>5+(type==='1.2'?2:0))continue;
      /* текст */
      var pre=stars?'Схема дорог района изображена в виде графа. В таблице звёздочкой отмечено наличие дороги между пунктами (пустая клетка — дороги нет). Нумерация пунктов в таблице никак не связана с буквами на схеме. ':'Схема дорог района изображена в виде графа. В таблице указана длина каждой дороги в километрах (пустая клетка — дороги нет). Нумерация пунктов в таблице никак не связана с буквами на схеме. Длины отрезков на схеме не отражают длины дорог. ';
      /* разбор */
      var degT=at.map(function(a){return Object.keys(a).length}),degG=ag.map(function(a){return Object.keys(a).length}),sum=degG.reduce(function(a,b){return a+b},0);
      var steps=['Степени по таблице (число '+(stars?'звёздочек':'заполненных клеток')+' в строке): '+nt.map(function(h,i){return h+' — '+degT[i]}).join('; ')+'.',
        'Степени по схеме (число линий у буквы): '+ng.map(function(h,i){return h+' — '+degG[i]}).join('; ')+'.',
        'Проверка: на схеме '+m+' '+(m%10===1&&m%100!==11?'дорога':(m%10>=2&&m%10<=4&&(m%100<10||m%100>=20)?'дороги':'дорог'))+', сумма степеней = '+sum+'; в таблице '+sum+' заполненных клеток — значит, сумма степеней тоже '+sum+'. Наборы степеней в схеме и в таблице совпадают: {'+degG.slice().sort(function(a,b){return a-b}).join(', ')+'}.'].concat(S2.steps);
      var final;
      if(type==='1.1')final='Нужные пары найдены: '+ng[focus[0]]+' = '+nt[S2.map[focus[0]]]+', '+ng[focus[1]]+' = '+nt[S2.map[focus[1]]]+'. Номера по возрастанию, слитно: '+ans[0]+'.';
      else if(type==='1.2'){var mm=I[0],inv={};mm.forEach(function(c,i){inv[c]=i});final='Собираем ответ по порядку номеров: '+nt.map(function(h,j){return h+'='+ng[inv[j]]}).join(', ')+'. Получаем строку '+ans[0]+'.'}
      else if(type==='1.3'){var mp=I[0];final='Дорога '+ng[extra.e1[0]]+'–'+ng[extra.e1[1]]+' — это пункты '+nt[mp[extra.e1[0]]]+' и '+nt[mp[extra.e1[1]]]+'. В таблице на пересечении строки '+nt[mp[extra.e1[0]]]+' и столбца '+nt[mp[extra.e1[1]]]+' стоит число '+ans[0]+'.'}
      else if(type==='1.4'){var mp4=I[0],l1=T[mp4[extra.es[0][0]]][mp4[extra.es[0][1]]],l2=T[mp4[extra.es[1][0]]][mp4[extra.es[1][1]]];
        final='Дорога '+ng[extra.es[0][0]]+'–'+ng[extra.es[0][1]]+' = '+nt[mp4[extra.es[0][0]]]+'–'+nt[mp4[extra.es[0][1]]]+': '+l1+'. Дорога '+ng[extra.es[1][0]]+'–'+ng[extra.es[1][1]]+' = '+nt[mp4[extra.es[1][0]]]+'–'+nt[mp4[extra.es[1][1]]]+': '+l2+'. Сумма: '+l1+' + '+l2+' = '+ans[0]+'.'}
      else{
        var c=extra.c,un=[],unT=[];for(var k2=0;k2<n;k2++)if(S2.map[k2]===undefined){un.push(k2)}
        var usedT={};for(k2 in S2.map)usedT[S2.map[k2]]=1;for(k2=0;k2<n;k2++)if(!usedT[k2])unT.push(k2);
        steps.push('Остались неразличимые пункты: буквы '+un.map(function(k){return ng[k]}).join(', ')+' и номера '+unT.map(function(k){return nt[k]}).join(', ')+' — они «близнецы»: структура схемы не различает их. Значит допустимы две расстановки.');
        I.forEach(function(m2,ix){var asg=un.map(function(k){return ng[k]+'='+nt[m2[k]]}).join(', '),l1=T[m2[c.x]][m2[c.y]],l2=T[m2[c.z]][m2[c.w]];
          steps.push('Расстановка '+(ix+1)+': '+asg+'. Тогда дорога '+ng[c.x]+ng[c.y]+' = '+l1+', дорога '+ng[c.z]+ng[c.w]+' = '+l2+'; «'+ng[c.x]+ng[c.y]+' длиннее '+ng[c.z]+ng[c.w]+'» — '+(l1>l2?'верно':'неверно')+'.')});
        steps.push('Подходит расстановка, где условие верно. В ней дорога '+ng[extra.a]+ng[extra.b]+' — это '+nt[c.ok[extra.a]]+'–'+nt[c.ok[extra.b]]+', длина '+ans[0]+'.');
        final=null}
      if(final)steps.push(final);
      var h=['Посчитайте степени всех пунктов: по таблице и по схеме.','Найдите степень, которая встречается ровно один раз (пара «буква = номер» готова).'];
      if(S2.steps[0])h.push('Первый шаг решения: '+S2.steps[0]);if(S2.steps[1])h.push('Второй шаг решения: '+S2.steps[1]);
      return{q:pre+qtxt,svg:svgOf(G,ng,T,{stars:stars,hdr:hdr,plain:plain}),f:FM[type],h:h,s:steps,a:String(ans[0]),m:QM[type],type:type}
    }
    return null}
  function gen16(r,n,m){
    for(var att=0;att<400;att++){
      var G=genGraph(r,n,m);if(!G)continue;
      var w=exShuf(r,(function(){var a=[];for(var i=2;i<=40;i++)a.push(i);return a})()).slice(0,m);
      var T=[];for(var i=0;i<n;i++){T.push([]);for(var j=0;j<n;j++)T[i].push(0)}
      G.E.forEach(function(e,k){T[e[0]][e[1]]=w[k];T[e[1]][e[0]]=w[k]});
      var p=exShuf(r,[0,1,2,3,4,5,6].slice(0,n)).slice(0,2),a=p[0],b=p[1],P=paths(T,a,b);
      if(P.length<3||P[0][0]===P[1][0]||P[0][1].length<3)continue;
      var L=LAT.slice(0,n),roads=[];
      for(i=0;i<n;i++){var o=[];for(j=0;j<n;j++)if(T[i][j]>0)o.push(L[j]+'('+T[i][j]+')');roads.push(L[i]+': '+o.join(', '))}
      var shown=P.slice(0,6).map(function(x){return x[1].map(function(k){return L[k]}).join('–')+' = '+x[0]}).join('; ');
      return{q:'В таблице указана протяжённость дорог между пунктами '+L[0]+'–'+L[n-1]+' (в километрах; пустая клетка — прямой дороги нет). Определите длину кратчайшего пути из пункта '+L[a]+' в пункт '+L[b]+': передвигаться можно только по построенным дорогам. В ответе запишите целое число.',
        svg:svgOf(null,L,T,{noGraph:1,hdr:L}),f:FM['1.6'],
        h:['Выпишите, из каких пунктов в какие есть дороги и какой они длины.','Переберите все пути из начального пункта в конечный без повторов пунктов и сравните их длины.'],
        s:['Выписываем дороги из таблицы (пункт: сосед(длина)): '+roads.join('; ')+'.','Перебираем пути из '+L[a]+' в '+L[b]+' без повторов пунктов (показаны самые короткие): '+shown+'.','Минимум — путь '+P[0][1].map(function(k){return L[k]}).join('–')+' длиной '+P[0][0]+'.'],
        a:String(P[0][0]),m:QM['1.6'],type:'1.6'}}
    return null}
  EXGEN[1]={no:1,name:'Схема дорог и таблица',types:[
    {id:'1.1',n:'Звёздочки: два номера',d:'Найти номера двух пунктов'},
    {id:'1.2',n:'Звёздочки: все буквы',d:'Выписать буквы для всех пунктов'},
    {id:'1.3',n:'Длина одной дороги',d:'Найти длину дороги по таблице'},
    {id:'1.4',n:'Сумма двух дорог',d:'Сложить длины двух дорог'},
    {id:'1.5',n:'Условие «длиннее»',d:'Выбрать расстановку по условию'},
    {id:'1.6',n:'Кратчайший путь',d:'Найти кратчайший путь по таблице'}],
    make:function(type,r){r=r||exRnd((Date.now()^(Math.random()*4294967296))>>>0);if(type==='any')type=exPick(r,['1.1','1.2','1.3','1.3','1.4','1.4','1.5','1.6']);return gen1(type,r)}};
})();
