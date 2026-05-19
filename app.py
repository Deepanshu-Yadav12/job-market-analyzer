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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0D0D0D !important;
    color: #F0EDE8 !important;
}

/* Override Streamlit Main Container */
.stApp {
    background-color: #0D0D0D;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: #141414;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 40px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: #F0EDE8;
    margin: 0 0 10px 0;
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.hero-title em {
    color: #E8C547;
    font-style: italic;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #8A8680;
    margin: 0;
    font-weight: 300;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: 1px solid rgba(61,173,127,0.3);
    color: #3DAD7F;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── KPI METRIC CARDS ── */
div[data-testid="metric-container"] {
    background: #141414;
    border: 1px solid rgba(255,255,255,0.07);
    padding: 20px 24px;
    border-radius: 12px;
    transition: background 0.2s;
}
div[data-testid="metric-container"]:hover {
    background: #1C1C1C;
}
div[data-testid="metric-container"] label {
    color: #5A5754 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif;
    color: #F0EDE8 !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

/* ── JOB CARDS ── */
.job-card {
    background: #141414;
    padding: 20px 24px;
    border-radius: 12px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.07);
    transition: background 0.2s;
}
.job-card:hover {
    background: #1C1C1C;
}
.job-title {
    margin: 0 0 8px 0;
    color: #F0EDE8;
    font-size: 1.15rem;
    font-weight: 500;
}
.job-detail {
    margin: 4px 0;
    color: #8A8680;
    font-size: 0.85rem;
}
.job-detail strong {
    color: #5A5754;
    font-weight: 500;
}
.skill-tag {
    display: inline-block;
    background: rgba(232,197,71,0.1);
    border: 1px solid rgba(232,197,71,0.2);
    color: #E8C547;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    margin: 4px 4px 0 0;
}
.salary-badge {
    display: inline-block;
    background: rgba(61,173,127,0.1);
    border: 1px solid rgba(61,173,127,0.2);
    color: #3DAD7F;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 6px;
    margin-top: 10px;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #F0EDE8;
    margin: 0 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 30px 0;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #141414 !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO BANNER
# -----------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Live Data Analytics</div>
    <h1 class="hero-title">The <em>smartest</em> way to read the market.</h1>
    <p class="hero-subtitle">Real-Time Job Market Intelligence Platform &nbsp;·&nbsp; Powered by Adzuna API</p>
</div>
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