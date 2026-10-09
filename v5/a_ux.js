/* v5.3.0: цвет системной панели браузера под тему */
(function(){
  var m=document.querySelector('meta[name="theme-color"]');
  if(!m){m=document.createElement('meta');m.name='theme-color';document.head.appendChild(m)}
  function sync(){try{var c=getComputedStyle(document.body).backgroundColor;if(c)m.content=c}catch(e){}}
  sync();
  try{new MutationObserver(sync).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']})}catch(e){}
  try{matchMedia('(prefers-color-scheme:dark)').addEventListener('change',sync)}catch(e){}
  setTimeout(sync,300);
})();
