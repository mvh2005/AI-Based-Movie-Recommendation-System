"""
app.py — CineMatch Ultra — Streamlit Movie Recommendation Web App

Run with:
    streamlit run app.py
"""

import streamlit as st
import pickle
import pandas as pd
import os
import random

# ── Page config (must be first Streamlit command) ─────────────
st.set_page_config(
    page_title="CineMatch — AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# ULTRA CINEMATIC THEME — Full CSS & Animation Overhaul
# ══════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');

/* ─── CSS Variables ─────────────────────────────────── */
:root {
    --gold:      #FFD700;
    --red:       #e94560;
    --neon:      #00d4ff;
    --purple:    #7c3aed;
    --green:     #10b981;
    --orange:    #f59e0b;
    --pink:      #ec4899;
    --bg-deep:   #03030a;
    --bg-mid:    #08081a;
    --bg-card:   #0d1020;
    --border:    rgba(255,255,255,0.07);
    --text:      #e8eaf0;
    --muted:     #5a6380;
    --shine:     linear-gradient(135deg,#FFD700 0%,#ff6b35 50%,#e94560 100%);
}

/* ─── Global Reset ──────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}

.stApp {
    background:var(--bg-deep)!important;
    color:var(--text)!important;
    font-family:'Inter',sans-serif;
    overflow-x:hidden;
}

.block-container {
    padding-top:0!important;
    padding-bottom:3rem!important;
    max-width:1380px!important;
}

/* ─── Deep Cinematic Background ─────────────────────── */
.stApp::before {
    content:'';
    position:fixed;
    inset:0;
    background:
        radial-gradient(ellipse 90% 50% at 50% -5%,  rgba(233,69,96,0.22)  0%,transparent 65%),
        radial-gradient(ellipse 70% 40% at 10% 110%, rgba(124,58,237,0.16) 0%,transparent 55%),
        radial-gradient(ellipse 50% 30% at 90% 85%,  rgba(0,212,255,0.10)  0%,transparent 55%);
    pointer-events:none;
    z-index:0;
}

/* Perspective Grid Floor */
.stApp::after {
    content:'';
    position:fixed;
    bottom:0;left:-50%;
    width:200%;height:50vh;
    background:
        linear-gradient(rgba(0,212,255,0.04) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,212,255,0.04) 1px,transparent 1px);
    background-size:70px 70px;
    transform:perspective(700px) rotateX(72deg);
    transform-origin:center bottom;
    pointer-events:none;
    z-index:0;
    mask-image:linear-gradient(to top,rgba(0,0,0,0.6) 0%,transparent 65%);
    -webkit-mask-image:linear-gradient(to top,rgba(0,0,0,0.6) 0%,transparent 65%);
    animation:grid-drift 20s linear infinite;
}
@keyframes grid-drift {
    0%  {background-position:0 0,0 0;}
    100%{background-position:0 70px,0 0;}
}

/* ─── Film Strip ─────────────────────────────────────── */
.filmstrip-header {
    width:100%;
    background:linear-gradient(180deg,#1a1a1a,#111);
    border-bottom:3px solid #1e1e1e;
    padding:6px 0;
    display:flex;overflow:hidden;
    position:relative;z-index:10;
}
.filmstrip-holes {
    display:flex;align-items:center;gap:22px;
    animation:filmroll 14s linear infinite;
    white-space:nowrap;padding:0 10px;
}
@keyframes filmroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}
.film-hole {
    width:18px;height:14px;border-radius:3px;
    background:#030308;border:2px solid #2a2a2a;flex-shrink:0;
}
.film-title-cell {
    font-family:'Bebas Neue',sans-serif;font-size:10px;
    color:var(--gold);letter-spacing:4px;padding:0 28px;opacity:0.7;flex-shrink:0;
}

/* ─── Hero ───────────────────────────────────────────── */
.hero-wrap {
    text-align:center;padding:4rem 1rem 2.5rem;
    position:relative;z-index:2;
}
.hero-badge {
    display:inline-flex;align-items:center;gap:8px;
    background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);
    border-radius:50px;padding:6px 18px;font-size:0.75rem;font-weight:600;
    color:var(--neon);letter-spacing:2.5px;text-transform:uppercase;
    margin-bottom:1.4rem;animation:badge-glow 3s ease-in-out infinite;
}
@keyframes badge-glow {
    0%,100%{box-shadow:0 0 12px rgba(0,212,255,0.15);}
    50%    {box-shadow:0 0 25px rgba(0,212,255,0.35);}
}
.hero-title {
    font-family:'Bebas Neue',sans-serif;
    font-size:clamp(5rem,13vw,11rem);line-height:0.88;
    display:inline-block;
    background:linear-gradient(160deg,#fff 0%,#FFD700 30%,#ff6b35 65%,#e94560 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    filter:drop-shadow(0 0 40px rgba(233,69,96,0.25));
    animation:title-breathe 4s ease-in-out infinite;
}
@keyframes title-breathe {
    0%,100%{filter:drop-shadow(0 0 30px rgba(233,69,96,0.2));}
    50%    {filter:drop-shadow(0 0 60px rgba(233,69,96,0.4));}
}
.hero-tagline {
    font-size:1.05rem;font-weight:300;color:#6b7592;
    letter-spacing:3px;text-transform:uppercase;margin-top:1rem;
}
.hero-tagline strong{color:var(--neon);font-weight:500;}
.hero-line {
    width:320px;height:1.5px;margin:1.4rem auto 0;
    background:linear-gradient(90deg,transparent,var(--neon) 20%,var(--gold) 50%,var(--red) 80%,transparent);
    border-radius:2px;animation:line-sweep 3s ease-in-out infinite;
}
@keyframes line-sweep{
    0%,100%{opacity:0.7;width:280px;}
    50%    {opacity:1;width:380px;box-shadow:0 0 20px var(--neon);}
}

/* ─── Stats Row ──────────────────────────────────────── */
.stats-row {
    display:grid;grid-template-columns:repeat(4,1fr);
    gap:1rem;margin:2.5rem 0 2rem;position:relative;z-index:2;
}
.stat-card {
    background:linear-gradient(145deg,rgba(15,15,35,0.9),rgba(8,8,20,0.95));
    border:1px solid rgba(255,255,255,0.06);border-radius:20px;
    padding:1.5rem 1rem;text-align:center;position:relative;overflow:hidden;
    transition:transform 0.35s cubic-bezier(.23,1,.32,1),box-shadow 0.35s ease;
    cursor:default;
}
.stat-card::before {
    content:'';position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--border-color,rgba(255,215,0,0.5)),transparent);
}
.stat-card:hover {
    transform:translateY(-6px) scale(1.02);
    box-shadow:0 25px 50px rgba(0,0,0,0.45),0 0 25px var(--glow-color,rgba(255,215,0,0.1));
}
.stat-card .s-icon{font-size:1.8rem;margin-bottom:0.5rem;display:block;}
.stat-card .s-val {
    font-family:'Bebas Neue',sans-serif;font-size:2.8rem;line-height:1;
    background:var(--val-gradient,var(--shine));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    letter-spacing:1px;
}
.stat-card .s-lbl {
    font-size:0.68rem;font-weight:600;color:var(--muted);
    letter-spacing:2.5px;text-transform:uppercase;margin-top:0.3rem;
}

/* ─── Neon Divider ───────────────────────────────────── */
.neon-divider {
    height:1px;margin:1.5rem 0;
    background:linear-gradient(90deg,transparent,rgba(233,69,96,0.5) 25%,rgba(255,215,0,0.6) 50%,rgba(0,212,255,0.5) 75%,transparent);
    box-shadow:0 0 10px rgba(233,69,96,0.2);position:relative;z-index:2;
}

/* ─── Tabs ───────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background:rgba(0,0,0,0.5)!important;
    border:1px solid rgba(255,255,255,0.06)!important;
    border-radius:16px!important;padding:5px!important;gap:3px!important;
    backdrop-filter:blur(20px)!important;position:relative;z-index:2;
}
.stTabs [data-baseweb="tab"] {
    border-radius:12px!important;color:var(--muted)!important;
    font-weight:600!important;font-size:0.85rem!important;letter-spacing:0.3px!important;
    padding:10px 24px!important;transition:all 0.25s ease!important;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--gold)!important;background:rgba(255,215,0,0.05)!important;}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#e94560 0%,#7c3aed 100%)!important;
    color:#fff!important;
    box-shadow:0 4px 20px rgba(233,69,96,0.45),inset 0 1px 0 rgba(255,255,255,0.15)!important;
}

/* ─── Section Header ─────────────────────────────────── */
.sec-header {
    display:flex;align-items:center;gap:14px;
    margin:2rem 0 1.4rem;position:relative;z-index:2;
}
.sec-header-icon{font-size:1.6rem;filter:drop-shadow(0 0 8px currentColor);}
.sec-header-text{font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;color:#fff;line-height:1;}
.sec-header-line{flex:1;height:1px;background:linear-gradient(90deg,rgba(255,215,0,0.3),transparent);}

/* ─── Mood Grid ──────────────────────────────────────── */
.mood-grid {
    display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));
    gap:0.9rem;margin:1rem 0 1.5rem;position:relative;z-index:2;
}
.mood-btn {
    background:linear-gradient(145deg,rgba(15,15,30,0.8),rgba(5,5,15,0.9));
    border:1px solid rgba(255,255,255,0.07);border-radius:16px;
    padding:1.1rem 0.7rem;text-align:center;cursor:pointer;
    transition:all 0.3s cubic-bezier(.23,1,.32,1);position:relative;overflow:hidden;
}
.mood-btn::before {
    content:'';position:absolute;inset:0;background:var(--mood-color);
    opacity:0;transition:opacity 0.3s ease;border-radius:16px;
}
.mood-btn:hover::before{opacity:0.12;}
.mood-btn:hover{transform:translateY(-4px) scale(1.04);border-color:var(--mood-border);box-shadow:0 12px 30px rgba(0,0,0,0.4),0 0 20px var(--mood-glow);}
.mood-icon{font-size:2rem;display:block;margin-bottom:0.5rem;}
.mood-label{font-size:0.72rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--mood-text,#9aa0b4);}

/* ─── Genre Grid ─────────────────────────────────────── */
.genre-grid {
    display:flex;flex-wrap:wrap;gap:0.6rem;
    margin:1rem 0 1.5rem;position:relative;z-index:2;
}
.genre-pill {
    padding:8px 18px;border-radius:50px;border:1px solid rgba(255,255,255,0.08);
    background:rgba(255,255,255,0.03);font-size:0.8rem;font-weight:600;
    letter-spacing:0.5px;color:#8892b0;cursor:pointer;transition:all 0.25s ease;
    position:relative;overflow:hidden;
}
.genre-pill::before {
    content:'';position:absolute;inset:0;
    background:var(--genre-color,linear-gradient(135deg,var(--red),var(--purple)));
    opacity:0;transition:opacity 0.25s ease;
}
.genre-pill:hover::before{opacity:1;}
.genre-pill:hover{color:#fff;border-color:transparent;transform:scale(1.05);}
.genre-pill span{position:relative;z-index:1;}

/* ─── Ultra Movie Card ───────────────────────────────── */
.movie-card-ultra {
    background:linear-gradient(160deg,rgba(16,16,35,0.98),rgba(8,8,18,0.99));
    border:1px solid rgba(255,255,255,0.055);border-radius:22px;overflow:hidden;
    position:relative;transition:transform 0.4s cubic-bezier(.23,1,.32,1),box-shadow 0.4s ease,border-color 0.3s ease;
    margin-bottom:1.2rem;z-index:2;
}
.movie-card-ultra:hover{
    transform:translateY(-8px) scale(1.015);border-color:rgba(233,69,96,0.35);
    box-shadow:0 25px 60px rgba(0,0,0,0.6),0 0 35px rgba(233,69,96,0.12),inset 0 1px 0 rgba(255,255,255,0.08);
}
.movie-card-ultra::after {
    content:'';position:absolute;top:-50%;left:-70%;
    width:35%;height:200%;
    background:linear-gradient(108deg,transparent,rgba(255,255,255,0.035),transparent);
    transform:rotate(20deg);transition:left 0.7s ease;pointer-events:none;
}
.movie-card-ultra:hover::after{left:130%;}

.poster-area{width:100%;height:200px;position:relative;overflow:hidden;flex-shrink:0;}
.poster-gradient{width:100%;height:100%;display:flex;align-items:center;justify-content:center;position:relative;}
.poster-title-overlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1rem;text-align:center;}
.poster-big-icon{font-size:3rem;opacity:0.85;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.6));margin-bottom:0.5rem;}
.poster-movie-name{font-family:'Outfit',sans-serif;font-weight:800;font-size:0.95rem;color:rgba(255,255,255,0.9);text-shadow:0 2px 8px rgba(0,0,0,0.8);text-align:center;line-height:1.2;max-width:90%;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.rank-badge{position:absolute;top:10px;left:12px;background:linear-gradient(135deg,var(--gold),#ff6b35);color:#000;font-family:'Bebas Neue',sans-serif;font-size:1rem;padding:3px 10px;border-radius:8px;letter-spacing:1px;box-shadow:0 4px 12px rgba(255,215,0,0.4);z-index:3;}
.rating-on-poster{position:absolute;top:10px;right:12px;background:rgba(0,0,0,0.75);backdrop-filter:blur(8px);border:1px solid rgba(255,215,0,0.3);color:var(--gold);font-weight:700;font-size:0.82rem;padding:4px 10px;border-radius:10px;z-index:3;}
.poster-fade{position:absolute;bottom:0;left:0;right:0;height:60%;background:linear-gradient(to top,rgba(8,8,18,1) 0%,transparent 100%);pointer-events:none;}

.card-body{padding:1rem 1.3rem 1.3rem;}
.card-title-text{font-family:'Outfit',sans-serif;font-weight:700;font-size:1.1rem;color:#eef0f8;margin-bottom:0.5rem;line-height:1.25;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;letter-spacing:-0.01em;}
.card-chips{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:0.7rem;}
.chip{font-size:0.7rem;font-weight:600;padding:3px 10px;border-radius:20px;letter-spacing:0.3px;}
.chip-genre{background:rgba(0,212,255,0.08);color:var(--neon);border:1px solid rgba(0,212,255,0.18);}
.chip-year{background:rgba(255,215,0,0.07);color:var(--gold);border:1px solid rgba(255,215,0,0.18);}
.chip-runtime{background:rgba(124,58,237,0.1);color:#a78bfa;border:1px solid rgba(124,58,237,0.2);}
.card-overview-text{color:#5a6380;font-size:0.83rem;line-height:1.65;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
.score-bar-wrap{margin-top:0.9rem;display:flex;align-items:center;gap:10px;}
.score-bar-bg{flex:1;height:4px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;}
.score-bar-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--red),var(--gold));box-shadow:0 0 8px rgba(233,69,96,0.5);transition:width 0.6s ease;}
.score-label{font-size:0.75rem;font-weight:700;color:var(--gold);white-space:nowrap;}

/* ─── Search Select ──────────────────────────────────── */
.stSelectbox>div>div {
    background:rgba(8,8,25,0.85)!important;border:1px solid rgba(0,212,255,0.2)!important;
    border-radius:16px!important;color:var(--text)!important;backdrop-filter:blur(12px)!important;
    transition:all 0.25s ease!important;font-size:1rem!important;
}
.stSelectbox>div>div:focus-within{border-color:var(--neon)!important;box-shadow:0 0 0 3px rgba(0,212,255,0.1),0 8px 30px rgba(0,0,0,0.4)!important;}
.stSelectbox label{color:var(--muted)!important;font-size:0.78rem!important;letter-spacing:2px!important;text-transform:uppercase!important;font-weight:600!important;}

/* ─── Carousel ───────────────────────────────────────── */
.carousel-wrap{position:relative;z-index:2;margin:0.5rem 0 1.5rem;}
.carousel-row{display:flex;gap:1rem;overflow-x:auto;padding-bottom:1rem;scroll-snap-type:x mandatory;scrollbar-width:thin;scrollbar-color:var(--red) transparent;}
.carousel-row::-webkit-scrollbar{height:4px;}
.carousel-row::-webkit-scrollbar-track{background:transparent;}
.carousel-row::-webkit-scrollbar-thumb{background:linear-gradient(90deg,var(--red),var(--purple));border-radius:4px;}
.carousel-item{flex:0 0 220px;scroll-snap-align:start;}
.mini-card{background:linear-gradient(160deg,rgba(16,16,35,0.98),rgba(8,8,18,0.99));border:1px solid rgba(255,255,255,0.055);border-radius:18px;overflow:hidden;transition:transform 0.3s cubic-bezier(.23,1,.32,1),box-shadow 0.3s ease;position:relative;}
.mini-card:hover{transform:translateY(-6px) scale(1.03);box-shadow:0 20px 40px rgba(0,0,0,0.55),0 0 20px rgba(233,69,96,0.1);border-color:rgba(233,69,96,0.25);}
.mini-poster{height:145px;width:100%;position:relative;overflow:hidden;}
.mini-body{padding:0.75rem;}
.mini-title{font-family:'Outfit',sans-serif;font-weight:700;font-size:0.85rem;color:#dde0f0;line-height:1.2;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:0.35rem;}
.mini-rating{font-size:0.75rem;font-weight:700;color:var(--gold);}

/* ─── Detail Card ────────────────────────────────────── */
.detail-hero {
    background:linear-gradient(160deg,rgba(16,16,38,0.98),rgba(6,6,18,0.99));
    border:1px solid rgba(255,215,0,0.12);border-radius:24px;padding:2.2rem;
    position:relative;overflow:hidden;
    box-shadow:0 30px 80px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,215,0,0.1);
    margin-bottom:1.5rem;z-index:2;
}
.detail-hero::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--gold) 25%,var(--red) 75%,transparent);box-shadow:0 0 20px rgba(255,215,0,0.4);}
.detail-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(2rem,4vw,3.2rem);line-height:1;background:linear-gradient(135deg,#fff 0%,var(--gold) 60%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.5rem;letter-spacing:1px;}
.detail-tagline{font-style:italic;color:var(--gold);font-size:1rem;opacity:0.8;border-left:3px solid var(--gold);padding-left:1rem;margin:1rem 0;}
.detail-overview{color:#8892b0;line-height:1.8;font-size:0.92rem;}
.detail-meta-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1.5rem;}
.meta-item{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:1rem;}
.meta-key{font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}
.meta-val{font-size:1.05rem;font-weight:600;color:var(--text);}

/* ─── Misc ───────────────────────────────────────────── */
.no-result{text-align:center;padding:4rem 2rem;color:var(--muted);}
.no-result .nr-icon{font-size:4rem;margin-bottom:1rem;display:block;}
.no-result p{font-size:0.95rem;letter-spacing:1px;text-transform:uppercase;}
.select-prompt{text-align:center;padding:3.5rem 2rem;color:#2a3050;position:relative;z-index:2;}
.select-prompt .sp-icon{font-size:5rem;margin-bottom:1rem;display:block;opacity:0.6;}
.select-prompt p{font-size:0.9rem;letter-spacing:2px;text-transform:uppercase;}
.demo-banner{background:linear-gradient(135deg,rgba(0,212,255,0.06),rgba(124,58,237,0.06));border:1px solid rgba(0,212,255,0.18);border-radius:14px;padding:1rem 1.5rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:14px;font-size:0.87rem;color:#7a8299;position:relative;z-index:2;}
.demo-banner strong{color:var(--neon);}
.trending-label{display:flex;align-items:center;gap:8px;font-family:'Bebas Neue',sans-serif;font-size:0.9rem;letter-spacing:3px;color:var(--red);margin-bottom:0.6rem;position:relative;z-index:2;}
.trending-dot{width:8px;height:8px;border-radius:50%;background:var(--red);animation:blink 1.2s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;box-shadow:0 0 6px var(--red);}50%{opacity:0.3;box-shadow:none;}}
.cinema-footer{text-align:center;padding:2.5rem 0 1.5rem;border-top:1px solid rgba(255,255,255,0.04);margin-top:3rem;position:relative;z-index:2;}
.cinema-footer p{color:#2a3050;font-size:0.76rem;letter-spacing:2px;text-transform:uppercase;}
.cinema-footer span{color:var(--red);}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--red),var(--purple));border-radius:4px;}
.stSpinner>div{border-top-color:var(--neon)!important;}
h3{color:#e8eaf0!important;}
.stMarkdown p{color:#7a8299;}
.stSlider>div>div>div>div{background:linear-gradient(90deg,var(--red),var(--purple))!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════
# PARTICLE SYSTEM (JavaScript)
# ══════════════════════════════════════════════════════════════
st.components.v1.html(
    """
<canvas id="pcvs" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.45;"></canvas>
<script>
(function(){
  var c=document.getElementById('pcvs');
  if(!c)return;
  var ctx=c.getContext('2d');
  var W=c.width=window.innerWidth,H=c.height=window.innerHeight;
  var COLORS=['#e94560','#FFD700','#00d4ff','#7c3aed','#ff6b35'];
  var pts=Array.from({length:55},function(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.5+0.4,dx:(Math.random()-.5)*.35,dy:(Math.random()-.5)*.35,color:COLORS[Math.floor(Math.random()*5)],alpha:Math.random()*.5+.15};});
  function draw(){
    ctx.clearRect(0,0,W,H);
    pts.forEach(function(p){
      ctx.save();ctx.globalAlpha=p.alpha;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=p.color;ctx.shadowBlur=10;ctx.shadowColor=p.color;ctx.fill();ctx.restore();
      p.x+=p.dx;p.y+=p.dy;
      if(p.x<-5)p.x=W+5;if(p.x>W+5)p.x=-5;if(p.y<-5)p.y=H+5;if(p.y>H+5)p.y=-5;
    });
    requestAnimationFrame(draw);
  }
  draw();
  window.addEventListener('resize',function(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;});
})();
</script>
""",
    height=0,
)


# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════
def _build_demo_dataset():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    demo_movies = [
        {"title":"The Shawshank Redemption","genres":"Drama","vote_average":8.7,"vote_count":24000,"release_date":"1994-09-23","runtime":142,"budget":25000000,"revenue":16000000,"tagline":"Fear can hold you prisoner. Hope can set you free.","overview":"Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
        {"title":"The Godfather","genres":"Crime, Drama","vote_average":8.7,"vote_count":18000,"release_date":"1972-03-24","runtime":175,"budget":6000000,"revenue":245066411,"tagline":"An offer you can't refuse.","overview":"The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
        {"title":"The Dark Knight","genres":"Action, Crime, Drama","vote_average":8.5,"vote_count":30000,"release_date":"2008-07-18","runtime":152,"budget":185000000,"revenue":1004934033,"tagline":"Why so serious?","overview":"When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."},
        {"title":"Pulp Fiction","genres":"Crime, Drama","vote_average":8.5,"vote_count":25000,"release_date":"1994-10-14","runtime":154,"budget":8000000,"revenue":213928762,"tagline":"Just because you are a character doesn't mean you have character.","overview":"The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."},
        {"title":"Inception","genres":"Action, Science Fiction, Adventure","vote_average":8.4,"vote_count":32000,"release_date":"2010-07-16","runtime":148,"budget":160000000,"revenue":836836967,"tagline":"Your mind is the scene of the crime.","overview":"A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."},
        {"title":"Interstellar","genres":"Adventure, Drama, Science Fiction","vote_average":8.4,"vote_count":29000,"release_date":"2014-11-07","runtime":169,"budget":165000000,"revenue":701729206,"tagline":"Mankind was born on Earth. It was never meant to die here.","overview":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
        {"title":"The Matrix","genres":"Action, Science Fiction","vote_average":8.2,"vote_count":24000,"release_date":"1999-04-07","runtime":136,"budget":63000000,"revenue":467221000,"tagline":"Welcome to the Real World.","overview":"A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."},
        {"title":"Schindler's List","genres":"Drama, History, War","vote_average":8.6,"vote_count":14000,"release_date":"1993-12-15","runtime":195,"budget":22000000,"revenue":321306305,"tagline":"Whoever saves one life, saves the world entire.","overview":"In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."},
        {"title":"Forrest Gump","genres":"Comedy, Drama, Romance","vote_average":8.5,"vote_count":25000,"release_date":"1994-07-06","runtime":142,"budget":55000000,"revenue":678226133,"tagline":"Life is like a box of chocolates.","overview":"The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75."},
        {"title":"The Lord of the Rings: The Return of the King","genres":"Adventure, Fantasy, Action","vote_average":8.5,"vote_count":21000,"release_date":"2003-12-17","runtime":201,"budget":94000000,"revenue":1120000000,"tagline":"The eye of the enemy is moving.","overview":"Aragorn is revealed as the heir to the ancient kings as he and his friends make a desperate last stand against Sauron's army at Gondor."},
        {"title":"Goodfellas","genres":"Crime, Drama","vote_average":8.5,"vote_count":18000,"release_date":"1990-09-19","runtime":145,"budget":25000000,"revenue":46836394,"tagline":"Three decades of life in the mafia.","overview":"The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito."},
        {"title":"Fight Club","genres":"Drama, Thriller","vote_average":8.4,"vote_count":24000,"release_date":"1999-11-11","runtime":139,"budget":63000000,"revenue":100853753,"tagline":"Mischief. Mayhem. Soap.","overview":"An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more."},
        {"title":"The Silence of the Lambs","genres":"Crime, Drama, Thriller","vote_average":8.3,"vote_count":14000,"release_date":"1991-02-14","runtime":118,"budget":19000000,"revenue":272742922,"tagline":"To enter the mind of a killer she must challenge the mind of a madman.","overview":"A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer."},
        {"title":"Avengers: Infinity War","genres":"Adventure, Action, Science Fiction","vote_average":8.3,"vote_count":27000,"release_date":"2018-04-25","runtime":149,"budget":300000000,"revenue":2048359754,"tagline":"An entire universe. Once and for all.","overview":"As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos."},
        {"title":"Avengers: Endgame","genres":"Adventure, Action, Science Fiction","vote_average":8.3,"vote_count":28000,"release_date":"2019-04-24","runtime":181,"budget":356000000,"revenue":2797800564,"tagline":"Part of the journey is the end.","overview":"After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions."},
        {"title":"Spider-Man: No Way Home","genres":"Action, Adventure, Science Fiction","vote_average":8.2,"vote_count":21000,"release_date":"2021-12-15","runtime":148,"budget":200000000,"revenue":1901216740,"tagline":"The Multiverse unleashed.","overview":"Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero."},
        {"title":"The Lion King","genres":"Animation, Adventure, Drama","vote_average":8.3,"vote_count":17000,"release_date":"1994-06-24","runtime":88,"budget":45000000,"revenue":968483777,"tagline":"Life's greatest adventure is finding your place in the Circle of Life.","overview":"A young lion prince is cast out of his pride by his cruel uncle, who claims he killed his father."},
        {"title":"Toy Story","genres":"Animation, Adventure, Comedy","vote_average":8.0,"vote_count":16000,"release_date":"1995-11-22","runtime":81,"budget":30000000,"revenue":373554033,"tagline":"Hang on for the most hair-raising adventure of all time!","overview":"Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene."},
        {"title":"Guardians of the Galaxy","genres":"Action, Science Fiction, Adventure","vote_average":8.0,"vote_count":22000,"release_date":"2014-08-01","runtime":121,"budget":170000000,"revenue":773328629,"tagline":"You're Welcome.","overview":"Peter Quill finds himself the prime target of a manhunt after discovering an orb wanted by Ronan the Accuser."},
        {"title":"Jurassic Park","genres":"Adventure, Science Fiction, Thriller","vote_average":8.2,"vote_count":15000,"release_date":"1993-06-11","runtime":127,"budget":63000000,"revenue":1029153882,"tagline":"An adventure 65 million years in the making.","overview":"A pragmatic paleontologist is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose."},
        {"title":"The Lord of the Rings: The Fellowship of the Ring","genres":"Adventure, Fantasy, Action","vote_average":8.4,"vote_count":21000,"release_date":"2001-12-19","runtime":178,"budget":93000000,"revenue":871368364,"tagline":"One ring to rule them all.","overview":"A meek Hobbit and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."},
        {"title":"Harry Potter and the Philosopher's Stone","genres":"Adventure, Fantasy","vote_average":7.9,"vote_count":19000,"release_date":"2001-11-16","runtime":152,"budget":125000000,"revenue":974755371,"tagline":"Let the magic begin.","overview":"An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world."},
        {"title":"Star Wars: Episode IV - A New Hope","genres":"Adventure, Action, Science Fiction","vote_average":8.2,"vote_count":19000,"release_date":"1977-05-25","runtime":121,"budget":11000000,"revenue":775398007,"tagline":"A long time ago in a galaxy far, far away...","overview":"Princess Leia is captured by the evil Imperial forces. Rebel pilot Luke Skywalker and Han Solo team up to rescue her."},
        {"title":"Parasite","genres":"Comedy, Drama, Thriller","vote_average":8.5,"vote_count":15000,"release_date":"2019-05-30","runtime":132,"budget":11400000,"revenue":258773645,"tagline":"Act like you own the place.","overview":"Ki-taek's family takes peculiar interest in the wealthy and glamorous Park family and carefully formulates a plan to infiltrate their household."},
        {"title":"Joker","genres":"Crime, Drama, Thriller","vote_average":8.2,"vote_count":22000,"release_date":"2019-10-04","runtime":122,"budget":55000000,"revenue":1074458282,"tagline":"Put on a happy face.","overview":"In Gotham City, mentally troubled comedian Arthur Fleck embarks on a downward spiral of revolution and bloody crime."},
        {"title":"Mad Max: Fury Road","genres":"Action, Adventure, Science Fiction","vote_average":8.1,"vote_count":20000,"release_date":"2015-05-15","runtime":120,"budget":150000000,"revenue":375432728,"tagline":"What a lovely day!","overview":"In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland."},
        {"title":"La La Land","genres":"Comedy, Drama, Music","vote_average":8.0,"vote_count":18000,"release_date":"2016-12-09","runtime":128,"budget":30000000,"revenue":446092357,"tagline":"Here's to the fools who dream.","overview":"A jazz pianist falls for an aspiring actress in Los Angeles."},
        {"title":"Whiplash","genres":"Drama, Music","vote_average":8.5,"vote_count":15000,"release_date":"2014-10-10","runtime":107,"budget":3300000,"revenue":48966143,"tagline":"The road to greatness can take you to the edge.","overview":"A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing."},
        {"title":"Blade Runner 2049","genres":"Science Fiction, Drama","vote_average":8.0,"vote_count":14000,"release_date":"2017-10-06","runtime":164,"budget":150000000,"revenue":259238537,"tagline":"The key to the future is finally unearthed.","overview":"Thirty years after the events of the first film, a new blade runner unearths a long-buried secret that has the potential to plunge what's left of society into chaos."},
        {"title":"Dune","genres":"Science Fiction, Adventure","vote_average":7.9,"vote_count":16000,"release_date":"2021-10-22","runtime":155,"budget":165000000,"revenue":401777413,"tagline":"Beyond fear, destiny awaits.","overview":"Paul Atreides must travel to the most dangerous planet in the universe to ensure the future of his family and his people."},
        {"title":"Top Gun: Maverick","genres":"Action, Drama","vote_average":8.3,"vote_count":17000,"release_date":"2022-05-27","runtime":130,"budget":170000000,"revenue":1491000000,"tagline":"Feel the need... the need for speed.","overview":"After more than thirty years of service, Pete Mitchell is pushing the envelope as a courageous test pilot."},
        {"title":"Oppenheimer","genres":"Drama, History, Thriller","vote_average":8.4,"vote_count":18000,"release_date":"2023-07-21","runtime":181,"budget":100000000,"revenue":952000000,"tagline":"The world forever changes.","overview":"The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II."},
        {"title":"Barbie","genres":"Comedy, Adventure, Fantasy","vote_average":7.0,"vote_count":15000,"release_date":"2023-07-21","runtime":114,"budget":145000000,"revenue":1441600000,"tagline":"She's everything. He's just Ken.","overview":"Barbie and Ken are having the time of their lives in Barbie Land."},
        {"title":"The Batman","genres":"Crime, Mystery, Action","vote_average":7.8,"vote_count":16000,"release_date":"2022-03-04","runtime":176,"budget":185000000,"revenue":770836786,"tagline":"Unmask the truth.","overview":"When the Riddler, a sadistic serial killer, begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption."},
        {"title":"John Wick","genres":"Action, Thriller","vote_average":7.8,"vote_count":17000,"release_date":"2014-10-24","runtime":101,"budget":20000000,"revenue":86003742,"tagline":"Don't set him off.","overview":"An ex-hitman comes out of retirement to track down the gangsters that killed his dog and took everything from him."},
        {"title":"Coco","genres":"Animation, Family, Fantasy","vote_average":8.4,"vote_count":14000,"release_date":"2017-11-22","runtime":105,"budget":175000000,"revenue":807082196,"tagline":"The celebration of a lifetime.","overview":"Despite his family's ban on music, Miguel dreams of becoming an accomplished musician like his idol, Ernesto de la Cruz."},
        {"title":"Get Out","genres":"Horror, Mystery, Thriller","vote_average":7.7,"vote_count":16000,"release_date":"2017-02-24","runtime":104,"budget":4500000,"revenue":255407663,"tagline":"Just because you're invited, doesn't mean you're welcome.","overview":"A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness eventually reaches a boiling point."},
        {"title":"A Quiet Place","genres":"Drama, Horror, Science Fiction","vote_average":7.5,"vote_count":16000,"release_date":"2018-04-06","runtime":90,"budget":17000000,"revenue":340939361,"tagline":"Silence is survival.","overview":"In a post-apocalyptic world, a family is forced to live in near silence while hiding from creatures that hunt by sound."},
        {"title":"Everything Everywhere All at Once","genres":"Action, Science Fiction, Comedy","vote_average":8.0,"vote_count":11000,"release_date":"2022-03-25","runtime":139,"budget":14300000,"revenue":79000000,"tagline":"The Wildest Ride Through the Multiverse.","overview":"An aging Chinese immigrant is swept up in an insane adventure, in which she alone can save the world by exploring other universes."},
        {"title":"The Revenant","genres":"Western, Drama","vote_average":7.9,"vote_count":17000,"release_date":"2015-12-25","runtime":156,"budget":135000000,"revenue":532950503,"tagline":"Blood lost. Life found.","overview":"A frontiersman sets out on a path of vengeance against those who left him for dead after a bear mauling."},
        {"title":"The Grand Budapest Hotel","genres":"Comedy, Drama","vote_average":8.1,"vote_count":14000,"release_date":"2014-03-28","runtime":100,"budget":25000000,"revenue":174800000,"tagline":"Explore the hotel. Room by room.","overview":"The adventures of Gustave H, a legendary concierge at a famous European hotel between the wars."},
        {"title":"Goodfellas","genres":"Crime, Drama","vote_average":8.5,"vote_count":18000,"release_date":"1990-09-19","runtime":145,"budget":25000000,"revenue":46836394,"tagline":"Three decades of life in the mafia.","overview":"The story of Henry Hill and his life in the mob."},
        {"title":"Iron Man","genres":"Action, Science Fiction, Adventure","vote_average":7.6,"vote_count":23000,"release_date":"2008-05-02","runtime":126,"budget":140000000,"revenue":585171547,"tagline":"Heroes aren't born. They're built.","overview":"After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."},
        {"title":"1917","genres":"Drama, War, Action","vote_average":8.0,"vote_count":15000,"release_date":"2019-12-25","runtime":119,"budget":95000000,"revenue":384917788,"tagline":"Time is the enemy.","overview":"Two young British soldiers must cross enemy territory and deliver a message that will stop a deadly attack on hundreds of soldiers."},
        {"title":"Aliens","genres":"Action, Thriller, Science Fiction","vote_average":8.4,"vote_count":12000,"release_date":"1986-07-18","runtime":137,"budget":18000000,"revenue":131000000,"tagline":"This time it's war.","overview":"Fifty-seven years after surviving an apocalyptic attack aboard her space vessel by merciless space creatures, Officer Ripley awakens from a coma."},
        {"title":"The Terminator","genres":"Action, Science Fiction, Thriller","vote_average":8.0,"vote_count":13000,"release_date":"1984-10-26","runtime":107,"budget":6400000,"revenue":78371200,"tagline":"Your future is in its hands.","overview":"A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine."},
        {"title":"Once Upon a Time... in Hollywood","genres":"Drama, Comedy","vote_average":7.5,"vote_count":14000,"release_date":"2019-07-26","runtime":161,"budget":90000000,"revenue":377252722,"tagline":"Hollywood 1969.","overview":"TV star Rick Dalton and his longtime stunt double Cliff Booth make their way around an industry they hardly recognize anymore."},
        {"title":"No Time to Die","genres":"Action, Adventure, Thriller","vote_average":7.3,"vote_count":14000,"release_date":"2021-09-30","runtime":163,"budget":250000000,"revenue":774153007,"tagline":"The world will be watching.","overview":"James Bond has left active service but is drawn back in when a mysterious villain armed with dangerous new technology appears."},
        {"title":"Black Panther","genres":"Action, Adventure, Science Fiction","vote_average":7.5,"vote_count":21000,"release_date":"2018-02-16","runtime":134,"budget":200000000,"revenue":1346739107,"tagline":"Long live the king.","overview":"King T'Challa returns home to Wakanda to serve as his country's new leader."},
        {"title":"Doctor Strange","genres":"Action, Adventure, Fantasy","vote_average":7.5,"vote_count":18000,"release_date":"2016-11-04","runtime":115,"budget":165000000,"revenue":677796076,"tagline":"The impossibilities of space, time and what makes a hero.","overview":"A brilliant but arrogant surgeon gets a new lease on life when a sorcerer trains him to defend the world against evil."},
    ]

    df = pd.DataFrame(demo_movies)
    df["combined_features"] = df["genres"].fillna("") + " " + df["overview"].fillna("") + " " + df.get("tagline", pd.Series([""] * len(df))).fillna("")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return {"cosine_sim": cosine_sim, "movie_data": df, "tfidf": tfidf}


@st.cache_resource
def load_model():
    pkl_path = os.path.join(os.path.dirname(__file__), "model_artifacts.pkl")
    if os.path.exists(pkl_path):
        with open(pkl_path, "rb") as f:
            return pickle.load(f)
    csv_path = os.path.join(os.path.dirname(__file__), "TMDB_movie_dataset_v11.csv")
    if os.path.exists(csv_path):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        movie_data = pd.read_csv(csv_path, encoding="latin1", on_bad_lines="skip")
        movie_data["combined_features"] = movie_data["combined_features"].fillna("")
        subset = movie_data.head(5000).reset_index(drop=True)
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(subset["combined_features"])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return {"cosine_sim": cosine_sim, "movie_data": subset, "tfidf": tfidf}
    return _build_demo_dataset()


artifacts  = load_model()
cosine_sim = artifacts["cosine_sim"]
movie_data = artifacts["movie_data"]

_csv_missing = not os.path.exists(os.path.join(os.path.dirname(__file__), "TMDB_movie_dataset_v11.csv"))
_pkl_missing = not os.path.exists(os.path.join(os.path.dirname(__file__), "model_artifacts.pkl"))
DEMO_MODE = _csv_missing and _pkl_missing

C = movie_data["vote_average"].mean()
m = movie_data["vote_count"].quantile(0.90)

def weighted_rating(row):
    v, R = row["vote_count"], row["vote_average"]
    return (v / (v + m) * R) + (m / (m + v) * C)

movie_data["weighted_score"] = movie_data.apply(weighted_rating, axis=1)

def get_recommendations(title, n=10):
    title_lower = title.strip().lower()
    matches = movie_data[movie_data["title"].str.lower() == title_lower]
    if matches.empty:
        return None
    idx = matches.index[0]
    sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)[1:n+1]
    return movie_data.iloc[[i[0] for i in sim_scores]][["title","genres","vote_average","weighted_score","overview","vote_count","release_date","runtime"]].copy()


# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════
GENRE_PALETTES = {
    "Action":          ("linear-gradient(135deg,#e94560,#ff6b35)", "#e94560", "rgba(233,69,96,0.25)"),
    "Adventure":       ("linear-gradient(135deg,#f59e0b,#ff6b35)", "#f59e0b", "rgba(245,158,11,0.25)"),
    "Animation":       ("linear-gradient(135deg,#10b981,#00d4ff)", "#10b981", "rgba(16,185,129,0.25)"),
    "Comedy":          ("linear-gradient(135deg,#FFD700,#f59e0b)", "#FFD700", "rgba(255,215,0,0.25)"),
    "Crime":           ("linear-gradient(135deg,#7c3aed,#e94560)", "#7c3aed", "rgba(124,58,237,0.25)"),
    "Drama":           ("linear-gradient(135deg,#6366f1,#7c3aed)", "#6366f1", "rgba(99,102,241,0.25)"),
    "Fantasy":         ("linear-gradient(135deg,#ec4899,#7c3aed)", "#ec4899", "rgba(236,72,153,0.25)"),
    "History":         ("linear-gradient(135deg,#b45309,#f59e0b)", "#b45309", "rgba(180,83,9,0.25)"),
    "Horror":          ("linear-gradient(135deg,#1f2937,#e94560)", "#e94560", "rgba(233,69,96,0.2)"),
    "Music":           ("linear-gradient(135deg,#ec4899,#f59e0b)", "#ec4899", "rgba(236,72,153,0.25)"),
    "Mystery":         ("linear-gradient(135deg,#0f172a,#6366f1)", "#6366f1", "rgba(99,102,241,0.2)"),
    "Romance":         ("linear-gradient(135deg,#ec4899,#e94560)", "#ec4899", "rgba(236,72,153,0.25)"),
    "Science Fiction": ("linear-gradient(135deg,#00d4ff,#6366f1)", "#00d4ff", "rgba(0,212,255,0.25)"),
    "Thriller":        ("linear-gradient(135deg,#374151,#7c3aed)", "#7c3aed", "rgba(124,58,237,0.2)"),
    "War":             ("linear-gradient(135deg,#374151,#e94560)", "#e94560", "rgba(233,69,96,0.2)"),
    "Western":         ("linear-gradient(135deg,#b45309,#e94560)", "#b45309", "rgba(180,83,9,0.25)"),
    "Family":          ("linear-gradient(135deg,#10b981,#FFD700)", "#10b981", "rgba(16,185,129,0.25)"),
}
POSTER_ICONS = {
    "Action":"🔥","Adventure":"🗺️","Animation":"✨","Comedy":"😄",
    "Crime":"🕵️","Drama":"🎭","Fantasy":"🔮","History":"📜",
    "Horror":"👻","Music":"🎵","Mystery":"🌀","Romance":"💕",
    "Science Fiction":"🚀","Thriller":"⚡","War":"⚔️","Western":"🤠","Family":"❤️",
}

def get_genre_style(genres_str):
    if not genres_str or pd.isna(genres_str):
        return ("linear-gradient(135deg,#e94560,#7c3aed)","#e94560","rgba(233,69,96,0.25)")
    first = str(genres_str).split(",")[0].strip()
    return GENRE_PALETTES.get(first,("linear-gradient(135deg,#e94560,#7c3aed)","#e94560","rgba(233,69,96,0.25)"))

def get_poster_icon(genres_str):
    if not genres_str or pd.isna(genres_str): return "🎬"
    first = str(genres_str).split(",")[0].strip()
    return POSTER_ICONS.get(first,"🎬")

def genre_chips_html(genres_str, max_chips=3):
    html = ""
    if not genres_str or pd.isna(genres_str): return html
    for g in str(genres_str).split(",")[:max_chips]:
        g = g.strip()
        if g: html += f'<span class="chip chip-genre">{g}</span>'
    return html

def render_ultra_card(row, rank=None):
    title    = row.get("title","Unknown")
    genres   = row.get("genres","")
    overview = str(row.get("overview","")) if pd.notna(row.get("overview",None)) else ""
    overview_short = overview[:240] + ("…" if len(overview)>240 else "")
    vote_avg = row.get("vote_average",0); 
    if pd.isna(vote_avg): vote_avg=0
    runtime  = row.get("runtime",0);    
    if pd.isna(runtime): runtime=0
    rel_date = row.get("release_date","")
    year = str(rel_date)[:4] if rel_date and str(rel_date) not in ("","N/A","nan") else ""
    gradient, accent_color, glow = get_genre_style(genres)
    icon = get_poster_icon(genres)
    chips_html = genre_chips_html(genres)
    if year: chips_html += f'<span class="chip chip-year">📅 {year}</span>'
    if runtime>0: chips_html += f'<span class="chip chip-runtime">⏱ {int(runtime)}m</span>'
    rank_html = f'<div class="rank-badge">#{rank}</div>' if rank else ""
    bar_pct = min(int(vote_avg/10*100),100)
    st.markdown(f"""
        <div class="movie-card-ultra">
          <div class="poster-area">
            <div class="poster-gradient" style="background:{gradient};">
              <div style="position:absolute;inset:0;background:rgba(0,0,0,0.18);"></div>
              <div class="poster-title-overlay">
                <span class="poster-big-icon">{icon}</span>
                <span class="poster-movie-name">{title}</span>
              </div>
            </div>
            {rank_html}
            <div class="rating-on-poster">⭐ {vote_avg:.1f}</div>
            <div class="poster-fade"></div>
          </div>
          <div class="card-body">
            <div class="card-title-text">{title}</div>
            <div class="card-chips">{chips_html}</div>
            <div class="card-overview-text">{overview_short}</div>
            <div class="score-bar-wrap">
              <div class="score-bar-bg"><div class="score-bar-fill" style="width:{bar_pct}%;"></div></div>
              <span class="score-label">{vote_avg:.1f}/10</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# GENRE & STATS PREP
# ══════════════════════════════════════════════════════════════
genres_flat   = movie_data["genres"].fillna("").str.split(", ").explode()
unique_genres = sorted(set(g.strip() for g in genres_flat if g.strip()))
avg_rating    = movie_data["vote_average"].mean()
total_votes   = movie_data["vote_count"].sum()


# ══════════════════════════════════════════════════════════════
# ▶ FILM STRIP HEADER
# ══════════════════════════════════════════════════════════════
holes = ('<span class="film-hole"></span>' * 10 +
         '<span class="film-title-cell">CINEMATCH &nbsp;•&nbsp; AI MOVIE RECOMMENDATIONS &nbsp;•&nbsp; TF-IDF &nbsp;•&nbsp; COSINE SIMILARITY &nbsp;•&nbsp;</span>') * 4
st.markdown(f'''
    <div class="filmstrip-header" style="height:40px;overflow:hidden;">
      <div class="filmstrip-holes">{holes}</div>
    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ▶ HERO SECTION
# ══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">🎬 &nbsp; AI-Powered &nbsp;·&nbsp; TF-IDF &amp; Cosine Similarity</div>
        <div class="hero-title">CineMatch</div>
        <div class="hero-tagline">Discover films you'll <strong>love</strong> &nbsp;·&nbsp; Powered by Machine Learning</div>
        <div class="hero-line"></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ▶ STAT CARDS
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card" style="--border-color:rgba(255,215,0,0.5);--glow-color:rgba(255,215,0,0.1);--val-gradient:linear-gradient(135deg,#FFD700,#ff6b35);">
            <span class="s-icon">🎞️</span><div class="s-val">{len(movie_data):,}</div><div class="s-lbl">Movies in DB</div>
        </div>
        <div class="stat-card" style="--border-color:rgba(0,212,255,0.5);--glow-color:rgba(0,212,255,0.1);--val-gradient:linear-gradient(135deg,#00d4ff,#6366f1);">
            <span class="s-icon">🎭</span><div class="s-val">{len(unique_genres)}</div><div class="s-lbl">Genres</div>
        </div>
        <div class="stat-card" style="--border-color:rgba(233,69,96,0.5);--glow-color:rgba(233,69,96,0.1);--val-gradient:linear-gradient(135deg,#e94560,#7c3aed);">
            <span class="s-icon">⭐</span><div class="s-val">{avg_rating:.1f}</div><div class="s-lbl">Avg Rating</div>
        </div>
        <div class="stat-card" style="--border-color:rgba(124,58,237,0.5);--glow-color:rgba(124,58,237,0.1);--val-gradient:linear-gradient(135deg,#7c3aed,#ec4899);">
            <span class="s-icon">🤖</span><div class="s-val">AI</div><div class="s-lbl">ML-Powered</div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

if DEMO_MODE:
    st.markdown("""
        <div class="demo-banner">
            <span style="font-size:1.5rem">📽️</span>
            <div><strong>Demo Mode</strong> — Showcasing 50 iconic films.
            Download <code>TMDB_movie_dataset_v11.csv</code> from
            <a href="https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies"
               target="_blank" style="color:#00d4ff;">Kaggle</a>
            and run <code>python save_model.py</code> to unlock 1M+ movies.</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ▶ TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍  Find Similar", "🏆  Top Rated", "🎭  Browse Genre", "🎯  Mood Finder", "🎥  Movie Details"
])


# ──────────────────────────────────────────────────────────────
# TAB 1 — Find Similar
# ──────────────────────────────────────────────────────────────
with tab1:
    st.markdown('''<div class="sec-header"><span class="sec-header-icon">🔍</span><span class="sec-header-text">Content-Based Discovery</span><div class="sec-header-line"></div></div>''', unsafe_allow_html=True)
    ctrl_col1, ctrl_col2 = st.columns([3, 1])
    with ctrl_col1:
        all_titles = sorted(movie_data["title"].dropna().unique().tolist())
        selected = st.selectbox("🎬  SEARCH FOR A MOVIE:", [""]+all_titles, key="rec_search", help="Type to search")
    with ctrl_col2:
        n_recs = st.slider("Results", 4, 20, 10, key="n_recs")

    if not selected:
        st.markdown('<div class="trending-label"><div class="trending-dot"></div> TRENDING NOW</div>', unsafe_allow_html=True)
        trending = movie_data.nlargest(12, "weighted_score")
        carousel_html = '<div class="carousel-row">'
        for _, row in trending.iterrows():
            t = row.get("title",""); g = row.get("genres","")
            va = row.get("vote_average",0)
            if pd.isna(va): va=0
            grad,_,_ = get_genre_style(g); ico = get_poster_icon(g)
            carousel_html += f"""<div class="carousel-item"><div class="mini-card">
              <div class="mini-poster"><div style="width:100%;height:100%;background:{grad};display:flex;align-items:center;justify-content:center;font-size:2.2rem;position:relative;">
                <div style="position:absolute;inset:0;background:rgba(0,0,0,0.15);"></div>
                <span style="position:relative;z-index:1;">{ico}</span>
                <div style="position:absolute;bottom:0;left:0;right:0;height:50%;background:linear-gradient(to top,rgba(8,8,18,1),transparent);"></div>
                <div style="position:absolute;top:8px;right:8px;background:rgba(0,0,0,0.7);color:#FFD700;font-size:0.72rem;font-weight:700;padding:3px 8px;border-radius:8px;border:1px solid rgba(255,215,0,0.25);">⭐ {va:.1f}</div>
              </div></div>
              <div class="mini-body"><div class="mini-title">{t}</div><div class="mini-rating">⭐ {va:.1f}</div></div>
            </div></div>"""
        carousel_html += "</div>"
        st.markdown(f'<div class="carousel-wrap">{carousel_html}</div>', unsafe_allow_html=True)
        st.markdown('''<div class="select-prompt"><span class="sp-icon">🎬</span><p>Search a movie above to find what to watch next</p></div>''', unsafe_allow_html=True)
    else:
        with st.spinner("🔮 Finding your perfect matches…"):
            results = get_recommendations(selected, n=n_recs)
        if results is not None:
            st.markdown(f'<div class="neon-divider"></div><div class="sec-header"><span class="sec-header-icon">🎯</span><span class="sec-header-text">Because you liked &nbsp;<span style="color:var(--gold)">{selected}</span></span><div class="sec-header-line"></div></div>', unsafe_allow_html=True)
            col_a, col_b = st.columns(2, gap="large")
            for i, (_, row) in enumerate(results.iterrows()):
                with col_a if i%2==0 else col_b: render_ultra_card(row)
        else:
            st.markdown('''<div class="no-result"><span class="nr-icon">🎭</span><p>No match found — try a different title</p></div>''', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# TAB 2 — Top Rated
# ──────────────────────────────────────────────────────────────
with tab2:
    st.markdown('''<div class="sec-header"><span class="sec-header-icon">🏆</span><span class="sec-header-text">Top Rated — IMDb Weighted Formula</span><div class="sec-header-line"></div></div>
    <p style="color:var(--muted);font-size:0.76rem;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:1rem;position:relative;z-index:2;">
        W = (v ÷ v+m) · R + (m ÷ v+m) · C &nbsp;—&nbsp; Votes threshold at 90th percentile</p>''', unsafe_allow_html=True)
    top_n = st.slider("Show top", 10, 30, 20, key="top_slider")
    top = movie_data.nlargest(top_n, "weighted_score").reset_index(drop=True)
    col_a, col_b = st.columns(2, gap="large")
    for rank, (_, row) in enumerate(top.iterrows(), 1):
        with col_a if rank%2!=0 else col_b: render_ultra_card(row, rank=rank)


# ──────────────────────────────────────────────────────────────
# TAB 3 — Genre Browser
# ──────────────────────────────────────────────────────────────
with tab3:
    st.markdown('''<div class="sec-header"><span class="sec-header-icon">🎭</span><span class="sec-header-text">Explore by Genre</span><div class="sec-header-line"></div></div>''', unsafe_allow_html=True)
    genre_icons = {g: POSTER_ICONS.get(g,"🎬") for g in unique_genres}
    pills_html = '<div class="genre-grid">'
    for g in unique_genres:
        grad,color,_ = GENRE_PALETTES.get(g,("linear-gradient(135deg,#e94560,#7c3aed)","#e94560","rgba(233,69,96,0.25)"))
        ico = genre_icons.get(g,"🎬")
        pills_html += f'<div class="genre-pill" style="--genre-color:{grad};"><span>{ico} {g}</span></div>'
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)
    genre = st.selectbox("OR SELECT A GENRE:", [""]+unique_genres, key="genre_select")
    if not genre:
        st.markdown('''<div class="select-prompt"><span class="sp-icon">🎭</span><p>Pick a genre above to see the finest films</p></div>''', unsafe_allow_html=True)
    else:
        filtered  = movie_data[movie_data["genres"].str.contains(genre, na=False)]
        top_genre = filtered.nlargest(12, "weighted_score").reset_index(drop=True)
        grad,color,_ = get_genre_style(genre)
        st.markdown(f'<div class="neon-divider"></div><div class="sec-header"><span class="sec-header-icon">{genre_icons.get(genre,"🎬")}</span><span class="sec-header-text">Top <span style="background:{grad};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{genre}</span> Films</span><div class="sec-header-line"></div></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")
        for i, (_, row) in enumerate(top_genre.iterrows()):
            with col_a if i%2==0 else col_b: render_ultra_card(row, rank=i+1)


# ──────────────────────────────────────────────────────────────
# TAB 4 — Mood Finder
# ──────────────────────────────────────────────────────────────
with tab4:
    st.markdown('''<div class="sec-header"><span class="sec-header-icon">🎯</span><span class="sec-header-text">Mood Finder</span><div class="sec-header-line"></div></div>
    <p style="color:var(--muted);font-size:0.82rem;letter-spacing:1px;margin-bottom:1rem;position:relative;z-index:2;">
        How are you feeling tonight? We'll find the perfect movie for your mood.</p>''', unsafe_allow_html=True)

    MOODS = [
        {"label":"Epic",       "icon":"⚔️", "genres":["Action","Adventure","Fantasy"],  "color":"rgba(233,69,96,0.15)","border":"rgba(233,69,96,0.4)","glow":"rgba(233,69,96,0.2)","text":"#e94560"},
        {"label":"Mind-Blown", "icon":"🤯", "genres":["Science Fiction","Mystery","Thriller"],"color":"rgba(0,212,255,0.12)","border":"rgba(0,212,255,0.35)","glow":"rgba(0,212,255,0.18)","text":"#00d4ff"},
        {"label":"Laugh",      "icon":"😂", "genres":["Comedy"],                        "color":"rgba(255,215,0,0.12)","border":"rgba(255,215,0,0.35)","glow":"rgba(255,215,0,0.18)","text":"#FFD700"},
        {"label":"Emotional",  "icon":"😢", "genres":["Drama","Romance"],               "color":"rgba(99,102,241,0.12)","border":"rgba(99,102,241,0.35)","glow":"rgba(99,102,241,0.18)","text":"#818cf8"},
        {"label":"Spooked",    "icon":"👻", "genres":["Horror","Thriller"],             "color":"rgba(124,58,237,0.12)","border":"rgba(124,58,237,0.35)","glow":"rgba(124,58,237,0.18)","text":"#a78bfa"},
        {"label":"Inspired",   "icon":"🌟", "genres":["History","War","Drama"],         "color":"rgba(180,83,9,0.15)","border":"rgba(245,158,11,0.35)","glow":"rgba(245,158,11,0.18)","text":"#f59e0b"},
        {"label":"Family",     "icon":"🏠", "genres":["Animation","Family","Comedy"],   "color":"rgba(16,185,129,0.12)","border":"rgba(16,185,129,0.35)","glow":"rgba(16,185,129,0.18)","text":"#10b981"},
        {"label":"Romantic",   "icon":"💕", "genres":["Romance","Comedy","Drama"],      "color":"rgba(236,72,153,0.12)","border":"rgba(236,72,153,0.35)","glow":"rgba(236,72,153,0.18)","text":"#ec4899"},
    ]

    mood_grid_html = '<div class="mood-grid">'
    for mood in MOODS:
        mood_grid_html += f'''
        <div class="mood-btn" style="--mood-color:{mood["color"]};--mood-border:{mood["border"]};--mood-glow:{mood["glow"]};">
          <span class="mood-icon">{mood["icon"]}</span>
          <span class="mood-label" style="color:{mood["text"]};">{mood["label"]}</span>
        </div>'''
    mood_grid_html += "</div>"
    st.markdown(mood_grid_html, unsafe_allow_html=True)

    selected_mood = st.session_state.get("selected_mood", None)
    mood_cols = st.columns(4)
    for idx, mood in enumerate(MOODS):
        with mood_cols[idx % 4]:
            if st.button(f'{mood["icon"]}  {mood["label"]}', key=f'mood_{mood["label"]}', use_container_width=True):
                st.session_state["selected_mood"] = mood["label"]
                selected_mood = mood["label"]

    if selected_mood:
        mood_obj = next((m for m in MOODS if m["label"]==selected_mood), None)
        if mood_obj:
            target_genres = mood_obj["genres"]
            mask = movie_data["genres"].fillna("").apply(lambda g: any(tg in g for tg in target_genres))
            mood_movies = movie_data[mask].nlargest(8,"weighted_score").reset_index(drop=True)
            st.markdown(f'<div class="neon-divider"></div><div class="sec-header"><span class="sec-header-icon">{mood_obj["icon"]}</span><span class="sec-header-text">Best <span style="color:{mood_obj["text"]};">{selected_mood}</span> Picks</span><div class="sec-header-line"></div></div>', unsafe_allow_html=True)
            col_a, col_b = st.columns(2, gap="large")
            for i, (_, row) in enumerate(mood_movies.iterrows()):
                with col_a if i%2==0 else col_b: render_ultra_card(row)
    else:
        st.markdown('''<div class="select-prompt" style="margin-top:1rem;"><span class="sp-icon">🎯</span><p>Tap your mood above to get personalised picks</p></div>''', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# TAB 5 — Movie Details
# ──────────────────────────────────────────────────────────────
with tab5:
    st.markdown('''<div class="sec-header"><span class="sec-header-icon">🎥</span><span class="sec-header-text">Movie Metadata Explorer</span><div class="sec-header-line"></div></div>''', unsafe_allow_html=True)
    all_titles_detail = sorted(movie_data["title"].dropna().unique().tolist())
    detail_movie = st.selectbox("SELECT A MOVIE:", [""]+all_titles_detail, key="detail_search")

    if not detail_movie:
        st.markdown('''<div class="select-prompt"><span class="sp-icon">🎥</span><p>Select a movie to dive deep into its details</p></div>''', unsafe_allow_html=True)
    else:
        match = movie_data[movie_data["title"].str.lower()==detail_movie.strip().lower()]
        if not match.empty:
            info = match.iloc[0]
            vote_avg   = info.get("vote_average",0);   
            if pd.isna(vote_avg): vote_avg=0
            vote_count = info.get("vote_count",0);     
            if pd.isna(vote_count): vote_count=0
            runtime    = info.get("runtime",0);        
            if pd.isna(runtime): runtime=0
            budget     = info.get("budget",0);         
            if pd.isna(budget): budget=0
            revenue    = info.get("revenue",0);        
            if pd.isna(revenue): revenue=0
            tagline    = info.get("tagline","")
            overview   = info.get("overview","No overview available.")
            if pd.isna(overview): overview="No overview available."
            genres_str = info.get("genres","N/A")
            rel_date   = info.get("release_date","N/A")
            ws         = info.get("weighted_score",0); 
            if pd.isna(ws): ws=0

            gradient, accent, glow = get_genre_style(genres_str)
            icon = get_poster_icon(genres_str)
            chips_html = genre_chips_html(genres_str, max_chips=10)
            tagline_html = f'<div class="detail-tagline">"{tagline}"</div>' if pd.notna(tagline) and tagline else ""
            budget_str  = f"${int(budget):,}"  if budget>0  else "N/A"
            revenue_str = f"${int(revenue):,}" if revenue>0 else "N/A"
            runtime_str = f"{int(runtime)} min" if runtime>0 else "N/A"
            ws_str      = f"{ws:.2f}" if ws else "N/A"
            year        = str(rel_date)[:4] if rel_date and str(rel_date)!="N/A" else "N/A"
            roi = "N/A"
            if budget>0 and revenue>0:
                roi_val = ((revenue-budget)/budget)*100
                roi = f"{roi_val:+.0f}%"
            bar_pct = min(int(vote_avg/10*100),100)

            st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
            d_col1, d_col2 = st.columns([1,2], gap="large")

            with d_col1:
                st.markdown(f"""
                    <div style="background:{gradient};border-radius:20px;height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.5);">
                      <div style="position:absolute;inset:0;background:rgba(0,0,0,0.2);"></div>
                      <span style="font-size:4.5rem;position:relative;z-index:1;filter:drop-shadow(0 4px 16px rgba(0,0,0,0.6));">{icon}</span>
                      <div style="position:absolute;bottom:0;left:0;right:0;padding:1rem;text-align:center;background:linear-gradient(to top,rgba(0,0,0,0.85),transparent);">
                        <div style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1rem;color:#fff;position:relative;z-index:1;">{info['title']}</div>
                      </div>
                      <div style="position:absolute;top:12px;right:12px;background:rgba(0,0,0,0.7);color:#FFD700;font-size:0.85rem;font-weight:700;padding:5px 12px;border-radius:10px;border:1px solid rgba(255,215,0,0.3);">⭐ {vote_avg:.1f}</div>
                    </div>
                    <div style="margin-top:1rem;position:relative;z-index:2;">
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                        <span style="color:var(--muted);font-size:0.72rem;letter-spacing:2px;text-transform:uppercase;font-weight:600;">USER SCORE</span>
                        <span style="color:var(--gold);font-weight:700;font-size:0.9rem;">{vote_avg:.1f} / 10</span>
                      </div>
                      <div style="height:6px;background:rgba(255,255,255,0.06);border-radius:6px;overflow:hidden;">
                        <div style="height:100%;width:{bar_pct}%;background:linear-gradient(90deg,{accent},{accent}88);border-radius:6px;box-shadow:0 0 10px {accent}66;"></div>
                      </div>
                      <div style="margin-top:8px;color:var(--muted);font-size:0.75rem;letter-spacing:1px;">{int(vote_count):,} votes</div>
                    </div>""", unsafe_allow_html=True)

            with d_col2:
                roi_color = '#10b981' if roi!="N/A" and "+" in roi else '#e94560' if roi!="N/A" else 'var(--muted)'
                st.markdown(f"""
                    <div class="detail-hero">
                      <div class="detail-title">{info['title']}</div>
                      <div class="card-chips" style="margin-bottom:0.5rem;">{chips_html}</div>
                      {tagline_html}
                      <div class="detail-overview">{overview}</div>
                      <div class="detail-meta-grid">
                        <div class="meta-item"><div class="meta-key">📅 Release Year</div><div class="meta-val">{year}</div></div>
                        <div class="meta-item"><div class="meta-key">⏱️ Runtime</div><div class="meta-val">{runtime_str}</div></div>
                        <div class="meta-item"><div class="meta-key">⚖️ Weighted Score</div><div class="meta-val">{ws_str}</div></div>
                        <div class="meta-item"><div class="meta-key">💰 Budget</div><div class="meta-val">{budget_str}</div></div>
                        <div class="meta-item"><div class="meta-key">💵 Box Office</div><div class="meta-val">{revenue_str}</div></div>
                        <div class="meta-item"><div class="meta-key">📈 ROI</div><div class="meta-val" style="color:{roi_color};">{roi}</div></div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            st.markdown(f'<div class="neon-divider"></div><div class="sec-header"><span class="sec-header-icon">🎯</span><span class="sec-header-text">You Might Also Like</span><div class="sec-header-line"></div></div>', unsafe_allow_html=True)
            sim = get_recommendations(detail_movie, n=6)
            if sim is not None:
                col_a, col_b = st.columns(2, gap="large")
                for i,(_, row) in enumerate(sim.iterrows()):
                    with col_a if i%2==0 else col_b: render_ultra_card(row)
        else:
            st.markdown('''<div class="no-result"><span class="nr-icon">🎭</span><p>Movie not found in the database</p></div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ▶ FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="cinema-footer">
        <p>Built with <span>♥</span> by <strong style="color:#c8ccd8;">Vignesh M</strong>
        &nbsp;•&nbsp; Powered by TF-IDF &amp; Cosine Similarity
        &nbsp;•&nbsp; Data: TMDB Movie Dataset &nbsp;•&nbsp; 🎬 CineMatch</p>
    </div>""", unsafe_allow_html=True)
