# Патчи v4.3.0 (после p420.py): новые темы 9 и 10
s = s.replace("v4.2.0", "v4.3.0").replace("v:'4.2.0'", "v:'4.3.0'")

# Skulpt 1.2.0 понимает только латиницу в isalpha/isalnum/isupper/islower/title/swapcase: чиним для кириллицы и других букв
rep("SKOK=true;res(true)", "SKOK=true;skPatch();res(true)")
rep("function skReady(){", r"""function skPatch(){try{var M=Sk.builtin.str.prototype;
var RU=/\p{Lu}/u,RL=/\p{Ll}/u,RT=/\p{Lt}/u,RA=/^\p{L}+$/u,RN=/^[\p{L}\p{Nd}]+$/u;
function B(v){return v?Sk.builtin.bool.true$:Sk.builtin.bool.false$}
function set(n,f){var d=M[n];if(d){d.$meth=f;if(d.d$def)d.d$def.$meth=f}}
set('isalpha',function(){return B(RA.test(this.v))});
set('isalnum',function(){return B(RN.test(this.v))});
set('isupper',function(){var v=this.v;return B((RU.test(v)||RT.test(v))&&!RL.test(v))});
set('islower',function(){var v=this.v;return B(RL.test(v)&&!RU.test(v)&&!RT.test(v))});
set('title',function(){var o='',prev=false;for(var ch of this.v){var cased=RU.test(ch)||RL.test(ch)||RT.test(ch);if(cased){o+=prev?ch.toLowerCase():ch.toUpperCase()}else o+=ch;prev=cased}return new Sk.builtin.str(o)});
set('swapcase',function(){var o='';for(var ch of this.v){o+=RU.test(ch)?ch.toLowerCase():RL.test(ch)?ch.toUpperCase():ch}return new Sk.builtin.str(o)});
}catch(e){}}
function skReady(){""")
