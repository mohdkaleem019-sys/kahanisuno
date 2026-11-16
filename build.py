#!/usr/bin/env python3
"""KahaniSuno site builder.
Usage:  python3 build.py        -> creates ./site (upload its CONTENTS to GitHub root) and kahanisuno-upload-me.zip
Edit stories.json to add stories. Put MP3s in ./audio named <slug>.mp3 (they are copied into the site).
"""
import os, shutil, html, json, datetime, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.khanisuno.in"
NAME = "KahaniSuno"
CONTACT_EMAIL = "your-email@example.com"   # CHANGE
SOCIAL = ""            # WhatsApp/Telegram channel link
YOUTUBE = ""           # YouTube channel link
GA_ID = ""             # Google Analytics ID like G-XXXXXXXXXX (optional)
OUT = os.path.join(HERE, "site")

CATS = {
    "horror": ("हॉरर कहानियाँ", "हॉरर", "👻", "रात में सुनने वाली डरावनी हिंदी ऑडियो कहानियाँ। छोटे एपिसोड, हर बार नया रोमांच।"),
    "rahasya": ("रहस्य कहानियाँ", "रहस्य", "🔍", "रहस्य और जासूसी की हिंदी ऑडियो कहानियाँ, जिनका अंत आपको चौंका देगा।"),
    "bedtime": ("सोने से पहले की कहानियाँ", "सोने से पहले", "🌙", "बच्चों और बड़ों के लिए सुकून भरी हिंदी कहानियाँ, जो नींद से पहले सुनने के लिए बनी हैं।"),
}
e = html.escape
STORIES = json.load(open(os.path.join(HERE, "stories.json"), encoding="utf-8"))
AUDIO_SRC = os.path.join(HERE, "audio")
TODAY = datetime.date.today().isoformat()

def has_audio(slug): return os.path.exists(os.path.join(AUDIO_SRC, slug + ".mp3"))

CSS = """:root{--bg:#080c1c;--card:#12182f;--card2:#1a2242;--ink:#f1f3fc;--mute:#a9b1cf;--acc:#ffd166;--acc2:#ff5d8f;--line:#262f52}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:radial-gradient(900px 500px at 85% -5%,#27358a 0%,transparent 60%),radial-gradient(700px 400px at 0% 10%,#3a1a5e 0%,transparent 55%),var(--bg);background-attachment:fixed;color:var(--ink);font-family:"Noto Sans Devanagari","Mukta",system-ui,sans-serif;font-size:18px;line-height:1.8}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1000px;margin:0 auto;padding:0 18px}
header{position:sticky;top:0;z-index:30;background:rgba(8,12,28,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 0;flex-wrap:wrap}
.logo{font-weight:800;font-size:23px;color:var(--ink)}.logo span{color:var(--acc)}.logo:hover{text-decoration:none}
nav a{margin-left:14px;color:var(--mute);font-size:16px}
.hero{text-align:center;padding:54px 0 20px;position:relative}
.moon{width:110px;height:110px;border-radius:50%;margin:0 auto 18px;background:radial-gradient(circle at 35% 35%,#fff7d6,#ffd166 60%,#e8a838);box-shadow:0 0 70px 18px rgba(255,209,102,.35);animation:glow 4s ease-in-out infinite}
@keyframes glow{50%{box-shadow:0 0 95px 28px rgba(255,209,102,.5)}}
.hero h1{font-size:clamp(30px,7vw,52px);line-height:1.25;margin:0 0 12px}
.hero h1 b{color:var(--acc)}
.hero p{color:var(--mute);max-width:640px;margin:0 auto 22px}
.btn{display:inline-block;background:var(--acc);color:#1a1a1a;font-weight:700;padding:12px 26px;border-radius:999px;border:0;cursor:pointer;font-size:17px;font-family:inherit;margin:4px}
.btn:hover{text-decoration:none;filter:brightness(1.08)}.btn.alt{background:transparent;color:var(--ink);border:1px solid var(--line)}
.stats{display:flex;gap:22px;justify-content:center;color:var(--mute);font-size:15px;margin-top:16px;flex-wrap:wrap}
h2{margin:40px 0 12px;font-size:26px}
.search{width:100%;padding:14px 18px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:17px;font-family:inherit;margin:8px 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.chip{background:var(--card);border:1px solid var(--line);color:var(--ink);padding:6px 16px;border-radius:999px;font-size:15px;cursor:pointer;font-family:inherit}
.chip.on,.chip:hover{background:var(--acc);color:#1a1a1a;text-decoration:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:block;color:var(--ink);position:relative;transition:transform .18s,border-color .18s}
.card:hover{border-color:var(--acc);transform:translateY(-4px);text-decoration:none}
.cover{height:128px;display:flex;align-items:center;justify-content:center;font-size:54px;position:relative}
.c-horror{background:linear-gradient(135deg,#2b0a1c,#7a1633 60%,#c0392b)}
.c-rahasya{background:linear-gradient(135deg,#071a33,#124a7a 60%,#2aa6c9)}
.c-bedtime{background:linear-gradient(135deg,#14123a,#3b3a8f 60%,#8e7cd8)}
.cb{padding:14px 16px 16px}
.card h3{margin:2px 0 6px;font-size:20px;line-height:1.4}.card p{margin:0;color:var(--mute);font-size:15px;line-height:1.6}
.tag{font-size:13px;color:#1a1a1a;background:var(--acc);padding:1px 10px;border-radius:999px;display:inline-block}
.tag.rahasya{background:#7bdff2}.tag.bedtime{background:#c3b8ff}
.min{position:absolute;right:10px;bottom:8px;background:rgba(0,0,0,.55);font-size:12px;padding:0 8px;border-radius:8px;line-height:1.7}
.fav{position:absolute;right:10px;top:10px;background:rgba(0,0,0,.45);border:0;color:#fff;border-radius:50%;width:36px;height:36px;font-size:18px;cursor:pointer;z-index:2}
.fav.on{color:var(--acc2)}
.resume{display:none;background:linear-gradient(90deg,#2a2060,#4a2a7a);border:1px solid var(--line);border-radius:16px;padding:14px 18px;margin:20px 0;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.story{font-size:20px;line-height:2.05}.story p{margin:0 0 18px}
.crumbs{font-size:15px;color:var(--mute);padding-top:20px}
.banner{border-radius:20px;padding:30px 20px;text-align:center;margin:14px 0;font-size:64px}
.player{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;margin:18px 0}
.prow{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.pbtn{background:var(--acc);color:#1a1a1a;border:0;border-radius:50%;width:58px;height:58px;font-size:24px;cursor:pointer}
.sbtn{background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:8px 12px;cursor:pointer;font-family:inherit;font-size:15px}
input[type=range]{flex:1;min-width:140px;accent-color:var(--acc)}
.time{color:var(--mute);font-size:14px;min-width:90px}
.note{color:var(--mute);font-size:14px;margin:8px 0 0}
.share{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.pn{display:flex;justify-content:space-between;gap:12px;margin:30px 0;flex-wrap:wrap}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0}
summary{cursor:pointer;font-weight:700}
.cta{background:linear-gradient(135deg,#1c2a6b,#5a2a7a);border-radius:20px;padding:26px;text-align:center;margin:40px 0}
footer{border-top:1px solid var(--line);margin-top:48px;padding:26px 0;color:var(--mute);font-size:15px;text-align:center}
footer a{margin:0 8px}
.hide{display:none!important}
"""

JS = r"""(function(){
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
})();"""

def ga():
    return f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}")</script>' if GA_ID else ""

def head(title, desc, path, extra="", body=""):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#080c1c">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/manifest.json">
<link rel="alternate" type="application/rss+xml" title="{NAME}" href="/feed.xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="hi_IN">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">{ga()}{extra}</head><body {body}>
<header><div class="wrap nav"><a class="logo" href="/">Kahani<span>Suno</span></a>
<nav><a href="/category/horror.html">हॉरर</a><a href="/category/rahasya.html">रहस्य</a><a href="/category/bedtime.html">सोने से पहले</a><a href="/about.html">हमारे बारे में</a></nav></div></header>
<main class="wrap">"""

def foot(js=True):
    links = ""
    if SOCIAL: links += f'<a class="btn" href="{e(SOCIAL)}" rel="noopener">📲 नई कहानी का अलर्ट पाएँ</a>'
    if YOUTUBE: links += f'<a class="btn alt" href="{e(YOUTUBE)}" rel="noopener">▶ YouTube पर देखें</a>'
    cta = f'<div class="cta"><h2 style="margin:0 0 8px">हर रात एक नई कहानी</h2><p style="margin:0 0 10px;color:var(--mute)">नया एपिसोड आते ही सबसे पहले सुनिए।</p>{links}</div>' if links else ""
    return f"""{cta}</main><footer><div class="wrap">
<p><a href="/about.html">हमारे बारे में</a><a href="/privacy.html">प्राइवेसी</a><a href="/contact.html">संपर्क</a><a href="/feed.xml">RSS</a></p>
<p>© {datetime.date.today().year} KahaniSuno। कहानियाँ AI की मदद से लिखी और सुनाई गई हैं।</p></div></footer><script src="/assets/site.js" defer></script></body></html>"""

def card(s):
    c = s["category"]
    return (f'<a class="card" href="/kahani/{s["slug"]}.html" data-s="{s["slug"]}" data-c="{c}" data-t="{e(s["title"]+" "+s["hook"]+" "+s["hinglish"])}">'
            f'<div class="cover c-{c}"><button class="fav" data-slug="{s["slug"]}" aria-label="पसंद में जोड़ें">♡</button><span>{CATS[c][2]}</span><span class="min">{s["minutes"]} मिनट</span></div>'
            f'<div class="cb"><span class="tag {c}">{CATS[c][1]}</span><h3>{e(s["title"])}</h3><p>{e(s["hook"])}</p></div></a>')

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "audio"), exist_ok=True)
if os.path.isdir(AUDIO_SRC):
    for f in os.listdir(AUDIO_SRC):
        if f.endswith(".mp3"): shutil.copy(os.path.join(AUDIO_SRC, f), os.path.join(OUT, "audio", f))
write("audio/README.txt", "MP3 files go here, named <story-slug>.mp3\n")
write("assets/style.css", CSS)
write("assets/site.js", JS)
write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#080c1c"/><circle cx="32" cy="32" r="16" fill="#ffd166"/><circle cx="40" cy="26" r="14" fill="#080c1c"/></svg>')
write("manifest.json", json.dumps({"name": NAME, "short_name": NAME, "start_url": "/", "display": "standalone", "background_color": "#080c1c", "theme_color": "#080c1c", "lang": "hi", "icons": [{"src": "/assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False))

faq = [("KahaniSuno क्या है?", "KahaniSuno एक मुफ़्त हिंदी ऑडियो कहानी वेबसाइट है, जहाँ हॉरर, रहस्य और सोने से पहले की कहानियाँ सुनी जा सकती हैं।"),
       ("क्या कहानियाँ मुफ़्त हैं?", "हाँ, सभी कहानियाँ पढ़ने और सुनने के लिए पूरी तरह मुफ़्त हैं।"),
       ("क्या मैं कहानी बीच में छोड़कर बाद में सुन सकता हूँ?", "हाँ, आपकी जगह इसी डिवाइस पर याद रहती है, इसलिए आप वहीं से आगे सुन सकते हैं।"),
       ("नई कहानियाँ कब आती हैं?", "हम नियमित रूप से नए एपिसोड जोड़ते हैं। अपडेट के लिए पेज के नीचे दिया चैनल लिंक देखें।")]
jl = [{"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE, "inLanguage": "hi"},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
home = head("KahaniSuno | हिंदी ऑडियो कहानियाँ: हॉरर, रहस्य और सोने से पहले की कहानियाँ", "हिंदी में मुफ़्त ऑडियो कहानियाँ सुनिए: डरावनी हॉरर कहानियाँ, रहस्य कथाएँ और सोने से पहले की सुकून भरी कहानियाँ।", "/",
            "".join('<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + "</script>" for j in jl))
home += f"""<section class="hero"><div class="moon"></div><h1>रात की कहानियाँ, <b>कानों के लिए।</b></h1>
<p>हिंदी ऑडियो कहानियाँ: डरावनी हॉरर, चौंकाने वाले रहस्य और नींद से पहले की मीठी कहानियाँ। छोटे एपिसोड, कहीं भी सुनिए।</p>
<a class="btn" href="/kahani/{STORIES[0]["slug"]}.html">▶ पहली कहानी सुनें</a><button id="random" class="btn alt">🎲 कोई भी कहानी</button>
<div class="stats"><span>📚 {len(STORIES)} कहानियाँ</span><span>🆓 पूरी तरह मुफ़्त</span><span>📱 मोबाइल पर तेज़</span></div></section>
<div id="resume" class="resume"><span></span><a class="btn" href="#">▶ जारी रखें</a></div>
<input id="q" class="search" type="search" placeholder="🔎 कहानी खोजें... जैसे हवेली, ट्रेन, जुगनू" aria-label="कहानी खोजें">
<div class="chips"><button class="chip on" data-c="all">सब</button>""" + "".join(f'<button class="chip" data-c="{c}">{v[2]} {v[1]}</button>' for c, v in CATS.items()) + """<button class="chip" data-fav="1">♥ मेरी पसंद</button></div>
<div class="grid">""" + "".join(card(s) for s in STORIES) + '</div><p id="empty" class="hide" style="text-align:center;color:var(--mute)">कोई कहानी नहीं मिली।</p>'
for c, v in CATS.items():
    home += f'<h2><a href="/category/{c}.html">{v[2]} {v[0]}</a></h2><p style="color:var(--mute);margin-top:0">{e(v[3])}</p>'
home += "<h2>अक्सर पूछे जाने वाले सवाल</h2>" + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
write("index.html", home + foot())

for c, v in CATS.items():
    items = [s for s in STORIES if s["category"] == c]
    p = head(f"{v[0]} | हिंदी ऑडियो | KahaniSuno", v[3], f"/category/{c}.html") + f'<p class="crumbs"><a href="/">होम</a> › {v[0]}</p><h1>{v[2]} {v[0]}</h1><p style="color:var(--mute)">{e(v[3])}</p><div class="grid">' + "".join(card(s) for s in items) + "</div>" + foot()
    write(f"category/{c}.html", p)

for i, s in enumerate(STORIES):
    slug, title, cat = s["slug"], s["title"], s["category"]
    url = f"{SITE}/kahani/{slug}.html"
    desc = s["hook"] + " हिंदी ऑडियो कहानी: पूरा पाठ पढ़ें और सुनें।"
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": title, "inLanguage": "hi", "description": s["hook"], "url": url, "datePublished": TODAY, "publisher": {"@type": "Organization", "name": NAME}}
    lds = ['<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"]
    if has_audio(slug):
        lds.append('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "AudioObject", "name": title, "contentUrl": f"{SITE}/audio/{slug}.mp3", "encodingFormat": "audio/mpeg", "inLanguage": "hi", "description": s["hook"]}, ensure_ascii=False) + "</script>")
    p = head(f"{title} | हिंदी ऑडियो कहानी | KahaniSuno", desc, f"/kahani/{slug}.html", "".join(lds), f'data-slug="{slug}" data-title="{e(title)}"')
    p += f'<p class="crumbs"><a href="/">होम</a> › <a href="/category/{cat}.html">{CATS[cat][0]}</a> › {e(title)}</p>'
    p += f'<div class="banner c-{cat}">{CATS[cat][2]}</div><h1 style="margin:10px 0 4px">{e(title)}</h1><p style="color:var(--mute);margin:0">{e(s["hook"])} · {s["minutes"]} मिनट</p>'
    p += f"""<div class="player"><audio id="audio" preload="none" src="/audio/{slug}.mp3"></audio>
<div class="prow"><button id="pbtn" class="pbtn" aria-label="सुनें">▶</button><button id="back" class="sbtn" aria-label="10 सेकंड पीछे">⏪ 10</button><button id="fwd" class="sbtn" aria-label="10 सेकंड आगे">10 ⏩</button><button id="spd" class="sbtn" aria-label="गति">1×</button><button id="sleep" class="sbtn">😴 स्लीप टाइमर</button>
<input id="bar" type="range" min="0" max="100" value="0" step="0.1" aria-label="प्रगति"><span id="time" class="time">0:00 / 0:00</span></div>
<p id="note" class="note">▶ दबाकर कहानी सुनें।</p></div>"""
    wa = "https://wa.me/?text=" + __import__("urllib.parse").parse.quote(f"{title}: यह हिंदी ऑडियो कहानी सुनिए\n{url}")
    p += f'<div class="share"><a class="btn" href="{wa}" rel="noopener">WhatsApp पर भेजें</a><button id="copy" class="btn alt">🔗 लिंक कॉपी करें</button><button id="nshare" class="btn alt hide">शेयर करें</button><button class="fav btn alt" style="position:static;width:auto;height:auto;border-radius:999px;padding:12px 22px;font-size:17px" data-slug="{slug}" aria-label="पसंद">♡</button></div>'
    p += '<article id="story" class="story">' + "".join(f"<p>{e(t)}</p>" for t in s["paragraphs"]) + "</article>"
    prev = STORIES[i - 1] if i > 0 else None
    nxt = STORIES[i + 1] if i < len(STORIES) - 1 else None
    p += '<div class="pn">' + (f'<a class="btn alt" href="/kahani/{prev["slug"]}.html">← {e(prev["title"])}</a>' if prev else "<span></span>") + (f'<a id="next" class="btn hide" href="/kahani/{nxt["slug"]}.html">अगली कहानी: {e(nxt["title"])} →</a>' if nxt else "") + "</div>"
    rel = [x for x in STORIES if x["category"] == cat and x["slug"] != slug][:3]
    if len(rel) < 3: rel += [x for x in STORIES if x["category"] != cat and x["slug"] != slug][:3 - len(rel)]
    p += "<h2>ये भी सुनिए</h2><div class=\"grid\">" + "".join(card(x) for x in rel) + "</div>"
    write(f"kahani/{slug}.html", p + foot())

write("about.html", head("हमारे बारे में | KahaniSuno", "KahaniSuno क्या है और हम कहानियाँ कैसे बनाते हैं।", "/about.html") + "<h1>हमारे बारे में</h1><p>KahaniSuno हिंदी में ऑडियो कहानियाँ सुनाने वाली वेबसाइट है। हम हॉरर, रहस्य और सोने से पहले की कहानियाँ छोटे एपिसोड में लाते हैं, ताकि आप कहीं भी, कभी भी सुन सकें।</p><p>हमारी कहानियाँ AI की मदद से लिखी और तैयार की जाती हैं, और हम उन्हें लगातार बेहतर बना रहे हैं।</p>" + foot())
write("privacy.html", head("प्राइवेसी पॉलिसी | KahaniSuno", "KahaniSuno की प्राइवेसी पॉलिसी।", "/privacy.html") + "<h1>प्राइवेसी पॉलिसी</h1><p>यह वेबसाइट आपसे कोई खाता या निजी जानकारी नहीं माँगती। कहानियाँ सुनने के लिए लॉगिन की ज़रूरत नहीं है।</p><p>आपकी पसंद और सुनने की जगह सिर्फ़ आपके अपने ब्राउज़र में सेव होती है, हमारे सर्वर पर नहीं।</p><p>अगर हम एनालिटिक्स या विज्ञापन जोड़ते हैं, तो इस पेज पर उसकी जानकारी दी जाएगी। तीसरे पक्ष की सेवाएँ (जैसे Google Fonts, YouTube, Google Analytics) अपनी नीतियों के अनुसार कुकीज़ का उपयोग कर सकती हैं।</p>" + foot())
write("contact.html", head("संपर्क करें | KahaniSuno", "KahaniSuno से संपर्क करें।", "/contact.html") + f'<h1>संपर्क करें</h1><p>कहानी की फ़रमाइश या सुझाव के लिए ईमेल करें: <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a></p>' + foot())
write("404.html", head("पेज नहीं मिला | KahaniSuno", "यह पेज उपलब्ध नहीं है।", "/404.html") + '<h1>पेज नहीं मिला</h1><p>यह पेज मौजूद नहीं है। <a href="/">होम पेज पर जाएँ</a> और कोई कहानी सुनें।</p>' + foot())

urls = ["/", "/about.html", "/privacy.html", "/contact.html"] + [f"/category/{c}.html" for c in CATS] + [f"/kahani/{s['slug']}.html" for s in STORIES]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
items = "".join(f'<item><title>{e(s["title"])}</title><link>{SITE}/kahani/{s["slug"]}.html</link><guid>{SITE}/kahani/{s["slug"]}.html</guid><description>{e(s["hook"])}</description></item>' for s in STORIES)
write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{NAME}</title><link>{SITE}</link><description>हिंदी ऑडियो कहानियाँ</description><language>hi</language>{items}</channel></rss>')

# YouTube / Shorts kit
kit = [f"# YouTube & Shorts kit ({TODAY})\n", "Upload each episode with these. Replace links after you publish.\n"]
for s in STORIES:
    hook = " ".join(s["paragraphs"][:2])
    tags = "#hindikahani #hindistory #audiostory #" + ("horrorstories #bhoot" if s["category"] == "horror" else "mystery #rahasya" if s["category"] == "rahasya" else "bedtimestory #nindiakahani")
    kit.append(f"""## {s['title']}
**Title:** {s['hinglish']} | {s['title']}
**Description:**
{s['hook']}
पूरी कहानी का पाठ पढ़ें: {SITE}/kahani/{s['slug']}.html
नई कहानियों के लिए चैनल सब्सक्राइब करें।
(यह कहानी AI की मदद से बनाई गई है।)
{tags}
**Shorts hook (first 30 sec):** {hook}
**Pinned comment:** अगला भाग चाहिए? कमेंट में बताइए, और बताइए आपको कैसी लगी।
""")
open(os.path.join(HERE, "youtube_kit.md"), "w", encoding="utf-8").write("\n".join(kit))

zp = os.path.join(HERE, "kahanisuno-upload-me.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in os.walk(OUT):
        for f in fs:
            full = os.path.join(d, f); z.write(full, os.path.relpath(full, OUT))
print("built", len(urls), "pages ->", OUT, "| zip:", zp)
