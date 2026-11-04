# -*- coding: utf-8 -*-
# Патчи v4.2.0 (после p415.py)
s = s.replace("v4.1.5", "v4.2.0").replace("v:'4.1.5'", "v:'4.2.0'")
CSS420 = r"""
/* ===== v4.2.0 ===== */
.term.fn{background:color-mix(in srgb,currentColor 16%,transparent);text-decoration-color:currentColor}
.seg2.gs{margin:6px 0 10px}
"""
_i = s.index('</style>')
s = s[:_i] + CSS420 + s[_i:]

# пол: хранение
rep("hc:r.hc?1:0,hist:hs", "hc:r.hc?1:0,g:r.g==='m'||r.g==='f'?r.g:'',hist:hs")
GSEG = '<div class="seg2 sm gs" role="group" aria-label="Как к тебе обращаться"><button class="gb" data-g="m">Парень</button><button class="gb" data-g="f">Девушка</button><button class="gb" data-g="">Не указывать</button></div>'
rep("<p>Придумай никнейм, кролик будет тебя приветствовать.</p><br>",
    "<p>Придумай никнейм, кролик будет тебя приветствовать.</p><p class=\"mu\" style=\"margin:0 0 6px\">Как к тебе обращаться? Это нужно для правильных окончаний в тексте.</p>" + GSEG + "<br>")
rep("var i=$('nk'),g=$('go');i.oninput=function(){g.disabled=!i.value.trim()};",
    "var i=$('nk'),g=$('go'),gv=S.g||'';function gsel(){app.querySelectorAll('.gb').forEach(function(b){b.classList.toggle('on',b.dataset.g===gv)})}app.querySelectorAll('.gb').forEach(function(b){b.onclick=function(){gv=b.dataset.g;gsel()}});gsel();i.oninput=function(){g.disabled=!i.value.trim()};")
rep("g.onclick=function(){S.nick=i.value.trim();if(!S.reg)", "g.onclick=function(){S.nick=i.value.trim();S.g=gv;if(!S.reg)")
rep("function shareTxt(){var n=ND();return'Я учу Python в ИТП! Уже прошёл '+n+' '+pl(n,['тему','темы','тем'])+', '+S.xp+' XP. Попробуй и ты!'}",
    "function shareTxt(){var n=ND(),v=S.g==='f'?'Уже прошла ':S.g==='m'?'Уже прошёл ':'Пройдено: ';return'Я учу Python в ИТП! '+v+n+' '+pl(n,['тему','темы','тем'])+', '+S.xp+' XP. Попробуй и ты!'}")
# настройки: выбор обращения
rep('<h2 style="font-size:20px">Настройки</h2><h3>Резервная копия</h3>', '<h2 style="font-size:20px">Настройки</h2><h3>Обращение</h3>' + GSEG + '<h3>Резервная копия</h3>')
rep("    ['Закрыть',null,1]]);\n}", "    ['Закрыть',null,1]]);\n  function gsel(){o.querySelectorAll('.gb').forEach(function(b){b.classList.toggle('on',b.dataset.g===(S.g||''))})}\n  o.querySelectorAll('.gb').forEach(function(b){b.onclick=function(){S.g=b.dataset.g;save();gsel()}});gsel();\n}")

# ---------- моржовый оператор в условии while (Skulpt его не знает) ----------
WAL = r"""
/* Skulpt не поддерживает :=. Условие while (name := выражение) ... переписываем в равносильный код:
   name = выражение до цикла, в условии name, а в конце тела и перед каждым continue присваивание повторяется. */
function wal(code){
  if(code.indexOf(':=')<0)return{code:code,map:null};
  var L=code.split('\n'),o=[],mp=[],loops=[];
  function ind(l){return l.match(/^[ \t]*/)[0].length}
  function push(l,n){o.push(l);mp.push(n)}
  for(var i=0;i<L.length;i++){
    var l=L[i],t=l.trim(),n=i+1;
    if(t&&t[0]!=='#'){
      var cur=ind(l);
      while(loops.length&&loops[loops.length-1].ind>=cur){var p=loops.pop();if(p.w)push(' '.repeat(p.ind+4)+p.name+' = '+p.expr,p.n)}
      var m=/^(\s*)while\s*\(\s*([A-Za-z_]\w*)\s*:=/.exec(l);
      if(m){
        var a=l.indexOf('(',m[1].length),s=l.indexOf(':=',a)+2,d=1,j=s,q='';
        for(;j<l.length&&d>0;j++){var c=l[j];if(q){if(c===q)q='';continue}if(c==='"'||c==="'"){q=c;continue}if(c==='(')d++;else if(c===')')d--}
        var rest=l.slice(j).replace(/#.*$/,'').replace(/\s+$/,'');
        if(d===0&&/:$/.test(rest)){
          var ex=l.slice(s,j-1).trim(),rs=rest.slice(0,-1);
          push(m[1]+m[2]+' = '+ex,n);push(m[1]+'while '+(rs.trim()?m[2]+rs:m[2])+':',n);
          loops.push({ind:cur,w:1,name:m[2],expr:ex,n:n});continue}
      }
      if(/^(while|for)\b.*:\s*(#.*)?$/.test(t)){loops.push({ind:cur,w:0});push(l,n);continue}
      var top=loops.length?loops[loops.length-1]:null;
      if(top&&top.w){
        if(t==='continue'){push(' '.repeat(cur)+top.name+' = '+top.expr,n);push(l,n);continue}
        var mc=/^(.*:\s*)continue\s*$/.exec(l);
        if(mc){push(mc[1]+top.name+' = '+top.expr+'; continue',n);continue}
      }
    }
    push(l,n);
  }
  while(loops.length){var p2=loops.pop();if(p2.w)push(' '.repeat(p2.ind+4)+p2.name+' = '+p2.expr,p2.n)}
  return{code:o.join('\n'),map:mp};
}
"""
rep("function exec(code,src){", WAL + "function exec(code,src){\n  var OC=code,WL=wal(code);code=WL.code;")
rep("function fin2(err){var o=out;", "function fin2(err){if(err){if(WL.map)err=err.replace(/(line |строке )(\\d+)/g,function(m0,a,b){return a+(WL.map[+b-1]||b)});if(/bad input|SyntaxError/.test(err)&&/:=/.test(OC))err+='. Оператор := в ИТП работает только в условии цикла while'}var o=out;")

# ---------- фон нажимаемых слов в цвет функции ----------
rep("function fcol(n){", "function fbg(n){var c=fcol(n);return/^hsl\\(/.test(c)?c.slice(0,-1)+' / .17)':'var(--soft)'}\nfunction fcol(n){")
rep("' style=\"color:'+fcol(n)+'\"'", "' style=\"color:'+fcol(n)+';background:'+fbg(n)+'\"'")

# в цели проекта переносы строк превращаем в абзацы
rep("<b>Цель</b><p>'+esc(it.q)+'</p>", "<b>Цель</b><p>'+esc(it.q).replace(/\\n/g,'</p><p>')+'</p>")
