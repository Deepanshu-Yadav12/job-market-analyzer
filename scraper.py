import requests
import pandas as pd
import streamlit as st

def fetch_real_jobs(app_id, app_key, query="Data Analyst", location="India", results=50):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results,
        "what": query,
        "where": location
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('results', [])
            
            jobs_list = []
            for job in data:
                title = job.get('title', 'N/A')
                company = job.get('company', {}).get('display_name', 'N/A')
                loc = job.get('location', {}).get('display_name', 'N/A')
                desc = job.get('description', '')
                
                # Extract basic skills from description
                skills_found = []
                desc_lower = desc.lower()
                common_skills = ["python", "sql", "excel", "power bi", "tableau", "aws", "azure", "machine learning", "java", "c++", "react", "node"]
                for skill in common_skills:
                    if skill in desc_lower:
                        # Capitalize properly
                        if skill == "sql": skills_found.append("SQL")
                        elif skill == "aws": skills_found.append("AWS")
                        else: skills_found.append(skill.title())
                        
                skills_str = ",".join(skills_found) if skills_found else "Not Specified"
                
                # Adzuna provides salary estimates
                salary_min = job.get('salary_min')
                salary_max = job.get('salary_max')
                if salary_min and salary_max:
                    salary = (salary_min + salary_max) / 2
                elif salary_min:
                    salary = salary_min
                else:
                    salary = 0 # Default if no salary provided
                    
                jobs_list.append([title, company, loc, skills_str, salary])
                
            df = pd.DataFrame(jobs_list, columns=["Title", "Company", "Location", "skills", "salary"])
            return df
        else:
            st.error(f"API Error {response.status_code}: Please check your App ID and App Key.")
            return pd.DataFrame(columns=["Title", "Company", "Location", "skills", "salary"])
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return pd.DataFrame(columns=["Title", "Company", "Location", "skills", "salary"])