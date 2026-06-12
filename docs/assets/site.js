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
})();