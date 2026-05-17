import streamlit as st
import pandas as pd
from collections import Counter

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("indian_jobs.csv")

# -----------------------------
# ADD LOCATIONS
# -----------------------------
locations = [
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Mumbai",
    "Delhi"
]

df["Location"] = [
    locations[i % len(locations)]
    for i in range(len(df))
]
# -----------------------------
# ADD SKILLS
# -----------------------------

skills_data = [
    "SQL,Python,Excel",
    "Power BI,SQL,Excel",
    "Python,Machine Learning,SQL",
    "Tableau,Excel,SQL"
]

df["skills"] = [
    skills_data[i % len(skills_data)]
    for i in range(len(df))
]
# -----------------------------
# ADD SALARY
# -----------------------------
salary_data = [
    400000,
    500000,
    700000,
    900000
]

df["salary"] = [
    salary_data[i % len(salary_data)]
    for i in range(len(df))
]
# -----------------------------
# TITLE
# -----------------------------

st.title("📊 Job Market Analyzer")

st.write("Analyze Indian job trends, skills, and salaries.")

# -----------------------------
# SHOW DATA
# -----------------------------

st.subheader("Job Listings")

# -----------------------------
# SEARCH BOX
# -----------------------------

search = st.text_input(
    "Search Job Title or Company"
)

if search:

    filtered_df = df[
        df["Title"].str.contains(search, case=False)
        |
        df["Company"].str.contains(search, case=False)
    ]

    st.dataframe(filtered_df)

else:

    st.dataframe(df)
    # -----------------------------
# DOWNLOAD BUTTON
# -----------------------------

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="job_data.csv",
    mime="text/csv"
)
# -----------------------------
# TOP COMPANIES
# -----------------------------

st.subheader("🏢 Top Hiring Companies")

company_counts = df["Company"].value_counts()

st.bar_chart(company_counts)

# -----------------------------
# TOP LOCATIONS
# -----------------------------

st.subheader("📍 Top Hiring Locations")

location_counts = df["Location"].value_counts()

st.bar_chart(location_counts)

# -----------------------------
# SKILL ANALYSIS
# -----------------------------

st.subheader("🛠 Top Skills in Demand")

all_skills = ",".join(df["skills"])

skills_list = [skill.strip() for skill in all_skills.split(",")]

skill_counts = Counter(skills_list)

skills_df = pd.DataFrame({
    "Skill": list(skill_counts.keys()),
    "Demand": list(skill_counts.values())
})

st.bar_chart(skills_df.set_index("Skill"))
# -----------------------------
# PIE CHART
# -----------------------------

st.subheader("📊 Skills Distribution")

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.pie(
    skills_df["Demand"],
    labels=skills_df["Skill"],
    autopct="%1.1f%%"
)

st.pyplot(fig)

# -----------------------------
# SALARY ANALYSIS
# -----------------------------

st.subheader("💰 Salary Analysis")

avg_salary = df["salary"].mean()

max_salary = df["salary"].max()

st.metric("Average Salary", f"₹{avg_salary:,.0f}")

st.metric("Highest Salary", f"₹{max_salary:,.0f}")

st.bar_chart(df["salary"])

st.write("Analyze Indian job trends, skills, and salaries.")
# -----------------------------
# KPI METRICS
# -----------------------------

st.subheader("📈 Project Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Jobs",
    len(df)
)

col2.metric(
    "Companies Hiring",
    df["Company"].nunique()
)

col3.metric(
    "Locations",
    df["Location"].nunique()
)
# -----------------------------
# SIDEBAR FILTER
# -----------------------------

st.sidebar.title("Filters")

selected_location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + list(df["Location"].unique())
)

if selected_location != "All":
    df = df[df["Location"] == selected_location]