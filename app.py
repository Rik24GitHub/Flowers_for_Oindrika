import json
import random
import uuid
from datetime import date, datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────
#  EDIT THESE FEW LINES TO MAKE IT YOURS
# ─────────────────────────────────────────────────────────────
HER_NAME = "Oindrika"
FULL_NAME = "Oindrika Roy"
HIS_NAME = "Rik"
START_DATE = date(2026, 3, 5)  # <- change to the day your story began

MEM_DIR = Path("memories")
MEM_INDEX = MEM_DIR / "index.json"
MEM_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title=f"For {HER_NAME}",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL STYLE
# ─────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Pinyon+Script&family=Jost:wght@300;400;500&display=swap');

:root{
  --night:#12060f; --plum:#2a0f27; --wine:#4a1632;
  --rose:#ff7a9c; --blush:#ffd3de; --gold:#e8c27a; --ivory:#fff4f0;
}
header, #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{display:none !important; visibility:hidden;}
.stApp{
  background:
    radial-gradient(1200px 600px at 15% -10%, #5a1c3d 0%, transparent 60%),
    radial-gradient(900px 600px at 100% 10%, #3a1240 0%, transparent 55%),
    linear-gradient(180deg, #12060f 0%, #1d0a1b 55%, #12060f 100%);
  color:var(--ivory);
  font-family:'Jost', sans-serif;
}
.block-container{max-width:860px; padding-top:1.2rem; padding-bottom:5rem;}
p, li, label, span, div{font-family:'Jost', sans-serif;}
.stApp p, .stApp label{color:#f6dfe5;}

iframe[title="streamlit_components_v1.html"], .stCustomComponentV1{
  border-radius:28px; border:1px solid rgba(255,211,222,.14);
  box-shadow:0 30px 80px rgba(0,0,0,.55), 0 0 0 1px rgba(232,194,122,.08) inset;
}

.section-title{
  font-family:'Cormorant Garamond', serif; font-weight:500; font-style:italic;
  font-size:2.3rem; line-height:1.15; color:var(--blush);
  margin:3.2rem 0 .3rem 0; letter-spacing:.2px;
}
.section-sub{color:#cfa9b6; font-weight:300; margin:0 0 1.4rem 0; font-size:1.02rem;}

.letter{
  position:relative;
  background:linear-gradient(160deg, rgba(255,244,240,.07), rgba(255,211,222,.04));
  border:1px solid rgba(255,211,222,.16);
  border-radius:26px; padding:2.6rem 2.4rem 2.2rem 2.4rem;
  box-shadow:0 24px 60px rgba(0,0,0,.35);
  backdrop-filter:blur(6px);
}
.letter .dear{font-family:'Pinyon Script', cursive; font-size:2.6rem; color:var(--gold); margin-bottom:.8rem;}
.letter p{
  font-family:'Cormorant Garamond', serif; font-size:1.34rem; line-height:1.75;
  color:#fbe9ee !important; margin:0 0 1.05rem 0; max-width:62ch;
}
.letter .sign{font-family:'Pinyon Script', cursive; font-size:2.3rem; color:var(--blush) !important; margin-top:1.4rem;}
.letter .days{font-style:italic; color:#e9bfcb !important;}

.note-card{
  background:rgba(255,244,240,.05); border:1px solid rgba(255,211,222,.14);
  border-radius:22px; padding:1.8rem 1.9rem;
}
.note-card p{
  font-family:'Cormorant Garamond', serif; font-size:1.3rem; line-height:1.7;
  color:#fbe9ee !important; margin:0;
}

.reason{
  font-family:'Cormorant Garamond', serif; font-style:italic; font-size:1.7rem;
  line-height:1.5; color:#fff4f0; text-align:center;
  padding:2rem 1.4rem; margin-top:1rem;
  border-top:1px solid rgba(232,194,122,.35); border-bottom:1px solid rgba(232,194,122,.35);
}

/* Buttons */
.stButton > button, .stDownloadButton > button{
  background:linear-gradient(135deg,#ff7a9c,#e0457b); color:#fff; border:0;
  border-radius:999px; padding:.7rem 1.7rem; font-weight:500; letter-spacing:.3px;
  box-shadow:0 10px 30px rgba(224,69,123,.35); transition:transform .2s ease, box-shadow .2s ease;
}
.stButton > button:hover{transform:translateY(-2px); box-shadow:0 16px 40px rgba(224,69,123,.5); color:#fff; border:0;}
.stButton > button:focus-visible{outline:2px solid var(--gold); outline-offset:3px;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{gap:.4rem; border-bottom:1px solid rgba(255,211,222,.15);}
.stTabs [data-baseweb="tab"]{color:#cfa9b6; font-weight:400; padding:.7rem 1rem;}
.stTabs [aria-selected="true"]{color:var(--blush) !important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--rose) !important;}

/* Inputs & uploader */
[data-testid="stFileUploaderDropzone"]{
  background:rgba(255,244,240,.05); border:1.5px dashed rgba(255,211,222,.35); border-radius:20px;
}
[data-testid="stFileUploaderDropzone"] *{color:#f6dfe5 !important;}
[data-testid="stFileUploaderDropzone"] button{
  background:rgba(255,211,222,.12) !important; border:1px solid rgba(255,211,222,.3) !important; border-radius:999px !important;
}
.stTextInput input, .stTextArea textarea{
  background:rgba(255,244,240,.06) !important; color:#fff4f0 !important;
  border:1px solid rgba(255,211,222,.22) !important; border-radius:14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus{border-color:var(--rose) !important; box-shadow:0 0 0 1px var(--rose) !important;}

.gate{text-align:center; margin-top:14vh;}
.gate .g-name{font-family:'Pinyon Script', cursive; font-size:4.2rem; color:var(--blush); line-height:1.1;}
.gate .g-sub{font-family:'Cormorant Garamond', serif; font-style:italic; font-size:1.4rem; color:#e9bfcb; margin:.4rem 0 1.6rem 0;}

.polaroid-cap{font-family:'Cormorant Garamond', serif; font-style:italic; font-size:1.1rem; color:#f6dfe5; margin:.35rem 0 1.1rem 0;}
.foot{
  text-align:center; margin-top:4.5rem; padding-top:2rem; border-top:1px solid rgba(255,211,222,.12);
  font-family:'Cormorant Garamond', serif; font-style:italic; font-size:1.35rem; color:#e9bfcb;
}
.foot b{font-family:'Pinyon Script', cursive; font-weight:400; font-size:2.2rem; color:var(--gold); display:block; margin-top:.3rem;}

@media (max-width:640px){
  .letter{padding:1.8rem 1.4rem;}
  .letter p{font-size:1.22rem;}
  .section-title{font-size:1.9rem;}
}
@media (prefers-reduced-motion: reduce){ *{transition:none !important;} }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  OPTIONAL PASSWORD GATE (set SITE_PASSWORD in Streamlit secrets)
#  A deployed Streamlit link can be opened by anyone who has it,
#  so this keeps your memories and words only for her.
# ─────────────────────────────────────────────────────────────
def _site_password():
    try:
        return st.secrets.get("SITE_PASSWORD")
    except Exception:
        return None


def gate():
    pw = _site_password()
    if not pw or st.session_state.get("unlocked"):
        return
    st.markdown(
        f"""
        <div class="gate">
          <div class="g-name">{HER_NAME}</div>
          <div class="g-sub">This one is only for you. What's our secret word?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        attempt = st.text_input("Secret word", type="password", label_visibility="collapsed",
                                placeholder="Our secret word")
        if st.button("Open", use_container_width=True):
            if attempt.strip().lower() == str(pw).strip().lower():
                st.session_state["unlocked"] = True
                st.rerun()
            else:
                st.error("Not quite. Think of the first thing that made us laugh.")
    st.stop()


gate()

# ─────────────────────────────────────────────────────────────
#  HERO: animated garden of flowers, falling petals, her name
# ─────────────────────────────────────────────────────────────
HERO_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,400;1,500&family=Pinyon+Script&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{height:100%;background:transparent;overflow:hidden;}
  .stage{
    position:relative; width:100%; height:100vh; overflow:hidden;
    background:
      radial-gradient(700px 420px at 50% 78%, rgba(255,122,156,.28), transparent 70%),
      radial-gradient(600px 400px at 85% 10%, rgba(120,60,150,.35), transparent 65%),
      linear-gradient(180deg,#14061a 0%, #2a0f2a 55%, #4a1632 100%);
  }
  .star{position:absolute; width:2px; height:2px; border-radius:50%; background:#fff6e0; opacity:.0;
        animation:tw 4s ease-in-out infinite;}
  @keyframes tw{0%,100%{opacity:.05} 50%{opacity:.85}}

  .moon{
    position:absolute; top:7%; right:9%; width:64px; height:64px; border-radius:50%;
    background:radial-gradient(circle at 35% 35%, #fffaf0, #f3dcb0 60%, #d9b878);
    box-shadow:0 0 60px 18px rgba(243,220,176,.25);
    opacity:0; animation:fade 3s ease 0.3s forwards;
  }
  @keyframes fade{to{opacity:.95}}

  .words{position:absolute; top:6%; left:0; right:0; text-align:center; padding:0 20px; z-index:3;}
  .for{font-family:'Cormorant Garamond',serif; font-style:italic; font-size:clamp(16px,2.4vw,22px);
       color:#e9bfcb; opacity:0; animation:rise 1.6s ease .6s forwards;}
  .name{
    font-family:'Pinyon Script',cursive; line-height:1.05;
    font-size:clamp(64px,15vw,128px);
    background:linear-gradient(100deg,#ffe1e8 0%,#ffb3c6 40%,#e8c27a 100%);
    -webkit-background-clip:text; background-clip:text; color:transparent;
    filter:drop-shadow(0 6px 30px rgba(255,122,156,.35));
    opacity:0; animation:rise 2.2s ease 1s forwards;
  }
  .line{
    font-family:'Cormorant Garamond',serif; font-style:italic;
    font-size:clamp(18px,3.1vw,27px); color:#fff0f3; margin-top:10px; min-height:1.6em;
    text-shadow:0 2px 18px rgba(0,0,0,.5);
  }
  .caret{display:inline-block; width:2px; height:1em; background:#ffd3de; margin-left:3px; vertical-align:-2px; animation:blink 1s steps(1) infinite;}
  @keyframes blink{50%{opacity:0}}
  @keyframes rise{from{opacity:0; transform:translateY(14px)} to{opacity:1; transform:none}}

  svg{position:absolute; left:0; bottom:0; width:100%; height:62%; z-index:2;}
  canvas{position:absolute; inset:0; width:100%; height:100%; z-index:4; pointer-events:none;}

  .stem{fill:none; stroke:url(#stemG); stroke-width:4; stroke-linecap:round;
        stroke-dasharray:var(--len); stroke-dashoffset:var(--len);
        animation:grow 1.7s cubic-bezier(.4,.1,.2,1) forwards;}
  @keyframes grow{to{stroke-dashoffset:0}}
  .pop{transform:scale(0); animation:pop 1.6s cubic-bezier(.2,.9,.25,1.15) forwards;}
  @keyframes pop{from{transform:scale(0) rotate(-25deg)} to{transform:scale(1) rotate(0)}}
  .breathe{animation:breathe 6s ease-in-out infinite; transform-origin:0 0;}
  @keyframes breathe{0%,100%{transform:scale(1) rotate(0)} 50%{transform:scale(1.045) rotate(1.5deg)}}

  @media (prefers-reduced-motion: reduce){
    .stem{animation:none; stroke-dashoffset:0}
    .pop{animation:none; transform:none}
    .breathe,.star{animation:none}
  }
</style>
</head>
<body>
<div class="stage" id="stage">
  <div class="moon"></div>
  <div class="words">
    <div class="for">for my love</div>
    <div class="name">__NAME__</div>
    <div class="line"><span id="typed"></span><span class="caret"></span></div>
  </div>

  <svg id="garden" viewBox="0 0 1000 480" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs>
      <linearGradient id="stemG" x1="0" y1="1" x2="0" y2="0">
        <stop offset="0" stop-color="#1f5a45"/><stop offset="1" stop-color="#7fc29a"/>
      </linearGradient>
      <linearGradient id="leafG" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0" stop-color="#1c4f3d"/><stop offset="1" stop-color="#6fb890"/>
      </linearGradient>
      <radialGradient id="core" cx="50%" cy="50%" r="50%">
        <stop offset="0" stop-color="#fff2b8"/><stop offset="1" stop-color="#e8b04a"/>
      </radialGradient>
    </defs>
    <g id="layer"></g>
  </svg>
  <canvas id="petals"></canvas>
</div>

<script>
(function(){
  const NS = "http://www.w3.org/2000/svg";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const stage = document.getElementById("stage");

  /* stars */
  for(let i=0;i<70;i++){
    const s=document.createElement("div"); s.className="star";
    s.style.left=Math.random()*100+"%"; s.style.top=Math.random()*55+"%";
    s.style.animationDelay=(Math.random()*4)+"s";
    s.style.width=s.style.height=(1+Math.random()*2)+"px";
    stage.appendChild(s);
  }

  /* flowers */
  const flowers = [
    {x:500,y:140,r:62,a:"#ffd6e0",b:"#ff4f87",n:10},
    {x:355,y:205,r:48,a:"#fff3f5",b:"#ff9db8",n:8},
    {x:645,y:200,r:50,a:"#ffe6c9",b:"#ff8f6b",n:8},
    {x:232,y:280,r:42,a:"#ffdcee",b:"#e45ca3",n:7},
    {x:768,y:285,r:42,a:"#fff5d2",b:"#f4b942",n:7},
    {x:122,y:350,r:33,a:"#ffe3ea",b:"#ff7d9c",n:7},
    {x:880,y:352,r:33,a:"#ffeaf3",b:"#ff6fa5",n:7},
    {x:428,y:305,r:35,a:"#ffffff",b:"#ffb3c6",n:6},
    {x:574,y:308,r:35,a:"#ffe9ef",b:"#ff5d8f",n:6}
  ];

  const layer = document.getElementById("layer");
  const defs = document.querySelector("#garden defs");
  const el=(t,attrs,parent)=>{const e=document.createElementNS(NS,t);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;};

  flowers.forEach((f,i)=>{
    const g = el("linearGradient",{id:"pg"+i,x1:0,y1:1,x2:0,y2:0},defs);
    el("stop",{offset:0,"stop-color":f.b},g); el("stop",{offset:1,"stop-color":f.a},g);
    const g2 = el("linearGradient",{id:"pi"+i,x1:0,y1:1,x2:0,y2:0},defs);
    el("stop",{offset:0,"stop-color":f.a},g2); el("stop",{offset:1,"stop-color":"#ffffff"},g2);

    const sway = (i%2?1:-1)*(18+Math.random()*22);
    const d = `M ${f.x+sway*.4} 480 C ${f.x+sway} ${480-(480-f.y)*.35}, ${f.x-sway} ${480-(480-f.y)*.7}, ${f.x} ${f.y}`;
    const stemDelay = i*0.32;
    const stem = el("path",{d:d,class:"stem"},layer);
    const len = stem.getTotalLength();
    stem.style.setProperty("--len",len);
    stem.style.animationDelay = stemDelay+"s";

    [0.45,0.68].forEach((t,k)=>{
      const p = stem.getPointAtLength(len*t);
      const side = (k+i)%2 ? 1 : -1;
      const lg = el("g",{transform:`translate(${p.x} ${p.y}) rotate(${side*58})`},layer);
      const leaf = el("g",{class:"pop",style:`animation-delay:${stemDelay+1+k*.25}s`},lg);
      el("path",{d:"M0 0 C 14 -12, 16 -34, 0 -50 C -16 -34, -14 -12, 0 0 Z",fill:"url(#leafG)",opacity:.95,transform:`scale(${f.r/48})`},leaf);
    });

    const pos = el("g",{transform:`translate(${f.x} ${f.y})`},layer);
    const bloom = el("g",{class:"pop",style:`animation-delay:${stemDelay+1.5}s`},pos);
    const sway2 = el("g",{class:"breathe",style:`animation-delay:${stemDelay+3.2}s`},bloom);

    el("circle",{r:f.r*1.45,fill:f.b,opacity:.16},sway2);
    for(let k=0;k<f.n;k++){
      el("ellipse",{cx:0,cy:-f.r*.62,rx:f.r*.34,ry:f.r*.64,fill:`url(#pg${i})`,opacity:.96,
        transform:`rotate(${k*360/f.n})`},sway2);
    }
    for(let k=0;k<f.n;k++){
      el("ellipse",{cx:0,cy:-f.r*.38,rx:f.r*.22,ry:f.r*.42,fill:`url(#pi${i})`,opacity:.92,
        transform:`rotate(${k*360/f.n + 180/f.n})`},sway2);
    }
    el("circle",{r:f.r*.17,fill:"url(#core)"},sway2);
    for(let k=0;k<9;k++){
      const a=Math.random()*6.283, rr=Math.random()*f.r*.12;
      el("circle",{cx:Math.cos(a)*rr,cy:Math.sin(a)*rr,r:f.r*.025,fill:"#b8741c",opacity:.7},sway2);
    }
  });

  /* typed lines */
  const lines = [
    "Whatever today felt like, I am right here.",
    "I love you more than these flowers could ever say.",
    "I am always with you, even when I am far.",
    "You are my favourite person in every world.",
    "Breathe. You are loved. You are so loved."
  ];
  const out = document.getElementById("typed");
  let li=0, ci=0, del=false;
  function tick(){
    const full = lines[li];
    if(reduce){ out.textContent = full; li=(li+1)%lines.length; setTimeout(tick,4200); return; }
    if(!del){
      ci++; out.textContent = full.slice(0,ci);
      if(ci===full.length){ del=true; return setTimeout(tick,2600); }
      setTimeout(tick,52);
    } else {
      ci-=2; out.textContent = full.slice(0,Math.max(ci,0));
      if(ci<=0){ del=false; li=(li+1)%lines.length; return setTimeout(tick,500); }
      setTimeout(tick,22);
    }
  }
  setTimeout(tick,3200);

  /* falling petals */
  if(!reduce){
    const cv=document.getElementById("petals"), ctx=cv.getContext("2d");
    let W,H,dpr=Math.min(window.devicePixelRatio||1,2);
    function size(){W=stage.clientWidth;H=stage.clientHeight;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);}
    size(); window.addEventListener("resize",size);
    const cols=["#ffc2d1","#ff8fb0","#ffe1e8","#ffb3c6","#f7d58f"];
    const P=Array.from({length:34},()=>mk(true));
    function mk(init){
      return {x:Math.random()*W,y:init?Math.random()*H:-20,s:5+Math.random()*8,vy:.35+Math.random()*.8,
        vx:(Math.random()-.5)*.5,rot:Math.random()*6.28,vr:(Math.random()-.5)*.03,
        ph:Math.random()*6.28,c:cols[Math.floor(Math.random()*cols.length)],o:.45+Math.random()*.45};
    }
    (function loop(t){
      ctx.clearRect(0,0,W,H);
      P.forEach((p,i)=>{
        p.y+=p.vy; p.x+=p.vx+Math.sin(t/1400+p.ph)*.45; p.rot+=p.vr;
        if(p.y>H+20||p.x<-30||p.x>W+30){P[i]=mk(false);return;}
        ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot);
        ctx.globalAlpha=p.o; ctx.fillStyle=p.c;
        ctx.beginPath(); ctx.ellipse(0,0,p.s*.55,p.s,0,0,6.283); ctx.fill();
        ctx.restore();
      });
      requestAnimationFrame(loop);
    })(0);
  }
})();
</script>
</body>
</html>
"""

components.html(HERO_HTML.replace("__NAME__", HER_NAME), height=720, scrolling=False)

# ─────────────────────────────────────────────────────────────
#  LOVE LETTER
# ─────────────────────────────────────────────────────────────
days_together = (date.today() - START_DATE).days
days_line = ""
if days_together > 0:
    days_line = (f'<p class="days">It has been {days_together:,} days since our story began, '
                 f"and I would choose every single one of them again.</p>")

st.markdown(
    f"""
    <div class="section-title">A letter, just for you</div>
    <div class="section-sub">Read it slowly. Read it again whenever you need to.</div>
    <div class="letter">
      <div class="dear">My dearest {HER_NAME},</div>
      {days_line}
      <p>I wanted to give you something that you could open on any day, a good one or a heavy one,
      and feel held the moment it loads. So I made you a little garden that blooms every time you arrive.</p>
      <p>I love you. Not in a loud way that fades, but in a quiet, steady way that settles into
      the ordinary parts of my day. I love your laugh, the way you care about people, the way you
      keep going even when you are tired. You are softer and stronger than you think.</p>
      <p>On the days you feel low, I need you to remember this: you are not too much, you are not
      behind, and you are never alone. I am with you in the good days and in the hard ones, in
      every distance and every silence. Whatever you are carrying, we carry it together.</p>
      <p>If nothing else, let these flowers say what I sometimes cannot: you are deeply, completely
      loved.</p>
      <div class="sign">Always yours, {HIS_NAME}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
#  OPEN WHEN...
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Open when…</div>'
    '<div class="section-sub">Pick the one that fits how you feel right now.</div>',
    unsafe_allow_html=True,
)

OPEN_WHEN = {
    "You feel sad": (
        "Come here. Take a slow breath in, and let it out. Whatever happened today does not get to "
        "decide who you are. You are allowed to feel this, and you are allowed to rest. I am proud of you "
        "for getting through it, and I am right here, holding on until the heaviness passes."
    ),
    "You miss me": (
        "I miss you too, in the quiet moments and the loud ones. Close your eyes and picture me beside you, "
        "because that is exactly where my heart is. Distance only changes the address, never the feeling. "
        "I will see you soon, and I will hold you tight."
    ),
    "You doubt yourself": (
        "Listen to me, because I see you clearly: you are talented, kind and brave, and you have already "
        "come further than you give yourself credit for. The voice that says you are not enough is wrong. "
        "I have never once doubted you, and I never will."
    ),
    "You cannot sleep": (
        "Put the phone down after this and let your shoulders drop. You did enough today. "
        "Tomorrow can wait for tomorrow. Imagine me saying goodnight, forehead against yours, "
        "and let the whole world go quiet. Sleep well, my love."
    ),
    "You are happy": (
        "Then I am happy too, completely. Keep this feeling, spin around once, and smile that smile of yours. "
        "You deserve every good thing that is coming. Call me, I want to celebrate with you."
    ),
}

tabs = st.tabs(list(OPEN_WHEN.keys()))
for tab, (_, msg) in zip(tabs, OPEN_WHEN.items()):
    with tab:
        st.markdown(f'<div class="note-card"><p>{msg}</p></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  REASONS I LOVE YOU
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">A reason I love you</div>'
    '<div class="section-sub">There are too many to count, so here is one at a time.</div>',
    unsafe_allow_html=True,
)

REASONS = [
    "Because you make ordinary days feel like something worth remembering.",
    "Because of how gently you care for the people you love.",
    "Because your smile can rearrange my whole mood.",
    "Because you keep trying, even on the days it is hard.",
    "Because home, for me, started to feel like you.",
    "Because you are real, warm, and wonderfully yourself.",
    "Because I am a better person when I am with you.",
    "Because your laugh is my favourite sound.",
    "Because you believe in me even when I forget to.",
    "Because loving you has never felt like effort, only like coming home.",
    "Because you are beautiful in the way that matters most, from the inside.",
    "Because with you, the future looks like something to look forward to.",
]

if "reason" not in st.session_state:
    st.session_state.reason = REASONS[0]

if st.button("Tell me another reason", key="reason_btn"):
    choices = [r for r in REASONS if r != st.session_state.reason]
    st.session_state.reason = random.choice(choices)

st.markdown(f'<div class="reason">{st.session_state.reason}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  OUR MEMORIES (UPLOAD + GALLERY)
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Our little album</div>'
    '<div class="section-sub">Add a photo of us, a place we loved, or a moment we never want to lose.</div>',
    unsafe_allow_html=True,
)


def load_index():
    if MEM_INDEX.exists():
        try:
            return json.loads(MEM_INDEX.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_index(items):
    MEM_INDEX.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


if "up_key" not in st.session_state:
    st.session_state.up_key = 0

files = st.file_uploader(
    "Add memories",
    type=["png", "jpg", "jpeg", "webp", "gif"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    key=f"uploader_{st.session_state.up_key}",
)
caption = st.text_input(
    "Caption",
    placeholder="What do you remember about this moment?",
    label_visibility="collapsed",
    key=f"caption_{st.session_state.up_key}",
)

if st.button("Save to our album", key="save_mem"):
    if not files:
        st.warning("Choose at least one photo first.")
    else:
        items = load_index()
        for f in files:
            ext = Path(f.name).suffix.lower() or ".jpg"
            fname = f"{uuid.uuid4().hex}{ext}"
            (MEM_DIR / fname).write_bytes(f.getbuffer())
            items.append({
                "file": fname,
                "caption": caption.strip(),
                "added": datetime.now().strftime("%d %b %Y"),
            })
        save_index(items)
        st.session_state.up_key += 1
        st.success("Saved. Another memory, safe with us. 💗")
        st.rerun()

items = load_index()
items = [i for i in items if (MEM_DIR / i["file"]).exists()]

if items:
    cols = st.columns(2)
    for idx, item in enumerate(reversed(items)):
        with cols[idx % 2]:
            st.image(str(MEM_DIR / item["file"]), use_container_width=True)
            cap = item["caption"] or "A moment with you"
            st.markdown(
                f'<div class="polaroid-cap">{cap}<br><span style="color:#b98a99;font-size:.95rem;">{item["added"]}</span></div>',
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        '<div class="note-card"><p>Our album is waiting for its first picture. '
        "Add one above and let it be the start of many.</p></div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="foot">
      Whenever you feel low, come back here. The flowers will always bloom for you.
      <b>Forever yours, {HIS_NAME}</b>
    </div>
    """,
    unsafe_allow_html=True,
)
