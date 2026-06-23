"""
app.py
─────────────────────────────────────────────
Streamlit web interface for the Rural Healthcare RAG Assistant.
Design: "Bio-signal interface" — dark medical HUD aesthetic.

Run with:
    streamlit run src/app.py
─────────────────────────────────────────────
"""

import streamlit as st
from rag import load_vectorstore, get_llm, answer_question, check_symptoms

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sehat Sathi · Rural Health Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)
symptom_mode = st.sidebar.toggle("🩹 Symptom Checker Mode", value=False)

# ─────────────────────────────────────────────
#  DESIGN SYSTEM — "Bio-signal interface"
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:        #0A0E0D;
        --bg-deep:   #060908;
        --glass:     rgba(255,255,255,0.045);
        --glass-brd: rgba(255,255,255,0.09);
        --glow:      #3DDC97;
        --glow-soft: rgba(61,220,151,0.35);
        --cyan:      #5EEAD4;
        --coral:     #FF8A5C;
        --text:      #E8F5F0;
        --text-dim:  #7A9089;
        --text-mute: #51635D;
    }

    html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }

    .stApp {
        background: radial-gradient(ellipse 120% 80% at 50% -10%, #0F1F19 0%, var(--bg) 45%, var(--bg-deep) 100%);
    }

    /* Hide default streamlit chrome bits that clash */
    [data-testid="stHeader"] { background: transparent; }

    /* ═══ HERO ═══════════════════════════════ */
    .hero-wrap {
        position: relative;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-brd);
        border-radius: 22px;
        padding: 2.4rem 2rem 2rem 2rem;
        margin-bottom: 1.4rem;
        overflow: hidden;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -50%; left: -20%;
        width: 140%; height: 200%;
        background: radial-gradient(circle, var(--glow-soft) 0%, transparent 60%);
        opacity: 0.18;
        animation: drift 12s ease-in-out infinite alternate;
        pointer-events: none;
    }
    @keyframes drift {
        0%   { transform: translate(0,0) scale(1); }
        100% { transform: translate(8%, 6%) scale(1.15); }
    }

    .hero-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--glow);
        margin-bottom: 0.7rem;
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .live-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: var(--glow);
        box-shadow: 0 0 8px var(--glow);
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1.12;
        margin: 0 0 0.6rem 0;
        position: relative;
        z-index: 1;
        background: linear-gradient(135deg, #FFFFFF 0%, var(--cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        font-size: 0.95rem;
        color: var(--text-dim);
        max-width: 460px;
        line-height: 1.55;
        margin-bottom: 1.3rem;
        position: relative;
        z-index: 1;
    }

    /* Bio-signal monitor strip — signature element */
    .vitals-strip {
        position: relative;
        z-index: 1;
        background: rgba(0,0,0,0.3);
        border: 1px solid var(--glass-brd);
        border-radius: 12px;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 14px;
        overflow: hidden;
    }
    .vitals-svg { width: 100%; height: 32px; flex: 1; }
    .vitals-line {
        stroke: var(--glow);
        stroke-width: 2;
        fill: none;
        stroke-linecap: round;
        filter: drop-shadow(0 0 4px var(--glow-soft));
        stroke-dasharray: 300;
        stroke-dashoffset: 300;
        animation: scan 3.2s linear infinite;
    }
    @keyframes scan {
        0%   { stroke-dashoffset: 300; }
        70%  { stroke-dashoffset: -300; }
        100% { stroke-dashoffset: -300; }
    }
    .vitals-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--cyan);
        white-space: nowrap;
        font-weight: 500;
    }

    /* ═══ STAT STRIP ═════════════════════════ */
    .stat-strip { display: flex; gap: 0.7rem; margin-bottom: 1.6rem; }
    .stat-pill {
        flex: 1;
        background: var(--glass);
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-brd);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        transition: border-color 0.2s ease;
    }
    .stat-pill:hover { border-color: var(--glow-soft); }
    .stat-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--glow);
        line-height: 1.3;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .stat-label {
        font-size: 0.66rem;
        color: var(--text-mute);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-weight: 600;
        margin-top: 3px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ═══ CHAT ═══════════════════════════════ */
    [data-testid="stChatMessage"] {
        background: var(--glass) !important;
        backdrop-filter: blur(14px);
        border: 1px solid var(--glass-brd);
        border-radius: 16px;
        padding: 0.3rem 0.3rem;
        margin-bottom: 0.6rem;
    }
    div[data-testid="stChatMessageContent"] {
        font-size: 0.95rem;
        line-height: 1.6;
        color: var(--text);
    }
    div[data-testid="stChatMessageContent"] p { color: var(--text); }

    .source-tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(61,220,151,0.08);
        color: var(--glow);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin: 6px 5px 0 0;
        border: 1px solid rgba(61,220,151,0.25);
        font-family: 'JetBrains Mono', monospace;
    }

    .badge-verified {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(61,220,151,0.1);
        color: var(--glow);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        margin: 0 5px 8px 0;
        border: 1px solid rgba(61,220,151,0.3);
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-general {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(255,138,92,0.1);
        color: var(--coral);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        margin: 0 5px 8px 0;
        border: 1px solid rgba(255,138,92,0.3);
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Disclaimer */
    .disclaimer-box {
        background: rgba(255,138,92,0.06);
        border: 1px solid rgba(255,138,92,0.25);
        border-left: 3px solid var(--coral);
        padding: 14px 18px;
        border-radius: 10px;
        font-size: 0.82rem;
        margin-top: 1.6rem;
        margin-bottom: 5rem;
        color: var(--text-dim);
        line-height: 1.55;
    }
    .disclaimer-box b { color: var(--coral); }

    /* Suggested question chips */
    .chip-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-mute);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.6rem;
    }
    div[data-testid="stButton"] button {
        background: var(--glass) !important;
        backdrop-filter: blur(10px);
        color: var(--text) !important;
        border: 1px solid var(--glass-brd) !important;
        border-radius: 24px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.1rem !important;
        transition: all 0.18s ease;
        width: 100%;
    }
    div[data-testid="stButton"] button:hover {
        border-color: var(--glow) !important;
        color: var(--glow) !important;
        box-shadow: 0 0 16px rgba(61,220,151,0.15);
    }

    /* Chat input bar — fix the ugly black void */
    [data-testid="stChatInput"] {
        background: var(--bg) !important;
        border-top: 1px solid var(--glass-brd);
        padding-top: 0.8rem;
    }
    [data-testid="stChatInput"] textarea {
        background: var(--glass) !important;
        backdrop-filter: blur(14px);
        border: 1px solid var(--glass-brd) !important;
        border-radius: 16px !important;
        color: var(--text) !important;
        outline: none !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--glow) !important;
        box-shadow: 0 0 0 1px rgba(61,220,151,0.3) !important;
        outline: none !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: var(--text-mute) !important; }
    [data-testid="stChatInput"] button { color: var(--glow) !important; }
    [data-testid="stBottomBlockContainer"] { background: var(--bg) !important; }
    .stApp > div:last-child { background: transparent; }
    * { outline-color: transparent !important; }
    *:focus { outline: none !important; box-shadow: none !important; }
    [data-testid="stChatInput"] *:focus {
        outline: none !important;
        box-shadow: 0 0 0 1px rgba(61,220,151,0.3) !important;
    }

    /* Sidebar — fix invisible white text */
    section[data-testid="stSidebar"] {
        background: var(--bg-deep);
        border-right: 1px solid var(--glass-brd);
        overflow: hidden !important;
    }
    section[data-testid="stSidebar"]::-webkit-scrollbar { display: none !important; }
    section[data-testid="stSidebar"] > div:first-child {
        overflow: hidden !important;
    }
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar { 
        display: none !important; 
        width: 0 !important;
    }
    section[data-testid="stSidebar"] * { color: var(--text) !important; }
    section[data-testid="stSidebar"] h3 { color: var(--glow) !important; font-family: 'Space Grotesk', sans-serif; }
    section[data-testid="stSidebar"] em { color: var(--text-dim) !important; }
    section[data-testid="stSidebar"] strong { color: var(--cyan) !important; }
    section[data-testid="stSidebar"] hr { border-color: var(--glass-brd); }

    /* Avatar glow */
    [data-testid="stChatMessageAvatarCustom"] {
        background: var(--glass) !important;
        border: 1px solid var(--glow-soft) !important;
    }

    /* Spinner text */
    .stSpinner > div { color: var(--glow) !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--glass-brd); border-radius: 4px; }

    /* Fix corner bleed on chat input wrapper */
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] > div > div,
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stBottomBlockContainer"] > div > div {
        background: var(--bg) !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Kill all default borders on chat input */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div,
    [data-testid="stChatInput"] > div > div > div {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    [data-baseweb="textarea"] > div {
        border: 1px solid var(--glass-brd) !important;
        border-radius: 16px !important;
        box-shadow: none !important;
        background: var(--glass) !important;
    }
    [data-baseweb="textarea"] > div:focus-within {
        border-color: rgba(61,220,151,0.4) !important;
        box-shadow: none !important;
    }

    /* Nuclear option — kill ALL red/blue focus borders */
    textarea:focus, input:focus, [contenteditable]:focus,
    textarea, input,
    .stChatInput textarea,
    .stChatInput textarea:focus,
    [data-baseweb] textarea,
    [data-baseweb] textarea:focus,
    [data-baseweb="textarea"] { 
        outline: none !important; 
        border-color: rgba(61,220,151,0.4) !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow"><span class="live-dot"></span>सेहत साथी &nbsp;·&nbsp; SYSTEM ONLINE</div>
    <div class="hero-title">Trusted answers,<br>in plain language.</div>
    <div class="hero-sub">
        Ask any health question. Every answer is grounded in official government
        guidelines and verified medical sources — not guesswork.
    </div>
    <div class="vitals-strip">
        <svg class="vitals-svg" viewBox="0 0 300 32" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
            <path class="vitals-line" d="M0,16 L40,16 L52,4 L64,28 L76,16 L95,16 L110,8 L122,24 L134,16 L300,16" />
        </svg>
        <span class="vitals-label">KNOWLEDGE BASE ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  STAT STRIP
# ─────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
    <div class="stat-pill">
        <div class="stat-num">🏛️ Gov.</div>
        <div class="stat-label">Verified Sources</div>
    </div>
    <div class="stat-pill">
        <div class="stat-num">🔍 RAG</div>
        <div class="stat-label">Retrieval Powered</div>
    </div>
    <div class="stat-pill">
        <div class="stat-num">✅ Free</div>
        <div class="stat-label">Always Accessible</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD MODELS (cached so it only loads once)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_resources():
    vectordb = load_vectorstore()
    llm = get_llm()
    return vectordb, llm

try:
    with st.spinner("🔧 Loading knowledge base..."):
        vectordb, llm = load_resources()
except FileNotFoundError:
    with st.spinner("🏗️ First-time setup: building knowledge base from documents (this takes a few minutes)..."):
        import subprocess
        import sys
        result = subprocess.run([sys.executable, "src/ingest.py"], capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"⚠️ Failed to build knowledge base: {result.stderr}")
            st.stop()
    st.cache_resource.clear()
    vectordb, llm = load_resources()
except ValueError as e:
    st.error(f"⚠️ {e}")
    st.info("Please add your Groq API key to the `.env` file (or Space secrets).")
    st.stop()

# ─────────────────────────────────────────────
#  CHAT HISTORY
# ─────────────────────────────────────────────
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

MAX_QUESTIONS_PER_SESSION = 15

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "नमस्ते 👋 I'm here to help with your health questions. What's on your mind today?",
            "sources": [],
            "is_verified": None
        }
    ]

# ─────────────────────────────────────────────
#  SUGGESTED QUESTION CHIPS (only show before first real question)
# ─────────────────────────────────────────────
SUGGESTIONS = [
    "What are the symptoms of dengue?",
    "How is diabetes managed?",
    "What vaccines do newborns need?",
    "Signs of dehydration in children",
]

clicked_suggestion = None
if len(st.session_state.messages) == 1:
    st.markdown('<div class="chip-label">⌁ Try asking</div>', unsafe_allow_html=True)
    chip_cols = st.columns(2)
    for i, q in enumerate(SUGGESTIONS):
        with chip_cols[i % 2]:
            if st.button(q, key=f"chip_{i}", use_container_width=True):
                clicked_suggestion = q

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🩺" if msg["role"] == "assistant" else "🙋"):
        if msg.get("is_verified") is True:
            st.markdown('<span class="badge-verified">✓ Verified source</span>', unsafe_allow_html=True)
        elif msg.get("is_verified") is False:
            st.markdown('<span class="badge-general">⌁ General knowledge</span>', unsafe_allow_html=True)
        st.markdown(msg["content"])
        if msg.get("sources"):
            tags_html = "".join([f'<span class="source-tag">⌁ {s}</span>' for s in msg["sources"]])
            st.markdown(tags_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHAT INPUT
# ─────────────────────────────────────────────
user_query = st.chat_input("Type your health question here...")
if clicked_suggestion:
    user_query = clicked_suggestion

if user_query:
    if st.session_state.question_count >= MAX_QUESTIONS_PER_SESSION:
        st.warning("⚠️ You've reached the session limit of 15 questions. Please refresh the page to start a new session.")
        st.stop()

    st.session_state.question_count += 1
    st.session_state.messages.append({"role": "user", "content": user_query, "sources": [], "is_verified": None})
    with st.chat_message("user", avatar="🙋"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Analyzing..." if symptom_mode else "Scanning verified sources..."):
            try:
                if symptom_mode:
                    answer = check_symptoms(user_query, llm)
                    sources, is_verified = [], None
                else:
                    answer, sources, is_verified = answer_question(user_query, vectordb, llm, chat_history=st.session_state.messages)
            except Exception as e:
                answer = f"⚠️ Something went wrong: {e}"
                sources = []
                is_verified = None

        if is_verified is True:
            st.markdown('<span class="badge-verified">✓ Verified source</span>', unsafe_allow_html=True)
        elif is_verified is False:
            st.markdown('<span class="badge-general">⌁ General knowledge</span>', unsafe_allow_html=True)
        st.markdown(answer)
        if sources:
            tags_html = "".join([f'<span class="source-tag">⌁ {s}</span>' for s in sources])
            st.markdown(tags_html, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "is_verified": is_verified
    })
    st.rerun()

# ─────────────────────────────────────────────
#  DISCLAIMER
# ─────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-box">
⚠️ <b>Important:</b> This assistant provides general health information based on official guidelines.
It is <b>not a substitute</b> for professional medical advice. For emergencies or serious symptoms,
please visit your nearest health center or call emergency services immediately.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
### 🩺 Sehat Sathi
*Your health companion, grounded in truth.*

---

**How this works**

This assistant uses **RAG (Retrieval Augmented Generation)** — it searches verified documents first, then crafts an answer only from what it finds there.

**Knowledge sources:**
- 🏛️ National Health Mission guidelines
- 🌍 WHO India fact sheets
- 📋 Ayushman Bharat documentation
- 📊 Verified medical Q&A datasets

---
""")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "नमस्ते 👋 I'm here to help with your health questions. What's on your mind today?",
                "sources": []
            }
        ]
        st.rerun()
        