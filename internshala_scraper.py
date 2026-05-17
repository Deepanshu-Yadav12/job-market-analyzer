from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# -----------------------------
# OPEN CHROME
# -----------------------------

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# -----------------------------
# OPEN INTERNSHALA PAGE
# -----------------------------

url = "https://internshala.com/jobs/data-analyst-jobs/"

driver.get(url)

# Wait for page to load
time.sleep(5)

# -----------------------------
# FIND JOB CARDS
# -----------------------------

jobs = driver.find_elements(
    By.CLASS_NAME,
    "internship_meta"
)

# -----------------------------
# STORE DATA
# -----------------------------

data = []

for job in jobs:

    try:

        title = job.find_element(
            By.CLASS_NAME,
            "job-title-href"
        ).text

        company = job.find_element(
            By.CLASS_NAME,
            "company-name"
        ).text

        # Skip empty rows
        if (
            title.strip() != ""
            and company.strip() != ""
            and title != "Actively hiring"
        ):

            data.append([
                title,
                company
            ])

            print(title, "-", company)

    except:
        pass

# -----------------------------
# SAVE CSV
# -----------------------------

df = pd.DataFrame(
    data,
    columns=["Title", "Company"]
)

print("\n")
print(df.head())

df.to_csv(
    "indian_jobs.csv",
    index=False
)

print("\nIndian Job Data Saved Successfully ✅")

# -----------------------------
# CLOSE BROWSER
# -----------------------------

driver.quit()