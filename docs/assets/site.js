(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{threshold:.06});
document.querySelectorAll('.card,.tile,.toc,.tbl-scroll,.guide,.related a,.spot').forEach(function(el){el.classList.add('rv');io.observe(el)})}
var tb=document.querySelector('.top-btn');if(tb){addEventListener('scroll',function(){tb.classList.toggle('show',scrollY>700)},{passive:true})}
var spot=document.querySelector('.spot');
if(spot){var tabs=spot.querySelectorAll('.spot-tab'),panels=spot.querySelectorAll('.spot-panel');
function bars(p){p.querySelectorAll('.bar i').forEach(function(b){b.style.width='0%';requestAnimationFrame(function(){requestAnimationFrame(function(){b.style.width=b.dataset.w+'%'})})})}
tabs.forEach(function(t){t.addEventListener('click',function(){
tabs.forEach(function(x){x.classList.remove('on')});t.classList.add('on');
panels.forEach(function(p){p.classList.remove('on')});
var p=spot.querySelector('.spot-panel[data-k=\"'+t.dataset.k+'\"]');p.classList.add('on');bars(p)})});
var first=spot.querySelector('.spot-panel.on');if(first)bars(first)}
var sb=document.getElementById('siq');
if(sb){var idx=null,res=document.getElementById('sres'),ov=document.getElementById('sov');
function closeS(){document.body.classList.remove('search-open')}
document.querySelectorAll('[data-close-search]').forEach(function(b){b.addEventListener('click',closeS)});
if(ov){ov.addEventListener('click',function(e){if(e.target===ov)closeS()})}
addEventListener('keydown',function(e){if(e.key==='Escape')closeS();
if(e.key==='/'&&!document.body.classList.contains('search-open')&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)){e.preventDefault();document.body.classList.add('search-open');sb.focus()}});
function render(){var q=sb.value.trim().toLowerCase();
if(!q){res.innerHTML='<div class="search-hint">Type to search every product we have reviewed — press Esc to close.</div>';return}
var out=idx.filter(function(p){return (p.n+' '+p.b+' '+p.c).toLowerCase().indexOf(q)>-1});
var seen={},uniq=[];out.forEach(function(p){if(!seen[p.n]){seen[p.n]=1;uniq.push(p)}});
res.innerHTML=uniq.slice(0,12).map(function(p){return '<a href="/'+p.u+'#'+p.i+'"><span>'+p.n+'<div class="meta">'+p.c+' · '+p.b+'</div></span><span class="sp">€'+p.p+'</span></a>'}).join('')||'<div class="search-hint">No products found for “'+sb.value+'”</div>'}
sb.addEventListener('input',function(){if(idx){render()}else{fetch('/assets/search.json').then(function(r){return r.json()}).then(function(d){idx=d;render()})}})}
})();