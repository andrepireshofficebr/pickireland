(function(){
/* O bloco de reveal por IntersectionObserver foi removido em 2026-09-06: ele punha
   opacity:0 em todo card/tabela/guia e devolvia a visibilidade so ao rolar, deixando 72% da
   pagina invisivel em repouso. Ver o comentario no CSS (.rv) para a medicao. */
/* galeria de fotos do produto: abre ao clicar na foto do card */
var galBtns=document.querySelectorAll('.pimg-btn');
if(galBtns.length){var dlg=document.createElement('dialog');dlg.className='gal';dlg.id='gallery';dlg.setAttribute('aria-label','Product photos');
dlg.innerHTML='<div class=\"gal-top\"><h2></h2><button type=\"button\" class=\"gal-x\" aria-label=\"Close\">×</button></div><div class=\"gal-stage\"><button type=\"button\" class=\"gal-nav gal-prev\" aria-label=\"Previous photo\">‹</button><img alt=\"\"><button type=\"button\" class=\"gal-nav gal-next\" aria-label=\"Next photo\">›</button></div><div class=\"gal-thumbs\"></div><div class=\"gal-foot\"><span class=\"gal-count\"></span><a target=\"_blank\">Check price on Amazon.ie</a></div>';
document.body.appendChild(dlg);
var gImg=dlg.querySelector('.gal-stage img'),gTh=dlg.querySelector('.gal-thumbs'),gCt=dlg.querySelector('.gal-count'),gA=dlg.querySelector('.gal-foot a'),gH=dlg.querySelector('h2'),gList=[],gI=0,gName='';
function gShow(i){gI=(i+gList.length)%gList.length;gImg.src=gList[gI];gImg.alt=gName+' — photo '+(gI+1)+' of '+gList.length;
gCt.textContent=gList.length>1?(gI+1)+' / '+gList.length:'';
gTh.querySelectorAll('button').forEach(function(b,k){b.setAttribute('aria-current',k===gI?'true':'false')})}
galBtns.forEach(function(b){b.addEventListener('click',function(){
try{gList=JSON.parse(b.dataset.gallery)}catch(e){gList=[b.querySelector('img').src]}
gName=b.dataset.name;gH.textContent=gName;gA.href=b.dataset.href;gA.rel=b.dataset.aff==='1'?'sponsored noopener':'nofollow noopener';
var multi=gList.length>1;dlg.querySelectorAll('.gal-nav').forEach(function(n){n.hidden=!multi});gTh.hidden=!multi;
gTh.innerHTML=multi?gList.map(function(u,k){return '<button type=\"button\" aria-label=\"Photo '+(k+1)+'\"><img src=\"'+u+'\" alt=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></button>'}).join(''):'';
gTh.querySelectorAll('button').forEach(function(t,k){t.addEventListener('click',function(){gShow(k)})});
gShow(0);dlg.showModal();
if(window.gtag)gtag('event','product_gallery_open',{product:gName,photos:gList.length})})});
dlg.querySelector('.gal-x').addEventListener('click',function(){dlg.close()});
dlg.querySelector('.gal-prev').addEventListener('click',function(){gShow(gI-1)});
dlg.querySelector('.gal-next').addEventListener('click',function(){gShow(gI+1)});
dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
dlg.addEventListener('keydown',function(e){if(gList.length<2)return;if(e.key==='ArrowLeft')gShow(gI-1);if(e.key==='ArrowRight')gShow(gI+1)});
var tx=null;gImg.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
gImg.addEventListener('touchend',function(e){if(tx===null||gList.length<2)return;var d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>40)gShow(gI+(d<0?1:-1));tx=null})}
var tb=document.querySelector('.top-btn');if(tb){addEventListener('scroll',function(){tb.classList.toggle('show',scrollY>700)},{passive:true})}
var spot=document.querySelector('.spot');
if(spot){var tabs=spot.querySelectorAll('.spot-tab'),panels=spot.querySelectorAll('.spot-panel');
function bars(p){p.querySelectorAll('.bar i').forEach(function(b){b.style.transition='none';b.style.width='0%';void b.offsetWidth;b.style.transition='';b.style.width=b.dataset.w+'%'})}
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