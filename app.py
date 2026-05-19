import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

from scraper import fetch_real_jobs

# -----------------------------
# LOAD ENV VARIABLES & SECRETS
# -----------------------------
load_dotenv()

try:
    app_id = os.getenv("ADZUNA_APP_ID") or st.secrets["ADZUNA_APP_ID"]
    app_key = os.getenv("ADZUNA_APP_KEY") or st.secrets["ADZUNA_APP_KEY"]
except (KeyError, FileNotFoundError):
    app_id = None
    app_key = None

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="HireScope",
    page_icon=None,
    layout="wide"
)

# -----------------------------
# GLOBAL CSS – Premium Dark Analytics Theme
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(79,139,249,0.25), transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: #a0aec0;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(79,139,249,0.2);
    border: 1px solid rgba(79,139,249,0.4);
    color: #7eb3ff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── KPI METRIC CARDS ── */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    border: 1px solid rgba(79,139,249,0.3);
    padding: 20px 24px;
    border-radius: 14px;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(79,139,249,0.2);
}
div[data-testid="metric-container"] label {
    color: #a0aec0 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* ── JOB CARDS ── */
.job-card {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    padding: 20px 24px;
    border-radius: 14px;
    margin-bottom: 14px;
    border: 1px solid rgba(79,139,249,0.2);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
}
.job-card::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #4F8BF9, #7c3aed);
    border-radius: 4px 0 0 4px;
}
.job-card:hover {
    border-color: rgba(79,139,249,0.6);
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(79,139,249,0.2);
}
.job-title {
    margin: 0 0 10px 0;
    color: #e2e8f0;
    font-size: 1.1rem;
    font-weight: 600;
}
.job-detail {
    margin: 5px 0;
    color: #94a3b8;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.job-detail strong {
    color: #cbd5e1;
}
.skill-tag {
    display: inline-block;
    background: rgba(79,139,249,0.15);
    border: 1px solid rgba(79,139,249,0.3);
    color: #7eb3ff;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 2px 10px;
    border-radius: 20px;
    margin: 3px 3px 0 0;
}
.salary-badge {
    display: inline-block;
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34d399;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 20px;
    margin-top: 6px;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(79,139,249,0.3);
}

/* ── DIVIDER ── */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO BANNER
# -----------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Live Data Analytics</div>
    <h1 class="hero-title">HireScope</h1>
    <p class="hero-subtitle">Real-Time Job Market Intelligence Platform &nbsp;·&nbsp; Powered by Adzuna API</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "df" not in st.session_state:
    try:
        fallback_df = pd.read_csv("indian_jobs.csv")

        locations = ["Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi"]
        if "Location" not in fallback_df.columns:
            fallback_df["Location"] = [locations[i % len(locations)] for i in range(len(fallback_df))]

        if "skills" not in fallback_df.columns:
            skills_data = [
                "SQL,Python,Excel",
                "Power BI,SQL,Excel",
                "Python,Machine Learning,SQL",
                "Tableau,Excel,SQL"
            ]
            fallback_df["skills"] = [skills_data[i % len(skills_data)] for i in range(len(fallback_df))]

        if "salary" not in fallback_df.columns:
            salary_data = [400000, 500000, 700000, 900000]
            fallback_df["salary"] = [salary_data[i % len(salary_data)] for i in range(len(fallback_df))]

        st.session_state.df = fallback_df

    except FileNotFoundError:
        st.session_state.df = pd.DataFrame(columns=["Title", "Company", "Location", "skills", "salary"])

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.markdown("## Search Jobs")
job_query = st.sidebar.text_input("Job Title", "Data Analyst")
job_location = st.sidebar.text_input("Location", "India")
num_results = st.sidebar.slider("Number of Results", 10, 100, 50)

if st.sidebar.button("Fetch Real-Time Data", use_container_width=True):
    if not app_id or not app_key:
        st.sidebar.error("Missing API credentials. Check .env file.")
    else:
        with st.spinner("Fetching live data from Adzuna API..."):
            new_df = fetch_real_jobs(
                app_id, app_key,
                query=job_query,
                location=job_location,
                results=num_results
            )
            if new_df is not None and not new_df.empty:
                st.session_state.df = new_df
                st.sidebar.success(f"{len(new_df)} jobs loaded!")
            else:
                st.sidebar.warning("No data found or API error.")

st.sidebar.markdown("---")
st.sidebar.markdown("## Filters")

df_display = st.session_state.df.copy()

if not df_display.empty:
    selected_location = st.sidebar.selectbox(
        "Filter by Location",
        ["All"] + sorted(list(df_display["Location"].unique()))
    )
    if selected_location != "All":
        df_display = df_display[df_display["Location"] == selected_location]
else:
    selected_location = "All"

# -----------------------------
# MAIN CONTENT
# -----------------------------

import streamlit.components.v1 as components
from collections import Counter

if df_display.empty:
    st.info("No data yet. Use the sidebar to fetch real-time jobs.")
else:
    # Read the HTML template
    with open("template.html", "r", encoding="utf-8") as f:
        html_template = f.read()
    
    # Calculate stats
    total_jobs = f"{len(df_display):,}"
    unique_companies = f"{df_display['Company'].nunique():,}"
    salary_df = df_display[df_display["salary"] > 0]
    avg_salary = f"₹{salary_df['salary'].mean() / 100000:.1f}L" if not salary_df.empty else "N/A"
    
    # Generate Companies HTML
    companies_html = ""
    top_companies = df_display["Company"].value_counts().head(7)
    max_comp_count = top_companies.max() if not top_companies.empty else 1
    for comp, count in top_companies.items():
        width = int((count / max_comp_count) * 100)
        companies_html += f'<div class="bar-row"><span class="bar-label">{comp}</span><div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div><span class="bar-count">{count}</span></div>\n'
        
    # Generate Locations HTML
    locations_html = ""
    top_locations = df_display["Location"].value_counts().head(7)
    max_loc_count = top_locations.max() if not top_locations.empty else 1
    for loc, count in top_locations.items():
        width = int((count / max_loc_count) * 100)
        locations_html += f'<div class="bar-row"><span class="bar-label">{loc}</span><div class="bar-track"><div class="bar-fill green" style="width:{width}%"></div></div><span class="bar-count">{count}</span></div>\n'
        
    # Generate Jobs HTML
    jobs_html = ""
    for _, row in df_display.head(5).iterrows():
        salary_text = f"₹{row['salary']/100000:.1f}L" if row["salary"] > 0 else "Not Disclosed"
        jobs_html += f'''
        <div class="job-row">
            <div class="job-row-left">
                <div class="job-title">{row['Title']}</div>
                <div class="job-company">{row['Company']} · {row['Location']}</div>
            </div>
            <div class="job-row-right">
                <span class="job-salary">{salary_text}</span>
            </div>
        </div>'''
        
    # Generate Skills HTML
    skills_html = ""
    valid_skills = [s for s in df_display["skills"] if pd.notna(s) and s != "Not Specified"]
    if valid_skills:
        all_skills = ",".join(valid_skills)
        skills_list = [s.strip() for s in all_skills.split(",") if s.strip()]
        skill_counts = Counter(skills_list).most_common(12)
        for i, (skill, count) in enumerate(skill_counts):
            if i < 3: style = "skill-hot"
            elif i < 8: style = "skill-warm"
            else: style = "skill-cool"
            skills_html += f'<span class="skill-pill {style}">{skill}</span>\n'

    # Inject into template
    html_filled = html_template.replace("{TOTAL_JOBS}", total_jobs)
    html_filled = html_filled.replace("{UNIQUE_COMPANIES}", unique_companies)
    html_filled = html_filled.replace("{AVG_SALARY}", avg_salary)
    html_filled = html_filled.replace("{COMPANIES_HTML}", companies_html)
    html_filled = html_filled.replace("{LOCATIONS_HTML}", locations_html)
    html_filled = html_filled.replace("{JOBS_HTML}", jobs_html)
    html_filled = html_filled.replace("{SKILLS_HTML}", skills_html)
    
    # Hide default Streamlit padding
    st.markdown('''
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
                max-width: 100%;
            }
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    ''', unsafe_allow_html=True)
    
    # Render custom HTML
    components.html(html_filled, height=1800, scrolling=True)
