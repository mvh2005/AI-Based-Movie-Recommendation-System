"""
app.py — CineMatch 3D Cinema — Streamlit Movie Recommendation Web App

Run with:
    streamlit run app.py
"""

import streamlit as st
import pickle
import pandas as pd
import os

# ── Page config (must be first Streamlit command) ─────────────
st.set_page_config(
    page_title="CineMatch 3D — AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# 3D CINEMA THEME  —  Full CSS overhaul
# ══════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* ─── CSS Variables ────────────────────────────────────── */
:root {
    --gold:    #FFD700;
    --red:     #e94560;
    --neon:    #00d4ff;
    --purple:  #7c3aed;
    --bg-deep: #030308;
    --bg-mid:  #0a0a1a;
    --bg-card: #0d1117;
    --glass:   rgba(255,255,255,0.04);
    --border:  rgba(255,255,255,0.07);
    --text:    #e8eaf0;
    --muted:   #6b7280;
    --shine:   linear-gradient(135deg, #FFD700 0%, #ff6b35 50%, #e94560 100%);
}

/* ─── Global Reset & Base ──────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: var(--bg-deep) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

/* Remove Streamlit default padding */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}

/* ─── Animated 3D Stage Background ────────────────────── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(233,69,96,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 60% 30% at 20% 100%, rgba(124,58,237,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 20% at 80% 90%, rgba(0,212,255,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* 3D Perspective grid on the floor */
.stApp::after {
    content: '';
    position: fixed;
    bottom: 0;
    left: -50%;
    width: 200%;
    height: 55vh;
    background:
        linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    transform: perspective(600px) rotateX(70deg);
    transform-origin: center bottom;
    pointer-events: none;
    z-index: 0;
    mask-image: linear-gradient(to top, rgba(0,0,0,0.5) 0%, transparent 70%);
    -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,0.5) 0%, transparent 70%);
}

/* ─── Film Strip Top Header ────────────────────────────── */
.filmstrip-header {
    width: 100%;
    background: #111;
    border-bottom: 3px solid #222;
    border-top: 3px solid #222;
    padding: 8px 0;
    display: flex;
    align-items: center;
    gap: 0;
    overflow: hidden;
    margin-bottom: 0;
    position: relative;
}
.filmstrip-holes {
    display: flex;
    align-items: center;
    gap: 20px;
    animation: filmroll 12s linear infinite;
    white-space: nowrap;
    padding: 0 10px;
}
@keyframes filmroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.film-hole {
    width: 18px;
    height: 14px;
    border-radius: 3px;
    background: var(--bg-deep);
    border: 2px solid #333;
    flex-shrink: 0;
}
.film-title-cell {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 11px;
    color: var(--gold);
    letter-spacing: 3px;
    padding: 0 30px;
    opacity: 0.8;
    flex-shrink: 0;
}

/* ─── Hero Section ─────────────────────────────────────── */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
    z-index: 1;
}
.hero-eyebrow {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 6px;
    color: var(--neon);
    margin-bottom: 0.6rem;
    text-transform: uppercase;
}
.hero-title-3d {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 9rem);
    line-height: 0.9;
    letter-spacing: -0.01em;
    margin: 0 0 0.5rem;

    /* 3-layer text shadow for depth */
    color: #fff;
    text-shadow:
        0 1px 0 #ccc,
        0 2px 0 #bbb,
        0 3px 0 #aaa,
        0 4px 0 #999,
        0 5px 0 #888,
        0 6px 1px rgba(0,0,0,.1),
        0 0 5px rgba(0,0,0,.1),
        0 1px 3px rgba(0,0,0,.3),
        0 3px 5px rgba(0,0,0,.2),
        0 5px 10px rgba(0,0,0,.25),
        0 10px 10px rgba(0,0,0,.2),
        0 20px 20px rgba(0,0,0,.15);

    background: linear-gradient(180deg, #fff 0%, #FFD700 40%, #ff6b35 80%, #e94560 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    transform: perspective(500px) rotateX(8deg);
    display: inline-block;
}
.hero-subtitle {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 2px;
    margin-top: 0.8rem;
    text-transform: uppercase;
}

/* Neon underline beneath title */
.hero-neon-line {
    width: 280px;
    height: 2px;
    margin: 1rem auto 0;
    background: linear-gradient(90deg, transparent, var(--neon), var(--red), var(--gold), transparent);
    border-radius: 2px;
    box-shadow: 0 0 12px var(--neon), 0 0 24px rgba(0,212,255,0.3);
    animation: pulse-line 3s ease-in-out infinite;
}
@keyframes pulse-line {
    0%, 100% { opacity: 1; box-shadow: 0 0 12px var(--neon); }
    50%       { opacity: 0.6; box-shadow: 0 0 24px var(--neon), 0 0 40px rgba(0,212,255,0.3); }
}

/* ─── 3D Stat Cards ─────────────────────────────────────── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0 1.5rem;
}
.stat-3d {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transform: perspective(800px) rotateX(4deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: default;
}
.stat-3d::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,215,0,0.6), transparent);
}
.stat-3d:hover {
    transform: perspective(800px) rotateX(0deg) translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(255,215,0,0.1);
}
.stat-3d .val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    line-height: 1;
    background: var(--shine);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 1px;
}
.stat-3d .lbl {
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.35rem;
}
.stat-3d .stat-icon {
    font-size: 1.5rem;
    margin-bottom: 0.4rem;
    display: block;
}

/* ─── Section Divider ───────────────────────────────────── */
.neon-divider {
    position: relative;
    height: 1px;
    margin: 1.5rem 0;
    background: linear-gradient(90deg, transparent, var(--red) 30%, var(--gold) 50%, var(--neon) 70%, transparent);
    box-shadow: 0 0 8px var(--red);
}

/* ─── Tabs Override ─────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 2px !important;
    backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.5px !important;
    padding: 10px 22px !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--gold) !important;
    background: rgba(255,215,0,0.06) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #e94560 0%, #7c3aed 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 15px rgba(233,69,96,0.4), 0 0 0 1px rgba(255,255,255,0.1) !important;
}

/* ─── 3D Movie Card ─────────────────────────────────────── */
.card-scene {
    perspective: 1000px;
    margin-bottom: 1.2rem;
}
.card-3d {
    background: linear-gradient(145deg, rgba(20,20,35,0.95), rgba(10,10,20,0.98));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 0;
    overflow: hidden;
    position: relative;
    transform: perspective(1000px) rotateY(-2deg) rotateX(1deg);
    transform-style: preserve-3d;
    transition: transform 0.4s cubic-bezier(.23,1,.32,1), box-shadow 0.4s ease;
    box-shadow:
        0 4px 8px rgba(0,0,0,0.3),
        8px 8px 20px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.06);
}
.card-3d:hover {
    transform: perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(-6px) scale(1.01);
    box-shadow:
        0 20px 50px rgba(0,0,0,0.5),
        0 0 30px rgba(233,69,96,0.15),
        inset 0 1px 0 rgba(255,255,255,0.1);
    border-color: rgba(233,69,96,0.3);
}

/* Left accent bar */
.card-3d::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--gold), var(--red), var(--purple));
    border-radius: 18px 0 0 18px;
}

/* Shine overlay on hover */
.card-3d::after {
    content: '';
    position: absolute;
    top: -50%; left: -60%;
    width: 30%;
    height: 200%;
    background: linear-gradient(105deg, transparent, rgba(255,255,255,0.04), transparent);
    transform: rotate(25deg);
    transition: left 0.6s ease;
    pointer-events: none;
}
.card-3d:hover::after {
    left: 130%;
}

.card-inner {
    padding: 1.4rem 1.4rem 1.4rem 1.8rem;
}

.card-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: #f0f0f5;
    margin: 0 0 0.6rem;
    letter-spacing: -0.01em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 0.7rem;
}
.rating-badge-3d {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: linear-gradient(135deg, #e94560, #ff6b35);
    color: #fff;
    padding: 3px 11px 3px 8px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(233,69,96,0.4);
}
.genre-chip {
    display: inline-block;
    background: rgba(0,212,255,0.08);
    color: var(--neon);
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.73rem;
    font-weight: 500;
    border: 1px solid rgba(0,212,255,0.2);
    letter-spacing: 0.3px;
}
.card-overview {
    color: #788090;
    font-size: 0.855rem;
    line-height: 1.65;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Rank number watermark */
.rank-3d {
    position: absolute;
    top: 10px;
    right: 14px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    line-height: 1;
    color: rgba(255,215,0,0.08);
    pointer-events: none;
    user-select: none;
}

/* ─── Search / Select Box ──────────────────────────────── */
.stSelectbox > div > div {
    background: rgba(10,10,25,0.8) !important;
    border-color: rgba(0,212,255,0.2) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(8px);
}
.stSelectbox > div > div:focus-within {
    border-color: var(--neon) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
.stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ─── Detail info grid ─────────────────────────────────── */
.detail-grid-card {
    background: linear-gradient(145deg, rgba(15,15,30,0.95), rgba(8,8,18,0.98));
    border: 1px solid rgba(255,215,0,0.12);
    border-radius: 20px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transform: perspective(1200px) rotateX(2deg);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,215,0,0.1);
}
.detail-grid-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold) 30%, var(--red) 70%, transparent);
    box-shadow: 0 0 15px rgba(255,215,0,0.5);
}
.detail-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    line-height: 1;
    background: linear-gradient(135deg, #fff 0%, var(--gold) 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem;
    letter-spacing: 1px;
}
.detail-meta-row {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}
.detail-key {
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.detail-val {
    color: var(--text);
    font-size: 1rem;
    font-weight: 500;
}
.detail-overview {
    color: #9aa0af;
    line-height: 1.75;
    font-size: 0.92rem;
}
.detail-tagline {
    font-style: italic;
    color: var(--gold);
    font-size: 1rem;
    border-left: 3px solid var(--gold);
    padding-left: 1rem;
    margin: 1rem 0;
    opacity: 0.85;
}

/* ─── Section headers ──────────────────────────────────── */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 3px;
    color: #fff;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(255,215,0,0.3), transparent);
}

/* ─── Demo mode banner ─────────────────────────────────── */
.demo-banner {
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(124,58,237,0.08));
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0 0 1.5rem;
    font-size: 0.88rem;
    color: #9aa0af;
    display: flex;
    align-items: center;
    gap: 12px;
}
.demo-banner strong { color: var(--neon); }

/* ─── Warning / Info ────────────────────────────────────── */
.stAlert {
    border-radius: 12px !important;
    border-left-color: var(--red) !important;
}

/* ─── Footer ────────────────────────────────────────────── */
.cinema-footer {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 3rem;
}
.cinema-footer p {
    color: #3a3f50;
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 0;
}
.cinema-footer span { color: #e94560; }

/* ─── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--red), var(--purple));
    border-radius: 3px;
}

/* ─── Spinner ───────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--neon) !important; }

/* ─── Markdown & text ─────────────────────────────────────── */
h3 { color: #e8eaf0 !important; }
.stMarkdown p { color: #8892b0; }

/* ─── No Results ────────────────────────────────────────── */
.no-result-msg {
    text-align: center;
    padding: 3rem;
    color: var(--muted);
    font-size: 1.1rem;
}

/* ─── Cursor prompt ─────────────────────────────────────── */
.select-prompt {
    text-align: center;
    padding: 4rem 2rem;
    color: #3a3f50;
}
.select-prompt .big-icon { font-size: 4rem; margin-bottom: 1rem; }
.select-prompt p { font-size: 1rem; letter-spacing: 1px; text-transform: uppercase; }

</style>
""",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════

def _build_demo_dataset():
    """Built-in demo dataset of 50 iconic movies — no CSV needed."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    demo_movies = [
        {"title": "The Shawshank Redemption", "genres": "Drama", "vote_average": 8.7, "vote_count": 24000, "release_date": "1994-09-23", "runtime": 142, "budget": 25000000, "revenue": 16000000, "tagline": "Fear can hold you prisoner. Hope can set you free.", "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "status": "Released"},
        {"title": "The Godfather", "genres": "Crime, Drama", "vote_average": 8.7, "vote_count": 18000, "release_date": "1972-03-24", "runtime": 175, "budget": 6000000, "revenue": 245066411, "tagline": "An offer you can't refuse.", "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "status": "Released"},
        {"title": "The Dark Knight", "genres": "Action, Crime, Drama", "vote_average": 8.5, "vote_count": 30000, "release_date": "2008-07-18", "runtime": 152, "budget": 185000000, "revenue": 1004934033, "tagline": "Why so serious?", "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", "status": "Released"},
        {"title": "Pulp Fiction", "genres": "Crime, Drama", "vote_average": 8.5, "vote_count": 25000, "release_date": "1994-10-14", "runtime": 154, "budget": 8000000, "revenue": 213928762, "tagline": "Just because you are a character doesn't mean you have character.", "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "status": "Released"},
        {"title": "Inception", "genres": "Action, Science Fiction, Adventure", "vote_average": 8.4, "vote_count": 32000, "release_date": "2010-07-16", "runtime": 148, "budget": 160000000, "revenue": 836836967, "tagline": "Your mind is the scene of the crime.", "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "status": "Released"},
        {"title": "Interstellar", "genres": "Adventure, Drama, Science Fiction", "vote_average": 8.4, "vote_count": 29000, "release_date": "2014-11-07", "runtime": 169, "budget": 165000000, "revenue": 701729206, "tagline": "Mankind was born on Earth. It was never meant to die here.", "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "status": "Released"},
        {"title": "The Matrix", "genres": "Action, Science Fiction", "vote_average": 8.2, "vote_count": 24000, "release_date": "1999-04-07", "runtime": 136, "budget": 63000000, "revenue": 467221000, "tagline": "Welcome to the Real World.", "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "status": "Released"},
        {"title": "Schindler's List", "genres": "Drama, History, War", "vote_average": 8.6, "vote_count": 14000, "release_date": "1993-12-15", "runtime": 195, "budget": 22000000, "revenue": 321306305, "tagline": "Whoever saves one life, saves the world entire.", "overview": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.", "status": "Released"},
        {"title": "Forrest Gump", "genres": "Comedy, Drama, Romance", "vote_average": 8.5, "vote_count": 25000, "release_date": "1994-07-06", "runtime": 142, "budget": 55000000, "revenue": 678226133, "tagline": "Life is like a box of chocolates.", "overview": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.", "status": "Released"},
        {"title": "The Lord of the Rings: The Return of the King", "genres": "Adventure, Fantasy, Action", "vote_average": 8.5, "vote_count": 21000, "release_date": "2003-12-17", "runtime": 201, "budget": 94000000, "revenue": 1120000000, "tagline": "The eye of the enemy is moving.", "overview": "Aragorn is revealed as the heir to the ancient kings as he and his friends make a desperate last stand against Sauron's army at Gondor.", "status": "Released"},
        {"title": "Goodfellas", "genres": "Crime, Drama", "vote_average": 8.5, "vote_count": 18000, "release_date": "1990-09-19", "runtime": 145, "budget": 25000000, "revenue": 46836394, "tagline": "Three decades of life in the mafia.", "overview": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.", "status": "Released"},
        {"title": "Fight Club", "genres": "Drama, Thriller", "vote_average": 8.4, "vote_count": 24000, "release_date": "1999-11-11", "runtime": 139, "budget": 63000000, "revenue": 100853753, "tagline": "Mischief. Mayhem. Soap.", "overview": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.", "status": "Released"},
        {"title": "The Silence of the Lambs", "genres": "Crime, Drama, Thriller", "vote_average": 8.3, "vote_count": 14000, "release_date": "1991-02-14", "runtime": 118, "budget": 19000000, "revenue": 272742922, "tagline": "To enter the mind of a killer she must challenge the mind of a madman.", "overview": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", "status": "Released"},
        {"title": "Avengers: Infinity War", "genres": "Adventure, Action, Science Fiction", "vote_average": 8.3, "vote_count": 27000, "release_date": "2018-04-25", "runtime": 149, "budget": 300000000, "revenue": 2048359754, "tagline": "An entire universe. Once and for all.", "overview": "As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos.", "status": "Released"},
        {"title": "Avengers: Endgame", "genres": "Adventure, Action, Science Fiction", "vote_average": 8.3, "vote_count": 28000, "release_date": "2019-04-24", "runtime": 181, "budget": 356000000, "revenue": 2797800564, "tagline": "Part of the journey is the end.", "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.", "status": "Released"},
        {"title": "Spider-Man: No Way Home", "genres": "Action, Adventure, Science Fiction", "vote_average": 8.2, "vote_count": 21000, "release_date": "2021-12-15", "runtime": 148, "budget": 200000000, "revenue": 1901216740, "tagline": "The Multiverse unleashed.", "overview": "Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero. When he asks for help from Doctor Strange, the stakes become even more dangerous.", "status": "Released"},
        {"title": "The Lion King", "genres": "Animation, Adventure, Drama", "vote_average": 8.3, "vote_count": 17000, "release_date": "1994-06-24", "runtime": 88, "budget": 45000000, "revenue": 968483777, "tagline": "Life's greatest adventure is finding your place in the Circle of Life.", "overview": "A young lion prince is cast out of his pride by his cruel uncle, who claims he killed his father. While the uncle rules with terror, the prince grows up beyond the Savannah.", "status": "Released"},
        {"title": "Toy Story", "genres": "Animation, Adventure, Comedy", "vote_average": 8.0, "vote_count": 16000, "release_date": "1995-11-22", "runtime": 81, "budget": 30000000, "revenue": 373554033, "tagline": "Hang on for the most hair-raising adventure of all time!", "overview": "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene.", "status": "Released"},
        {"title": "The Avengers", "genres": "Science Fiction, Action, Adventure", "vote_average": 7.7, "vote_count": 25000, "release_date": "2012-05-04", "runtime": 143, "budget": 220000000, "revenue": 1519557910, "tagline": "Some assembly required.", "overview": "When an unexpected enemy emerges and threatens global safety and security, Nick Fury, director of SHIELD, finds himself in need of a team to pull the world back from the brink of disaster.", "status": "Released"},
        {"title": "Guardians of the Galaxy", "genres": "Action, Science Fiction, Adventure", "vote_average": 8.0, "vote_count": 22000, "release_date": "2014-08-01", "runtime": 121, "budget": 170000000, "revenue": 773328629, "tagline": "You're Welcome.", "overview": "Peter Quill finds himself the prime target of a manhunt after discovering an orb wanted by Ronan the Accuser.", "status": "Released"},
        {"title": "Black Panther", "genres": "Action, Adventure, Science Fiction", "vote_average": 7.5, "vote_count": 21000, "release_date": "2018-02-16", "runtime": 134, "budget": 200000000, "revenue": 1346739107, "tagline": "Long live the king.", "overview": "King T'Challa returns home to Wakanda to serve as his country's new leader.", "status": "Released"},
        {"title": "Iron Man", "genres": "Action, Science Fiction, Adventure", "vote_average": 7.6, "vote_count": 23000, "release_date": "2008-05-02", "runtime": 126, "budget": 140000000, "revenue": 585171547, "tagline": "Heroes aren't born. They're built.", "overview": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.", "status": "Released"},
        {"title": "Doctor Strange", "genres": "Action, Adventure, Fantasy", "vote_average": 7.5, "vote_count": 18000, "release_date": "2016-11-04", "runtime": 115, "budget": 165000000, "revenue": 677796076, "tagline": "The impossibilities of space, time and what makes a hero.", "overview": "A brilliant but arrogant surgeon gets a new lease on life when a sorcerer trains him to defend the world against evil.", "status": "Released"},
        {"title": "Thor: Ragnarok", "genres": "Action, Adventure, Comedy, Science Fiction", "vote_average": 7.7, "vote_count": 20000, "release_date": "2017-11-03", "runtime": 130, "budget": 180000000, "revenue": 853977126, "tagline": "No hammer. No problem.", "overview": "Thor is imprisoned on the other side of the universe and finds himself in a race against time to get back to Asgard to stop Ragnarök.", "status": "Released"},
        {"title": "Jurassic Park", "genres": "Adventure, Science Fiction, Thriller", "vote_average": 8.2, "vote_count": 15000, "release_date": "1993-06-11", "runtime": 127, "budget": 63000000, "revenue": 1029153882, "tagline": "An adventure 65 million years in the making.", "overview": "A pragmatic paleontologist is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose.", "status": "Released"},
        {"title": "The Lord of the Rings: The Fellowship of the Ring", "genres": "Adventure, Fantasy, Action", "vote_average": 8.4, "vote_count": 21000, "release_date": "2001-12-19", "runtime": 178, "budget": 93000000, "revenue": 871368364, "tagline": "One ring to rule them all.", "overview": "A meek Hobbit and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.", "status": "Released"},
        {"title": "Harry Potter and the Philosopher's Stone", "genres": "Adventure, Fantasy", "vote_average": 7.9, "vote_count": 19000, "release_date": "2001-11-16", "runtime": 152, "budget": 125000000, "revenue": 974755371, "tagline": "Let the magic begin.", "overview": "An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.", "status": "Released"},
        {"title": "Star Wars: Episode IV - A New Hope", "genres": "Adventure, Action, Science Fiction", "vote_average": 8.2, "vote_count": 19000, "release_date": "1977-05-25", "runtime": 121, "budget": 11000000, "revenue": 775398007, "tagline": "A long time ago in a galaxy far, far away...", "overview": "Princess Leia is captured by the evil Imperial forces. Rebel pilot Luke Skywalker and Han Solo team up to rescue her.", "status": "Released"},
        {"title": "The Terminator", "genres": "Action, Science Fiction, Thriller", "vote_average": 8.0, "vote_count": 13000, "release_date": "1984-10-26", "runtime": 107, "budget": 6400000, "revenue": 78371200, "tagline": "Your future is in its hands.", "overview": "A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine.", "status": "Released"},
        {"title": "Aliens", "genres": "Action, Thriller, Science Fiction", "vote_average": 8.4, "vote_count": 12000, "release_date": "1986-07-18", "runtime": 137, "budget": 18000000, "revenue": 131000000, "tagline": "This time it's war.", "overview": "Fifty-seven years after surviving an apocalyptic attack aboard her space vessel by merciless space creatures, Officer Ripley awakens from a coma.", "status": "Released"},
        {"title": "Get Out", "genres": "Horror, Mystery, Thriller", "vote_average": 7.7, "vote_count": 16000, "release_date": "2017-02-24", "runtime": 104, "budget": 4500000, "revenue": 255407663, "tagline": "Just because you're invited, doesn't mean you're welcome.", "overview": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness eventually reaches a boiling point.", "status": "Released"},
        {"title": "A Quiet Place", "genres": "Drama, Horror, Science Fiction", "vote_average": 7.5, "vote_count": 16000, "release_date": "2018-04-06", "runtime": 90, "budget": 17000000, "revenue": 340939361, "tagline": "Silence is survival.", "overview": "In a post-apocalyptic world, a family is forced to live in near silence while hiding from creatures that hunt by sound.", "status": "Released"},
        {"title": "Parasite", "genres": "Comedy, Drama, Thriller", "vote_average": 8.5, "vote_count": 15000, "release_date": "2019-05-30", "runtime": 132, "budget": 11400000, "revenue": 258773645, "tagline": "Act like you own the place.", "overview": "Ki-taek's family takes peculiar interest in the wealthy and glamorous Park family and carefully formulates a plan to infiltrate their household.", "status": "Released"},
        {"title": "Joker", "genres": "Crime, Drama, Thriller", "vote_average": 8.2, "vote_count": 22000, "release_date": "2019-10-04", "runtime": 122, "budget": 55000000, "revenue": 1074458282, "tagline": "Put on a happy face.", "overview": "In Gotham City, mentally troubled comedian Arthur Fleck embarks on a downward spiral of revolution and bloody crime.", "status": "Released"},
        {"title": "Once Upon a Time... in Hollywood", "genres": "Drama, Comedy", "vote_average": 7.5, "vote_count": 14000, "release_date": "2019-07-26", "runtime": 161, "budget": 90000000, "revenue": 377252722, "tagline": "Hollywood 1969.", "overview": "TV star Rick Dalton and his longtime stunt double Cliff Booth make their way around an industry they hardly recognize anymore.", "status": "Released"},
        {"title": "1917", "genres": "Drama, War, Action", "vote_average": 8.0, "vote_count": 15000, "release_date": "2019-12-25", "runtime": 119, "budget": 95000000, "revenue": 384917788, "tagline": "Time is the enemy.", "overview": "Two young British soldiers must cross enemy territory and deliver a message that will stop a deadly attack on hundreds of soldiers.", "status": "Released"},
        {"title": "Mad Max: Fury Road", "genres": "Action, Adventure, Science Fiction", "vote_average": 8.1, "vote_count": 20000, "release_date": "2015-05-15", "runtime": 120, "budget": 150000000, "revenue": 375432728, "tagline": "What a lovely day!", "overview": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners.", "status": "Released"},
        {"title": "La La Land", "genres": "Comedy, Drama, Music", "vote_average": 8.0, "vote_count": 18000, "release_date": "2016-12-09", "runtime": 128, "budget": 30000000, "revenue": 446092357, "tagline": "Here's to the fools who dream.", "overview": "A jazz pianist falls for an aspiring actress in Los Angeles.", "status": "Released"},
        {"title": "Whiplash", "genres": "Drama, Music", "vote_average": 8.5, "vote_count": 15000, "release_date": "2014-10-10", "runtime": 107, "budget": 3300000, "revenue": 48966143, "tagline": "The road to greatness can take you to the edge.", "overview": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing.", "status": "Released"},
        {"title": "The Revenant", "genres": "Western, Drama", "vote_average": 7.9, "vote_count": 17000, "release_date": "2015-12-25", "runtime": 156, "budget": 135000000, "revenue": 532950503, "tagline": "Blood lost. Life found.", "overview": "A frontiersman sets out on a path of vengeance against those who left him for dead after a bear mauling.", "status": "Released"},
        {"title": "The Grand Budapest Hotel", "genres": "Comedy, Drama", "vote_average": 8.1, "vote_count": 14000, "release_date": "2014-03-28", "runtime": 100, "budget": 25000000, "revenue": 174800000, "tagline": "Explore the hotel. Room by room.", "overview": "The adventures of Gustave H, a legendary concierge at a famous European hotel between the wars, and Zero Moustafa, the lobby boy who becomes his most trusted friend.", "status": "Released"},
        {"title": "Blade Runner 2049", "genres": "Science Fiction, Drama", "vote_average": 8.0, "vote_count": 14000, "release_date": "2017-10-06", "runtime": 164, "budget": 150000000, "revenue": 259238537, "tagline": "The key to the future is finally unearthed.", "overview": "Thirty years after the events of the first film, a new blade runner unearths a long-buried secret that has the potential to plunge what's left of society into chaos.", "status": "Released"},
        {"title": "Dune", "genres": "Science Fiction, Adventure", "vote_average": 7.9, "vote_count": 16000, "release_date": "2021-10-22", "runtime": 155, "budget": 165000000, "revenue": 401777413, "tagline": "Beyond fear, destiny awaits.", "overview": "Paul Atreides must travel to the most dangerous planet in the universe to ensure the future of his family and his people.", "status": "Released"},
        {"title": "No Time to Die", "genres": "Action, Adventure, Thriller", "vote_average": 7.3, "vote_count": 14000, "release_date": "2021-09-30", "runtime": 163, "budget": 250000000, "revenue": 774153007, "tagline": "The world will be watching.", "overview": "James Bond has left active service but is drawn back in when a mysterious villain armed with dangerous new technology appears.", "status": "Released"},
        {"title": "Top Gun: Maverick", "genres": "Action, Drama", "vote_average": 8.3, "vote_count": 17000, "release_date": "2022-05-27", "runtime": 130, "budget": 170000000, "revenue": 1491000000, "tagline": "Feel the need... the need for speed.", "overview": "After more than thirty years of service, Pete Mitchell is pushing the envelope as a courageous test pilot.", "status": "Released"},
        {"title": "Everything Everywhere All at Once", "genres": "Action, Science Fiction, Comedy", "vote_average": 8.0, "vote_count": 11000, "release_date": "2022-03-25", "runtime": 139, "budget": 14300000, "revenue": 79000000, "tagline": "The Wildest Ride Through the Multiverse.", "overview": "An aging Chinese immigrant is swept up in an insane adventure, in which she alone can save the world by exploring other universes.", "status": "Released"},
        {"title": "Oppenheimer", "genres": "Drama, History, Thriller", "vote_average": 8.4, "vote_count": 18000, "release_date": "2023-07-21", "runtime": 181, "budget": 100000000, "revenue": 952000000, "tagline": "The world forever changes.", "overview": "The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.", "status": "Released"},
        {"title": "Barbie", "genres": "Comedy, Adventure, Fantasy", "vote_average": 7.0, "vote_count": 15000, "release_date": "2023-07-21", "runtime": 114, "budget": 145000000, "revenue": 1441600000, "tagline": "She's everything. He's just Ken.", "overview": "Barbie and Ken are having the time of their lives in Barbie Land. However, when they get a chance to go to the real world, they discover the joys and perils of living among humans.", "status": "Released"},
        {"title": "The Batman", "genres": "Crime, Mystery, Action", "vote_average": 7.8, "vote_count": 16000, "release_date": "2022-03-04", "runtime": 176, "budget": 185000000, "revenue": 770836786, "tagline": "Unmask the truth.", "overview": "When the Riddler, a sadistic serial killer, begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption.", "status": "Released"},
        {"title": "John Wick", "genres": "Action, Thriller", "vote_average": 7.8, "vote_count": 17000, "release_date": "2014-10-24", "runtime": 101, "budget": 20000000, "revenue": 86003742, "tagline": "Don't set him off.", "overview": "An ex-hitman comes out of retirement to track down the gangsters that killed his dog and took everything from him.", "status": "Released"},
        {"title": "Coco", "genres": "Animation, Family, Fantasy", "vote_average": 8.4, "vote_count": 14000, "release_date": "2017-11-22", "runtime": 105, "budget": 175000000, "revenue": 807082196, "tagline": "The celebration of a lifetime.", "overview": "Despite his family's ban on music, Miguel dreams of becoming an accomplished musician like his idol, Ernesto de la Cruz.", "status": "Released"},
    ]

    df = pd.DataFrame(demo_movies)
    df["combined_features"] = (
        df["genres"].fillna("") + " " +
        df["overview"].fillna("") + " " +
        df["tagline"].fillna("")
    )
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return {"cosine_sim": cosine_sim, "movie_data": df, "tfidf": tfidf}


@st.cache_resource
def load_model():
    """Load pickled model artifacts → CSV fallback → built-in demo."""
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

# ── Weighted rating ───────────────────────────────────────────
C = movie_data["vote_average"].mean()
m = movie_data["vote_count"].quantile(0.90)


def weighted_rating(row):
    v, R = row["vote_count"], row["vote_average"]
    return (v / (v + m) * R) + (m / (m + v) * C)


movie_data["weighted_score"] = movie_data.apply(weighted_rating, axis=1)


# ── Recommendation engine ────────────────────────────────────
def get_recommendations(title, n=10):
    title_lower = title.strip().lower()
    matches = movie_data[movie_data["title"].str.lower() == title_lower]
    if matches.empty:
        return None
    idx = matches.index[0]
    sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)[1: n + 1]
    movie_indices = [i[0] for i in sim_scores]
    return movie_data.iloc[movie_indices][
        ["title", "genres", "vote_average", "weighted_score", "overview", "vote_count", "release_date", "runtime"]
    ].copy()


# ══════════════════════════════════════════════════════════════
# HELPER — Render a 3D movie card
# ══════════════════════════════════════════════════════════════
def render_3d_card(row, rank=None):
    genres_html = ""
    if pd.notna(row.get("genres", None)):
        for g in str(row["genres"]).split(", "):
            if g.strip():
                genres_html += f'<span class="genre-chip">{g.strip()}</span>'

    overview = str(row.get("overview", "")) if pd.notna(row.get("overview", None)) else ""
    overview_short = overview[:260] + ("…" if len(overview) > 260 else "")

    vote_avg = row.get("vote_average", 0)
    if pd.isna(vote_avg):
        vote_avg = 0

    rank_html = f'<div class="rank-3d">#{rank}</div>' if rank else ""

    st.markdown(
        f"""
        <div class="card-scene">
          <div class="card-3d">
            {rank_html}
            <div class="card-inner">
              <div class="card-title">{row.get("title", "Unknown")}</div>
              <div class="card-meta">
                <span class="rating-badge-3d">⭐ {vote_avg:.1f}</span>
                {genres_html}
              </div>
              <div class="card-overview">{overview_short}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
# FILM STRIP HEADER ANIMATION
# ══════════════════════════════════════════════════════════════
holes = ('<span class="film-hole"></span>' * 12 +
         '<span class="film-title-cell">CINEMATCH 3D &nbsp;•&nbsp; AI MOVIE RECOMMENDATION &nbsp;•&nbsp; COSINE SIMILARITY &nbsp;•&nbsp;</span>') * 4

st.markdown(
    f"""
    <div class="filmstrip-header" style="height:44px;overflow:hidden;">
      <div class="filmstrip-holes">{holes}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-eyebrow">🎬 &nbsp; Powered by TF-IDF &amp; Cosine Similarity</div>
        <div class="hero-title-3d">CineMatch</div>
        <div class="hero-subtitle">Your AI Cinema Guide &nbsp;·&nbsp; Discover. Explore. Watch.</div>
        <div class="hero-neon-line"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════
# STATS BAR
# ══════════════════════════════════════════════════════════════
genres_flat   = movie_data["genres"].fillna("").str.split(", ").explode()
unique_genres = sorted(set(g.strip() for g in genres_flat if g.strip()))
avg_rating    = movie_data["vote_average"].mean()
total_votes   = movie_data["vote_count"].sum()

st.markdown(
    f"""
    <div class="stat-row">
        <div class="stat-3d">
            <span class="stat-icon">🎞️</span>
            <div class="val">{len(movie_data):,}</div>
            <div class="lbl">Movies in DB</div>
        </div>
        <div class="stat-3d">
            <span class="stat-icon">🎭</span>
            <div class="val">{len(unique_genres)}</div>
            <div class="lbl">Genres</div>
        </div>
        <div class="stat-3d">
            <span class="stat-icon">⭐</span>
            <div class="val">{avg_rating:.1f}</div>
            <div class="lbl">Avg Rating</div>
        </div>
        <div class="stat-3d">
            <span class="stat-icon">🤖</span>
            <div class="val">AI</div>
            <div class="lbl">Cosine Similarity</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# ── Demo mode notice ──────────────────────────────────────────
if DEMO_MODE:
    st.markdown(
        """
        <div class="demo-banner">
            <span style="font-size:1.4rem">📽️</span>
            <div>
                <strong>Demo Mode</strong> — showcasing 50 iconic films.
                Download <code>TMDB_movie_dataset_v11.csv</code> from
                <a href="https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies"
                   target="_blank" style="color:#00d4ff;">Kaggle</a>
                and run <code>python save_model.py</code> to unlock 1M+ movies.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍  Find Similar Movies", "🏆  Top Rated", "🎭  Browse by Genre", "🎥  Movie Details"]
)


# ──────────────────────────────────────────────────────────────
# TAB 1 — Content-Based Recommendations
# ──────────────────────────────────────────────────────────────
with tab1:
    st.markdown(
        '<div class="section-header">🔍 Content-Based Discovery</div>',
        unsafe_allow_html=True,
    )

    all_titles = sorted(movie_data["title"].dropna().unique().tolist())
    selected = st.selectbox(
        "SEARCH FOR A MOVIE:",
        [""] + all_titles,
        key="rec_search",
        help="Start typing to filter",
    )

    if not selected:
        st.markdown(
            """
            <div class="select-prompt">
                <div class="big-icon">🎬</div>
                <p>Select a movie above to find similar titles</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("🔮 Scanning the multiverse of movies…"):
            results = get_recommendations(selected, n=10)

        if results is not None:
            st.markdown(
                f'<div class="neon-divider"></div>'
                f'<div class="section-header">Similar to &nbsp;<span style="color:var(--gold)">{selected}</span></div>',
                unsafe_allow_html=True,
            )
            col_l, col_r = st.columns(2, gap="medium")
            for i, (_, row) in enumerate(results.iterrows()):
                with col_l if i % 2 == 0 else col_r:
                    render_3d_card(row)
        else:
            st.markdown(
                '<div class="no-result-msg">🎭 No match found — try another title</div>',
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────────────────────
# TAB 2 — Top Rated
# ──────────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        '<div class="section-header">🏆 Top 20 — IMDb Weighted Rating</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:var(--muted);font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;">'
        'Formula: W = (v / v+m) · R + (m / v+m) · C &nbsp;—&nbsp; Minimum vote threshold at 90th percentile'
        '</p>',
        unsafe_allow_html=True,
    )

    top = movie_data.nlargest(20, "weighted_score").reset_index(drop=True)
    col_l, col_r = st.columns(2, gap="medium")
    for rank, (_, row) in enumerate(top.iterrows(), 1):
        with col_l if rank % 2 != 0 else col_r:
            render_3d_card(row, rank=rank)


# ──────────────────────────────────────────────────────────────
# TAB 3 — Genre Browser
# ──────────────────────────────────────────────────────────────
with tab3:
    st.markdown(
        '<div class="section-header">🎭 Explore by Genre</div>',
        unsafe_allow_html=True,
    )

    genre = st.selectbox("PICK A GENRE:", [""] + unique_genres, key="genre_select")

    if not genre:
        st.markdown(
            """
            <div class="select-prompt">
                <div class="big-icon">🎭</div>
                <p>Choose a genre to see the top-rated films</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        filtered  = movie_data[movie_data["genres"].str.contains(genre, na=False)]
        top_genre = filtered.nlargest(10, "weighted_score").reset_index(drop=True)

        st.markdown(
            f'<div class="neon-divider"></div>'
            f'<div class="section-header">Top <span style="color:var(--gold)">{genre}</span> Films</div>',
            unsafe_allow_html=True,
        )

        col_l, col_r = st.columns(2, gap="medium")
        for i, (_, row) in enumerate(top_genre.iterrows()):
            with col_l if i % 2 == 0 else col_r:
                render_3d_card(row, rank=i + 1)


# ──────────────────────────────────────────────────────────────
# TAB 4 — Movie Details
# ──────────────────────────────────────────────────────────────
with tab4:
    st.markdown(
        '<div class="section-header">🎥 Movie Metadata Explorer</div>',
        unsafe_allow_html=True,
    )

    all_titles_detail = sorted(movie_data["title"].dropna().unique().tolist())
    detail_movie = st.selectbox(
        "SELECT A MOVIE:", [""] + all_titles_detail, key="detail_search"
    )

    if not detail_movie:
        st.markdown(
            """
            <div class="select-prompt">
                <div class="big-icon">🎥</div>
                <p>Select a movie to view its full details</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        match = movie_data[
            movie_data["title"].str.lower() == detail_movie.strip().lower()
        ]
        if not match.empty:
            info = match.iloc[0]

            vote_avg   = info.get("vote_average", 0)
            vote_count = info.get("vote_count", 0)
            runtime    = info.get("runtime", 0)
            budget     = info.get("budget", 0)
            revenue    = info.get("revenue", 0)
            tagline    = info.get("tagline", "")
            overview   = info.get("overview", "No overview available.")
            genres_str = info.get("genres", "N/A")
            rel_date   = info.get("release_date", "N/A")
            ws         = info.get("weighted_score", 0)

            if pd.isna(vote_avg):   vote_avg = 0
            if pd.isna(vote_count): vote_count = 0
            if pd.isna(runtime):    runtime = 0
            if pd.isna(budget):     budget = 0
            if pd.isna(revenue):    revenue = 0
            if pd.isna(overview):   overview = "No overview available."

            # genre chips
            gc_html = ""
            if pd.notna(genres_str):
                for g in str(genres_str).split(", "):
                    if g.strip():
                        gc_html += f'<span class="genre-chip">{g.strip()}</span>'

            tagline_html = (
                f'<div class="detail-tagline">"{tagline}"</div>'
                if pd.notna(tagline) and tagline else ""
            )

            budget_str  = f"${int(budget):,}" if budget > 0 else "N/A"
            revenue_str = f"${int(revenue):,}" if revenue > 0 else "N/A"
            runtime_str = f"{int(runtime)} min" if runtime > 0 else "N/A"
            ws_str      = f"{ws:.2f}" if pd.notna(ws) else "N/A"
            year        = str(rel_date)[:4] if rel_date and str(rel_date) != "N/A" else "N/A"

            st.markdown(
                f"""
                <div class="neon-divider"></div>
                <div class="detail-grid-card">
                    <div class="detail-title">{info['title']}</div>
                    <div class="detail-meta-row">
                        <span class="rating-badge-3d">⭐ {vote_avg:.1f}</span>
                        <span style="color:var(--muted);font-size:0.85rem">({int(vote_count):,} votes)</span>
                        {gc_html}
                    </div>
                    {tagline_html}
                    <div class="detail-overview">{overview}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Metadata grid
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f'<div class="detail-key">📅 Release Year</div><div class="detail-val">{year}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f'<div class="detail-key">⏱️ Runtime</div><div class="detail-val">{runtime_str}</div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f'<div class="detail-key">⚖️ Weighted Score</div><div class="detail-val">{ws_str}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f'<div class="detail-key">💰 Budget</div><div class="detail-val">{budget_str}</div>',
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f'<div class="detail-key">💵 Revenue</div><div class="detail-val">{revenue_str}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f'<div class="detail-key">🎭 Genres</div><div class="detail-val">{genres_str if pd.notna(genres_str) else "N/A"}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="no-result-msg">🎭 Movie not found in the database.</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="cinema-footer">
        <p>
            Built with <span>♥</span> by <strong style="color:#e8eaf0">Vignesh M</strong>
            &nbsp;•&nbsp; Powered by TF-IDF &amp; Cosine Similarity
            &nbsp;•&nbsp; Data: TMDB Movie Dataset
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
