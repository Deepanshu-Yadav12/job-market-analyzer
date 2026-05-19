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
if df_display.empty:
    st.info("No data yet. Use the sidebar to fetch real-time jobs.")
else:
    # ── KPI CARDS ──
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", len(df_display))
    col2.metric("Unique Companies", df_display["Company"].nunique())
    col3.metric("Unique Locations", df_display["Location"].nunique())

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Skills & Salary", "Job Listings"])

    # ─────────── TAB 1: DASHBOARD ───────────
    with tab1:
        st.markdown('<p class="section-header">Market Overview</p>', unsafe_allow_html=True)
        colA, colB = st.columns(2)

        with colA:
            st.markdown("**Top Companies Hiring**")
            st.bar_chart(df_display["Company"].value_counts().head(10))

        with colB:
            st.markdown("**Top Locations**")
            st.bar_chart(df_display["Location"].value_counts().head(10))

    # ─────────── TAB 2: SKILLS & SALARY ───────────
    with tab2:
        st.markdown('<p class="section-header">Skills Analysis</p>', unsafe_allow_html=True)
        valid_skills = [s for s in df_display["skills"] if pd.notna(s) and s != "Not Specified"]

        if valid_skills:
            all_skills = ",".join(valid_skills)
            skills_list = [s.strip() for s in all_skills.split(",") if s.strip()]
            skill_counts = Counter(skills_list)
            skills_df = pd.DataFrame({
                "Skill": list(skill_counts.keys()),
                "Count": list(skill_counts.values())
            }).sort_values(by="Count", ascending=False)

            colC, colD = st.columns([2, 1])
            with colC:
                st.markdown("**Most In-Demand Skills**")
                st.bar_chart(skills_df.set_index("Skill").head(10))
            with colD:
                st.markdown("**Skills Distribution**")
                fig, ax = plt.subplots(figsize=(4, 4))
                fig.patch.set_facecolor('#0f0c29')
                ax.set_facecolor('#0f0c29')
                wedges, texts, autotexts = ax.pie(
                    skills_df["Count"].head(7),
                    labels=skills_df["Skill"].head(7),
                    autopct="%1.0f%%",
                    startangle=140,
                    textprops={'color': '#e2e8f0', 'fontsize': 8}
                )
                for a in autotexts:
                    a.set_color('#ffffff')
                st.pyplot(fig)
        else:
            st.info("No skills data available.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">Salary Insights</p>', unsafe_allow_html=True)
        salary_df = df_display[df_display["salary"] > 0]

        if not salary_df.empty:
            sc1, sc2 = st.columns(2)
            sc1.metric("Average Salary", f"₹{salary_df['salary'].mean():,.0f}")
            sc2.metric("Max Salary", f"₹{salary_df['salary'].max():,.0f}")
            st.markdown("**Salaries by Company**")
            st.bar_chart(salary_df[["Company", "salary"]].set_index("Company").head(15))
        else:
            st.info("No salary data available.")

    # ─────────── TAB 3: JOB CARDS ───────────
    with tab3:
        st.markdown(f'<p class="section-header">{len(df_display)} Job Listings</p>', unsafe_allow_html=True)

        cards_html = ""
        for _, row in df_display.iterrows():
            salary_text = f"₹{row['salary']:,.0f}" if row["salary"] > 0 else "Not Disclosed"
            salary_color = "salary-badge" if row["salary"] > 0 else "salary-badge"

            # Build skill tags
            skills_raw = str(row["skills"]) if pd.notna(row["skills"]) else "Not Specified"
            if skills_raw != "Not Specified":
                skill_tags = "".join(
                    [f'<span class="skill-tag">{s.strip()}</span>' for s in skills_raw.split(",") if s.strip()]
                )
            else:
                skill_tags = '<span class="skill-tag">Not Specified</span>'

            cards_html += f"""
            <div class="job-card">
                <h3 class="job-title">{row['Title']}</h3>
                <p class="job-detail"><strong>Company:</strong>&nbsp; {row['Company']}</p>
                <p class="job-detail"><strong>Location:</strong>&nbsp; {row['Location']}</p>
                <div class="job-detail" style="flex-wrap:wrap; align-items:flex-start;">
                    <span><strong>Skills:</strong>&nbsp;</span>
                    {skill_tags}
                </div>
                <div style="margin-top: 10px;">
                    <span class="{salary_color}">{salary_text}</span>
                </div>
            </div>
            """

        st.markdown(cards_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        csv = df_display.to_csv(index=False)
        st.download_button("Download as CSV", csv, "jobs.csv", "text/csv", use_container_width=True)