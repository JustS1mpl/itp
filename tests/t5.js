var vm=require('vm'),fs=require('fs');global.window=global;
vm.runInThisContext(fs.readFileSync('v5/a_gen.js','utf8').split('(function(){')[0]);
vm.runInThisContext(fs.readFileSync('v5/a_gen5.js','utf8'));
var D=JSON.parse(fs.readFileSync('exam/q5.json','utf8')),bad=0;
Object.keys(D).forEach(function(id){var e=D[id];var q={query:{rule:e.rule,params:e.params,form:e.form,q:e.q}};exFill5(q);
 var st=e.stmt.replace('единицы 1','1').split('\n'),txt=q.pr+'\n'+q.qq;
 if(q._v!==e.ans){bad++;console.log('ANS',id,q._v,e.ans)}
 if(txt!==st.join('\n')){bad++;console.log('TXT',id,'\n'+txt+'\n---\n'+st.join('\n'))}});
console.log('json bad',bad);
