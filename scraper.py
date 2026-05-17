import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.find_all("div", class_="card-content")

data = []

for job in jobs:

    title = job.find("h2").text.strip()

    company = job.find("h3").text.strip()

    location = job.find("p", class_="location").text.strip()

    data.append([title, company, location])

df = pd.DataFrame(data, columns=["Title", "Company", "Location"])

df.to_csv("jobs.csv", index=False)

print("Data Saved Successfully ✅")