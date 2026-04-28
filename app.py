import streamlit as st
from agents import run_research
from pdf_generator import generate_pdf
import re

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: #000000; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    background: #000;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(83,74,183,0.12) 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #9ca3af;
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.badge span { color: #a78bfa; }
.hero-title {
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    line-height: 1.05;
    letter-spacing: -2px;
    margin-bottom: 1rem;
}
.hero-title em {
    font-style: italic;
    color: #534AB7;
}
.hero-sub {
    font-size: 1.1rem;
    color: #4b5563;
    text-align: center;
    max-width: 480px;
    line-height: 1.7;
    margin-bottom: 3rem;
}
.pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 3rem;
    flex-wrap: wrap;
    justify-content: center;
}
.agent-box {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 10px 18px;
}
.agent-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: rgba(83,74,183,0.2);
    border: 1px solid rgba(83,74,183,0.4);
    color: #a78bfa;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.agent-name { font-size: 12px; font-weight: 600; color: #e5e7eb; }
.agent-role { font-size: 10px; color: #4b5563; margin-top: 1px; }
.pipe-arrow { color: #1f2937; font-size: 20px; padding: 0 8px; }
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    font-size: 16px !important;
    padding: 18px 24px !important;
}
.stTextInput input:focus {
    border-color: rgba(83,74,183,0.6) !important;
    box-shadow: 0 0 0 4px rgba(83,74,183,0.1) !important;
}
.stTextInput input::placeholder { color: #374151 !important; }
.stTextInput label { display: none !important; }
.stButton > button {
    background: #ffffff !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 40px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #f3f4f6 !important;
    transform: translateY(-2px) !important;
}
.chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 1.2rem;
}
.chip {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    color: #4b5563;
}
.section-divider {
    width: 100%;
    height: 1px;
    background: rgba(255,255,255,0.06);
}
.report-section { background: #000; padding: 4rem 3rem; }
.report-label {
    font-size: 10px;
    font-weight: 600;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1rem;
}
.report-title {
    font-size: clamp(1.8rem, 4vw, 3rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.report-body {
    color: #9ca3af;
    font-size: 15px;
    line-height: 1.9;
}
.report-body strong {
    color: #ffffff;
    font-weight: 600;
    display: block;
    font-size: 16px;
    margin-top: 2rem;
    margin-bottom: 0.5rem;
}
.side-panel { padding: 4rem 2rem 4rem 1rem; }
.side-block { margin-bottom: 2.5rem; }
.side-label {
    font-size: 10px;
    font-weight: 600;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.side-item {
    font-size: 12px;
    color: #4b5563;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    line-height: 1.5;
}
.side-item:last-child { border-bottom: none; }
.source-link {
    font-size: 11px;
    color: #374151;
    padding: 5px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    word-break: break-all;
}
.source-link a { color: #534AB7 !important; text-decoration: none !important; }
.source-link a:hover { color: #a78bfa !important; }
.stDownloadButton > button {
    background: transparent !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    border-color: rgba(255,255,255,0.4) !important;
    background: rgba(255,255,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge"><span>⚡</span> LLaMA 3 · LangGraph · Tavily</div>
    <div class="hero-title">Research <em>anything.</em><br>Instantly.</div>
    <div class="hero-sub">4 specialized AI agents collaborate to search the web, extract insights, and write a professional report — in under 90 seconds.</div>
    <div class="pipeline">
        <div class="agent-box">
            <div class="agent-num">1</div>
            <div class="agent-info">
                <div class="agent-name">Planner</div>
                <div class="agent-role">Structures topic</div>
            </div>
        </div>
        <div class="pipe-arrow">→</div>
        <div class="agent-box">
            <div class="agent-num">2</div>
            <div class="agent-info">
                <div class="agent-name">Searcher</div>
                <div class="agent-role">Finds sources</div>
            </div>
        </div>
        <div class="pipe-arrow">→</div>
        <div class="agent-box">
            <div class="agent-num">3</div>
            <div class="agent-info">
                <div class="agent-name">Extractor</div>
                <div class="agent-role">Pulls key facts</div>
            </div>
        </div>
        <div class="pipe-arrow">→</div>
        <div class="agent-box">
            <div class="agent-num">4</div>
            <div class="agent-info">
                <div class="agent-name">Writer</div>
                <div class="agent-role">Writes report</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────
_, mid, _ = st.columns([1, 2, 1])
with mid:
    topic = st.text_input(
        "",
        placeholder="Type any research topic...",
        label_visibility="collapsed",
        value=st.session_state.get("topic", "")
    )
    generate = st.button("Generate Research Report →", key="generate")
    st.markdown("""
    <div class="chips">
        <div class="chip">AI in healthcare</div>
        <div class="chip">Electric vehicles 2025</div>
        <div class="chip">Quantum computing</div>
        <div class="chip">Climate solutions</div>
        <div class="chip">Future of work</div>
    </div>
    """, unsafe_allow_html=True)

# ── GENERATE ──────────────────────────────────────────────────
if generate and topic:
    with st.status("Agents working...", expanded=True) as status:
        st.write("🧭 Planning research structure...")
        st.write("🔍 Searching the web for sources...")
        st.write("⚡ Extracting key insights...")
        st.write("✍️ Writing your report...")
        try:
            result = run_research(topic)
            status.update(label="✅ Report ready!", state="complete")
            st.session_state.report = result['final_report']
            st.session_state.subtopics = result['subtopics']
            st.session_state.sources = result['search_results']
            st.session_state.topic_done = topic
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Error: {str(e)}")

# ── REPORT ────────────────────────────────────────────────────
if "report" in st.session_state:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    left, right = st.columns([2.5, 1])

    with left:
        formatted = st.session_state.report
        formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
        formatted = formatted.replace('\n', '<br>')
        st.markdown(f"""
        <div class="report-section">
            <div class="report-label">Research Report</div>
            <div class="report-title">{st.session_state.topic_done.title()}</div>
            <div class="report-body">{formatted}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        subtopics_html = ''.join(
            f'<div class="side-item">• {s}</div>'
            for s in st.session_state.subtopics
        )
        sources = list({r['url'] for r in st.session_state.sources if r.get('url')})
        sources_html = ''.join(
            f'<div class="source-link"><a href="{u}" target="_blank">{u[:55]}...</a></div>'
            for u in sources[:10]
        )
        st.markdown(f"""
        <div class="side-panel">
            <div class="side-block">
                <div class="side-label">Subtopics</div>
                {subtopics_html}
            </div>
            <div class="side-block">
                <div class="side-label">Sources ({len(sources)})</div>
                {sources_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>" * 6, unsafe_allow_html=True)
        pdf_bytes = generate_pdf(
            st.session_state.topic_done,
            st.session_state.report
        )
        st.download_button(
            label="↓ Download PDF Report",
            data=pdf_bytes,
            file_name=f"research_{st.session_state.topic_done[:30].replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )