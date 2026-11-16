(function(){
var L=function(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}};
var W=function(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
function favs(){return L('ks_fav',[])}
function toggleFav(slug,btn){var f=favs(),i=f.indexOf(slug);if(i<0)f.push(slug);else f.splice(i,1);W('ks_fav',f);if(btn)paint(btn,slug)}
function paint(b,s){var on=favs().indexOf(s)>=0;b.classList.toggle('on',on);b.textContent=on?'♥':'♡';b.setAttribute('aria-pressed',on)}
document.querySelectorAll('.fav').forEach(function(b){var s=b.dataset.slug;paint(b,s);b.addEventListener('click',function(ev){ev.preventDefault();ev.stopPropagation();toggleFav(s,b)})});

/* home: resume banner, search, filters */
var rb=document.getElementById('resume');
if(rb){var last=L('ks_last',null);if(last&&last.slug){rb.style.display='flex';rb.querySelector('a').href='/kahani/'+last.slug+'.html';rb.querySelector('span').textContent='जहाँ छोड़ा था वहीं से सुनें: '+last.title}}
var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('.card[data-t]')),chips=[].slice.call(document.querySelectorAll('.chip')),cat='all',onlyFav=false;
function apply(){var t=(q?q.value:'').trim().toLowerCase(),f=favs(),n=0;
 cards.forEach(function(c){var ok=(cat==='all'||c.dataset.c===cat)&&(!t||c.dataset.t.toLowerCase().indexOf(t)>=0)&&(!onlyFav||f.indexOf(c.dataset.s)>=0);c.classList.toggle('hide',!ok);if(ok)n++});
 var e=document.getElementById('empty');if(e)e.classList.toggle('hide',n>0)}
if(q)q.addEventListener('input',apply);
chips.forEach(function(ch){ch.addEventListener('click',function(){chips.forEach(function(x){x.classList.remove('on')});ch.classList.add('on');if(ch.dataset.fav){onlyFav=true;cat='all'}else{onlyFav=false;cat=ch.dataset.c}apply()})});
var rnd=document.getElementById('random');
if(rnd)rnd.addEventListener('click',function(){var c=cards[Math.floor(Math.random()*cards.length)];location.href='/kahani/'+c.dataset.s+'.html'});

/* story page: player */
var a=document.getElementById('audio'),btn=document.getElementById('pbtn');
if(a&&btn){
var slug=document.body.dataset.slug,title=document.body.dataset.title,bar=document.getElementById('bar'),tm=document.getElementById('time'),spd=document.getElementById('spd'),note=document.getElementById('note'),nx=document.getElementById('next');
var useTTS=false,rate=1,text=document.getElementById('story').innerText;
function fmt(s){s=Math.floor(s||0);return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
function icon(p){btn.textContent=p?'⏸':'▶';btn.setAttribute('aria-label',p?'रोकें':'सुनें')}
function tts(){if(!('speechSynthesis' in window)){note.textContent='आपके ब्राउज़र में आवाज़ की सुविधा नहीं है।';return}
 useTTS=true;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='hi-IN';u.rate=rate;
 var v=speechSynthesis.getVoices().filter(function(x){return x.lang&&x.lang.indexOf('hi')===0})[0];if(v)u.voice=v;
 u.onend=function(){icon(false);if(nx)nx.classList.remove('hide')};speechSynthesis.speak(u);icon(true);
 note.textContent='डेमो आवाज़ चल रही है। असली ऑडियो जल्द आएगा।'}
a.addEventListener('error',function(){if(!useTTS)tts()});
var lastSave=0,pos=L('ks_pos',{});
a.addEventListener('loadedmetadata',function(){if(pos[slug]&&pos[slug]<a.duration-5)a.currentTime=pos[slug]});
a.addEventListener('timeupdate',function(){if(a.duration){bar.value=a.currentTime/a.duration*100;tm.textContent=fmt(a.currentTime)+' / '+fmt(a.duration)}
 var n=Date.now();if(n-lastSave>3000){lastSave=n;pos[slug]=a.currentTime;W('ks_pos',pos);W('ks_last',{slug:slug,title:title})}});
a.addEventListener('ended',function(){icon(false);pos[slug]=0;W('ks_pos',pos);if(nx)nx.classList.remove('hide')});
btn.addEventListener('click',function(){
 if(useTTS){if(speechSynthesis.speaking&&!speechSynthesis.paused){speechSynthesis.pause();icon(false)}else if(speechSynthesis.paused){speechSynthesis.resume();icon(true)}else tts();return}
 if(a.paused){var p=a.play();if(p&&p.catch)p.catch(function(){tts()});icon(true);W('ks_last',{slug:slug,title:title})}else{a.pause();icon(false)}});
document.getElementById('back').onclick=function(){if(!useTTS)a.currentTime=Math.max(0,a.currentTime-10)};
document.getElementById('fwd').onclick=function(){if(!useTTS&&a.duration)a.currentTime=Math.min(a.duration,a.currentTime+10)};
bar.oninput=function(){if(!useTTS&&a.duration)a.currentTime=bar.value/100*a.duration};
var R=[1,1.25,1.5,0.85],ri=0;spd.onclick=function(){ri=(ri+1)%R.length;rate=R[ri];a.playbackRate=rate;spd.textContent=rate+'×'};
var sl=document.getElementById('sleep'),st=null,S=[0,15,30,60],si=0;
sl.onclick=function(){si=(si+1)%S.length;clearTimeout(st);if(S[si]){sl.textContent='😴 '+S[si]+' मिनट';st=setTimeout(function(){a.pause();if('speechSynthesis' in window)speechSynthesis.cancel();icon(false)},S[si]*60000)}else sl.textContent='😴 स्लीप टाइमर'};
window.addEventListener('pagehide',function(){if('speechSynthesis' in window)speechSynthesis.cancel()});
var cp=document.getElementById('copy');if(cp)cp.onclick=function(){var u=location.href;if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){cp.textContent='कॉपी हो गया ✓'});else prompt('लिंक कॉपी करें',u)};
var ns=document.getElementById('nshare');if(ns&&navigator.share){ns.classList.remove('hide');ns.onclick=function(){navigator.share({title:title,url:location.href})}}
}
})();