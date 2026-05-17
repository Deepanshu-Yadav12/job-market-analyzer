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

# Try getting from environment first, then from Streamlit Secrets
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
    page_icon="💼",
    layout="wide"
)

st.title("💼 HireScope – Real-Time Job Insights Platform")
st.write("Analyze job trends, skills, and salaries using real-time API data.")

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "df" not in st.session_state:
    try:
        fallback_df = pd.read_csv("indian_jobs.csv")

        # Add missing columns safely
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
st.sidebar.header("🔍 Search Jobs")

job_query = st.sidebar.text_input("Job Title", "Data Analyst")
job_location = st.sidebar.text_input("Location", "India")
num_results = st.sidebar.slider("Number of Results", 10, 100, 50)

if st.sidebar.button("Fetch Real-Time Data"):
    if not app_id or not app_key:
        st.sidebar.error("Missing API credentials. Check .env file.")
    else:
        with st.spinner("Fetching data from Adzuna API..."):
            new_df = fetch_real_jobs(
                app_id,
                app_key,
                query=job_query,
                location=job_location,
                results=num_results
            )

            if new_df is not None and not new_df.empty:
                st.session_state.df = new_df
                st.sidebar.success("Data fetched successfully!")
            else:
                st.sidebar.warning("No data found or API error.")

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("📂 Filters")

if not st.session_state.df.empty:
    selected_location = st.sidebar.selectbox(
        "Select Location",
        ["All"] + list(st.session_state.df["Location"].unique())
    )
else:
    selected_location = "All"

df_display = st.session_state.df.copy()

if selected_location != "All" and not df_display.empty:
    df_display = df_display[df_display["Location"] == selected_location]

# -----------------------------
# CUSTOM CSS FOR CARDS
# -----------------------------
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #f0f2f6;
    border: 1px solid #e0e4eb;
    padding: 5% 5% 5% 10%;
    border-radius: 10px;
    color: #1f1f1f;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}
/* Dark mode compatibility */
@media (prefers-color-scheme: dark) {
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #33343d;
        color: white;
    }
}
.job-card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #e0e4eb;
    transition: transform 0.2s, border 0.2s;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.05);
}
.job-card:hover {
    border: 1px solid #4F8BF9;
    transform: scale(1.01);
}
.job-title {
    margin-top: 0;
    margin-bottom: 5px;
    color: #4F8BF9;
}
.job-detail {
    margin: 3px 0;
    color: #555;
    font-size: 0.95rem;
}
@media (prefers-color-scheme: dark) {
    .job-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
    }
    .job-title {
        color: #4F8BF9;
    }
    .job-detail {
        color: #ddd;
    }
}
</style>
""", unsafe_allow_html=True)

if df_display.empty:
    st.info("No data available. Please fetch real-time data.")
else:
    # -----------------------------
    # KPI METRICS (TOP CARDS)
    # -----------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Jobs", len(df_display))
    col2.metric("🏢 Unique Companies", df_display["Company"].nunique())
    col3.metric("📍 Unique Locations", df_display["Location"].nunique())
    
    st.markdown("---")

    # -----------------------------
    # TABS FOR ORGANIZATION
    # -----------------------------
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🛠 Skills & Salary", "📄 Job Listings"])

    with tab1:
        st.subheader("Market Overview")
        colA, colB = st.columns(2)
        
        with colA:
            st.markdown("**Top Companies Hiring**")
            st.bar_chart(df_display["Company"].value_counts().head(10))
            
        with colB:
            st.markdown("**Top Locations**")
            st.bar_chart(df_display["Location"].value_counts().head(10))

    with tab2:
        # SKILLS ANALYSIS
        st.subheader("Skills Analysis")
        valid_skills = [
            s for s in df_display["skills"]
            if pd.notna(s) and s != "Not Specified"
        ]

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
                fig, ax = plt.subplots()
                ax.pie(skills_df["Count"].head(7), labels=skills_df["Skill"].head(7), autopct="%1.1f%%")
                st.pyplot(fig)
        else:
            st.info("No skills data available.")

        # SALARY ANALYSIS
        st.markdown("---")
        st.subheader("💰 Salary Insights")
        salary_df = df_display[df_display["salary"] > 0]

        if not salary_df.empty:
            sal_col1, sal_col2 = st.columns(2)
            sal_col1.metric("Average Salary", f"₹{salary_df['salary'].mean():,.0f}")
            sal_col2.metric("Max Salary", f"₹{salary_df['salary'].max():,.0f}")

            st.markdown("**Salaries by Company**")
            st.bar_chart(salary_df[["Company", "salary"]].set_index("Company").head(15))
        else:
            st.info("No salary data available.")

    with tab3:
        st.subheader("Job Listings")
        
        # Render Job Cards
        cards_html = ""
        for _, row in df_display.iterrows():
            salary_text = f"₹{row['salary']:,.0f}" if row['salary'] > 0 else "Not Disclosed"
            cards_html += f"""
            <div class="job-card">
                <h3 class="job-title">{row['Title']}</h3>
                <p class="job-detail">🏢 <strong>Company:</strong> {row['Company']}</p>
                <p class="job-detail">📍 <strong>Location:</strong> {row['Location']}</p>
                <p class="job-detail">🛠 <strong>Skills:</strong> {row['skills']}</p>
                <p class="job-detail">💰 <strong>Salary:</strong> {salary_text}</p>
            </div>
            """
        st.markdown(cards_html, unsafe_allow_html=True)
        
        # DOWNLOAD
        st.markdown("<br>", unsafe_allow_html=True)
        csv = df_display.to_csv(index=False)
        st.download_button("📥 Download Full Data as CSV", csv, "jobs.csv", "text/csv")