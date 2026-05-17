import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------------
# LOAD CSV
# -----------------------------

df = pd.read_csv("jobs.csv")

print(df.head())

# -----------------------------
# SKILL ANALYSIS
# -----------------------------

# Dummy skills column add kar rahe hain
df["skills"] = [
    "SQL,Excel,Power BI",
    "Python,SQL,Tableau",
    "Python,ML,SQL",
    "Excel,SQL,Power BI"
] * 25

# combine all skills
all_skills = ",".join(df["skills"])

# split into list
skills_list = [skill.strip() for skill in all_skills.split(",")]

# count frequency
skill_counts = Counter(skills_list)

print("\nTop Skills in Demand:")

print(skill_counts)

# -----------------------------
# SKILL CHART
# -----------------------------

skills = list(skill_counts.keys())

counts = list(skill_counts.values())

plt.figure(figsize=(8,5))

plt.bar(skills, counts)

plt.title("Top Skills in Job Market")

plt.xlabel("Skills")

plt.ylabel("Demand")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# -----------------------------
# SALARY ANALYSIS
# -----------------------------

# Dummy salary column
df["salary"] = [
    600000,
    700000,
    1200000,
    800000
] * 25

# Average salary
avg_salary = df["salary"].mean()

print("\nAverage Salary:", avg_salary)

# Highest salary
max_salary = df["salary"].max()

print("Highest Salary:", max_salary)

# -----------------------------
# SALARY CHART
# -----------------------------

plt.figure(figsize=(8,5))

df["salary"].plot(kind="hist", bins=5)

plt.title("Salary Distribution")

plt.xlabel("Salary")

plt.ylabel("Frequency")

plt.tight_layout()

plt.show()