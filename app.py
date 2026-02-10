import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf, clean_text
from matcher import rank_resumes

st.set_page_config(
    page_title="ResumeIQ · AI Screening",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

.hero { text-align: center; padding: 3rem 0 2rem 0; margin-bottom: 2rem; }
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
    border: 1px solid rgba(99,102,241,0.4);
    color: #a78bfa;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.5rem 0;
    line-height: 1.1;
}
.hero p { color: #6b7280; font-size: 1.1rem; font-weight: 300; max-width: 500px; margin: 0 auto; }

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 0.75rem;
}

.score-display {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #13131a, #1a1025);
    border: 1px solid #2d1f4e;
    border-radius: 16px;
    margin-bottom: 1rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.score-label { font-size: 0.85rem; color: #6b7280; margin-top: 0.25rem; letter-spacing: 0.05em; }

.badge-strong {
    display: inline-block;
    background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.2));
    border: 1px solid rgba(16,185,129,0.4);
    color: #34d399; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem;
}
.badge-moderate {
    display: inline-block;
    background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(217,119,6,0.2));
    border: 1px solid rgba(245,158,11,0.4);
    color: #fbbf24; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem;
}
.badge-weak {
    display: inline-block;
    background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,38,0.2));
    border: 1px solid rgba(239,68,68,0.4);
    color: #f87171; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem;
}

.skill-matched {
    display: inline-block;
    background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3);
    color: #34d399; padding: 0.2rem 0.65rem; border-radius: 6px; font-size: 0.8rem; margin: 0.2rem;
}
.skill-missing {
    display: inline-block;
    background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
    color: #f87171; padding: 0.2rem 0.65rem; border-radius: 6px; font-size: 0.8rem; margin: 0.2rem;
}

.rank-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #13131a; border: 1px solid #1e1e2e; border-radius: 12px;
    padding: 1rem 1.25rem; margin-bottom: 0.5rem;
}
.rank-number { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; color: #6366f1; width: 2.5rem; }
.rank-name { flex: 1; font-size: 0.95rem; color: #e8e8f0; padding: 0 1rem; }
.rank-score { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.1rem; color: #a78bfa; }

.progress-bar-container { background: #1e1e2e; border-radius: 999px; height: 6px; margin: 1rem 0; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #6366f1, #a78bfa, #60a5fa); }

.stTextArea textarea {
    background: #13131a !important; border: 1px solid #1e1e2e !important;
    border-radius: 12px !important; color: #e8e8f0 !important;
}
[data-testid="stFileUploader"] { background: #13131a; border: 1px dashed #2d2d3e; border-radius: 12px; padding: 0.5rem; }

.custom-divider { height: 1px; background: linear-gradient(90deg, transparent, #2d2d3e, transparent); margin: 2rem 0; }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state-text { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 600; color: #374151; }
.footer { text-align: center; color: #374151; font-size: 0.75rem; padding: 2rem 0 1rem 0; letter-spacing: 0.05em; }

div.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.9rem !important; letter-spacing: 0.05em !important;
    padding: 0.65rem !important; transition: opacity 0.2s !important;
}
div.stButton > button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Powered by Semantic NLP</div>
    <h1>ResumeIQ</h1>
    <p>AI-powered resume screening that understands meaning, not just keywords.</p>
</div>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col1, spacer, col2 = st.columns([5, 0.5, 6])

with col1:
    st.markdown('<div class="section-label">📄 Upload Resumes</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop PDF resumes here", type=["pdf"],
        accept_multiple_files=True, label_visibility="collapsed"
    )
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💼 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job description", height=320,
        placeholder="Paste the full job description here — responsibilities, required skills, qualifications...",
        label_visibility="collapsed"
    )
    analyze = st.button("⚡  Analyze Resumes", use_container_width=True)

with col2:
    if analyze and uploaded_files and job_description:
        with st.spinner("Analyzing with AI..."):
            resumes_dict = {}
            for file in uploaded_files:
                raw_text = extract_text_from_pdf(file)
                clean = clean_text(raw_text)
                resumes_dict[file.name] = clean
            clean_job = clean_text(job_description)
            results = rank_resumes(resumes_dict, clean_job)

        if len(results) == 1:
            r = results[0]
            score = r["score"]
            if score >= 70:
                badge = '<span class="badge-strong">● Strong Match</span>'
            elif score >= 50:
                badge = '<span class="badge-moderate">● Moderate Match</span>'
            else:
                badge = '<span class="badge-weak">● Weak Match</span>'

            st.markdown(f"""
            <div class="score-display">
                <div class="score-number">{score}%</div>
                <div class="score-label">match score</div>
                <br>{badge}
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width:{score}%"></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-label">🏆 Rankings</div>', unsafe_allow_html=True)
            for i, r in enumerate(results):
                score = r["score"]
                color = "#34d399" if score >= 70 else "#fbbf24" if score >= 50 else "#f87171"
                st.markdown(f"""
                <div class="rank-row">
                    <div class="rank-number">#{i+1}</div>
                    <div class="rank-name">{r['filename']}</div>
                    <div class="rank-score" style="color:{color}">{score}%</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<br><div class="section-label">🔍 Skill Analysis</div>', unsafe_allow_html=True)
        for r in results:
            with st.expander(f"**{r['filename']}**  —  {r['score']}%"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="section-label">✅ Matched</div>', unsafe_allow_html=True)
                    if r["matched_skills"]:
                        pills = " ".join([f'<span class="skill-matched">{s}</span>' for s in r["matched_skills"]])
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.markdown('<span style="color:#4b5563;font-size:0.85rem">No strong matches found</span>', unsafe_allow_html=True)
                with c2:
                    st.markdown('<div class="section-label">❌ Missing</div>', unsafe_allow_html=True)
                    if r["missing_skills"]:
                        pills = " ".join([f'<span class="skill-missing">{s}</span>' for s in r["missing_skills"]])
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.markdown('<span style="color:#4b5563;font-size:0.85rem">No major gaps!</span>', unsafe_allow_html=True)

    elif analyze:
        st.warning("Please upload at least one resume and add a job description!")
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">⚡</div>
            <div class="empty-state-text">Upload resumes & paste a job<br>description to get started</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    ResumeIQ · Built with Python, sentence-transformers & Streamlit · Semantic cosine similarity matching
</div>
""", unsafe_allow_html=True)