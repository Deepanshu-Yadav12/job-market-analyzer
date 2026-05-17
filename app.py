import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

from scraper import fetch_real_jobs


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Job Market Analyzer", layout="wide")

st.title("📊 Job Market Analyzer")
st.write("Analyze job trends, skills, and salaries using real-time API data.")

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if 'df' not in st.session_state:
    try:
        # Load static fallback data
        fallback_df = pd.read_csv("indian_jobs.csv")
        # Add missing columns if needed for backward compatibility
        locations = ["Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi"]
        if "Location" not in fallback_df.columns:
            fallback_df["Location"] = [locations[i % len(locations)] for i in range(len(fallback_df))]
        
        if "skills" not in fallback_df.columns:
            skills_data = ["SQL,Python,Excel", "Power BI,SQL,Excel", "Python,Machine Learning,SQL", "Tableau,Excel,SQL"]
            fallback_df["skills"] = [skills_data[i % len(skills_data)] for i in range(len(fallback_df))]
        
        if "salary" not in fallback_df.columns:
            salary_data = [400000, 500000, 700000, 900000]
            fallback_df["salary"] = [salary_data[i % len(salary_data)] for i in range(len(fallback_df))]
            
        st.session_state.df = fallback_df
    except FileNotFoundError:
        st.session_state.df = pd.DataFrame(columns=["Title", "Company", "Location", "skills", "salary"])

# -----------------------------
# SIDEBAR CONFIG & FILTERS
# -----------------------------
st.sidebar.header("⚙️ API Configuration")
st.sidebar.markdown("**Adzuna API Credentials** ([Get Free Key](https://developer.adzuna.com/))")
app_id = st.sidebar.text_input("App ID", value="8a8de657", type="password")
app_key = st.sidebar.text_input("App Key", value="82c19ad1b7cd6b44a70c50ed3343e805", type="password")

st.sidebar.header("🔍 Search Jobs")
job_query = st.sidebar.text_input("Job Title", "Data Analyst")
job_location = st.sidebar.text_input("Location", "India")
num_results = st.sidebar.slider("Number of Results", 10, 100, 50)

if st.sidebar.button("Fetch Real-Time Data"):
    if not app_id or not app_key:
        st.sidebar.error("Please enter both App ID and App Key.")
    else:
        with st.spinner("Fetching data from Adzuna API..."):
            new_df = fetch_real_jobs(app_id, app_key, query=job_query, location=job_location, results=num_results)
            if not new_df.empty:
                st.session_state.df = new_df
                st.sidebar.success("Data fetched successfully!")
            else:
                st.sidebar.warning("No data found or API error.")

st.sidebar.header("📂 Filters")
selected_location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + list(st.session_state.df["Location"].unique()) if not st.session_state.df.empty else ["All"]
)

# Apply filter
df_display = st.session_state.df.copy()
if selected_location != "All" and not df_display.empty:
    df_display = df_display[df_display["Location"] == selected_location]


# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📄 Job Listings")
st.dataframe(df_display)


# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
if not df_display.empty:
    csv = df_display.to_csv(index=False)
    st.download_button(
        "📥 Download Data",
        csv,
        "jobs.csv",
        "text/csv"
    )

if df_display.empty:
    st.info("No data to analyze. Please fetch real-time data or ensure your fallback data exists.")
else:
    # -----------------------------
    # TOP COMPANIES
    # -----------------------------
    st.subheader("🏢 Top Companies")
    st.bar_chart(df_display["Company"].value_counts().head(15))


    # -----------------------------
    # TOP LOCATIONS
    # -----------------------------
    st.subheader("📍 Top Locations")
    st.bar_chart(df_display["Location"].value_counts().head(15))


    # -----------------------------
    # SKILLS ANALYSIS
    # -----------------------------
    st.subheader("🛠 Skills Analysis")
    
    # Filter out 'Not Specified'
    valid_skills = [s for s in df_display["skills"] if s != "Not Specified" and pd.notna(s)]
    if valid_skills:
        all_skills = ",".join(valid_skills)
        skills_list = [s.strip() for s in all_skills.split(",") if s.strip()]
        
        if skills_list:
            skill_counts = Counter(skills_list)
            
            skills_df = pd.DataFrame({
                "Skill": list(skill_counts.keys()),
                "Count": list(skill_counts.values())
            }).sort_values(by="Count", ascending=False)
            
            st.bar_chart(skills_df.set_index("Skill"))
            
            # -----------------------------
            # PIE CHART
            # -----------------------------
            st.subheader("📊 Skills Distribution")
            
            fig, ax = plt.subplots()
            ax.pie(
                skills_df["Count"],
                labels=skills_df["Skill"],
                autopct="%1.1f%%"
            )
            
            st.pyplot(fig)
        else:
            st.write("No skills data available.")
    else:
        st.write("No skills data available.")


    # -----------------------------
    # SALARY ANALYSIS
    # -----------------------------
    st.subheader("💰 Salary Insights")
    
    # Filter out 0 salaries for better metrics
    salary_df = df_display[df_display["salary"] > 0]
    
    if not salary_df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Average Salary (Est.)", f"₹{salary_df['salary'].mean():,.0f}")
        col2.metric("Max Salary", f"₹{salary_df['salary'].max():,.0f}")
        
        # Plot top salaries
        st.bar_chart(salary_df[["Company", "salary"]].set_index("Company").head(20))
    else:
        st.write("No salary data available in the current dataset.")


    # -----------------------------
    # KPI METRICS
    # -----------------------------
    st.subheader("📊 KPIs")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Jobs", len(df_display))
    col2.metric("Companies", df_display["Company"].nunique())
    col3.metric("Locations", df_display["Location"].nunique())