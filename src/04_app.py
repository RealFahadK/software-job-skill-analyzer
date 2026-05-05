import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DB_PATH = "database/jobs.db"

st.set_page_config(page_title="Software Engineering Skill Analyzer", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    jobs = pd.read_sql_query("""
        SELECT
            j.id,
            j.job_title,
            c.company_name,
            l.job_location,
            j.first_seen,
            j.search_city,
            j.search_country,
            j.job_level,
            j.job_type,
            j.role_category,
            j.skill_count
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        JOIN locations l ON j.location_id = l.id
    """, conn)

    skills = pd.read_sql_query("""
        SELECT
            j.id AS job_id,
            j.role_category,
            s.skill_name
        FROM jobs j
        JOIN job_skills js ON j.id = js.job_id
        JOIN skills s ON js.skill_id = s.id
    """, conn)

    conn.close()
    return jobs, skills

def bar_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)
    ax.set_xlabel(x_col.replace("_", " ").title())
    ax.set_ylabel(y_col.replace("_", " ").title())
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

jobs, skills = load_data()

st.title("Software Engineering Job Market Skill Analyzer")
st.write(
    "This dashboard analyzes software engineering job postings to identify common skills, "
    "role categories, companies, and locations."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Job Postings", len(jobs))
col2.metric("Companies", jobs["company_name"].nunique())
col3.metric("Locations", jobs["job_location"].nunique())
col4.metric("Unique Skills", skills["skill_name"].nunique())

role_options = ["All"] + sorted(jobs["role_category"].dropna().unique().tolist())
selected_role = st.sidebar.selectbox("Filter by role category", role_options)

if selected_role != "All":
    filtered_jobs = jobs[jobs["role_category"] == selected_role]
    filtered_skills = skills[skills["role_category"] == selected_role]
else:
    filtered_jobs = jobs
    filtered_skills = skills

st.subheader("Top Technical Skills")
top_skills = (
    filtered_skills["skill_name"]
    .value_counts()
    .head(15)
    .reset_index()
)
top_skills.columns = ["skill_name", "posting_count"]
st.pyplot(bar_chart(top_skills, "skill_name", "posting_count", "Top Skills"))

st.subheader("Role Category Distribution")
role_counts = (
    jobs["role_category"]
    .value_counts()
    .reset_index()
)
role_counts.columns = ["role_category", "posting_count"]
st.pyplot(bar_chart(role_counts, "role_category", "posting_count", "Postings by Role Category"))

left, right = st.columns(2)

with left:
    st.subheader("Top Companies")
    top_companies = (
        filtered_jobs["company_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_companies.columns = ["company_name", "posting_count"]
    st.dataframe(top_companies, use_container_width=True)

with right:
    st.subheader("Top Locations")
    top_locations = (
        filtered_jobs["job_location"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_locations.columns = ["job_location", "posting_count"]
    st.dataframe(top_locations, use_container_width=True)

st.subheader("Sample Job Postings")
st.dataframe(
    filtered_jobs[["job_title", "company_name", "job_location", "job_level", "job_type", "role_category", "skill_count"]].head(50),
    use_container_width=True
)

st.subheader("Conclusion")
st.write(
    "The cleaned dataset and database-backed analysis show which technical skills appear most often "
    "in software engineering job postings. This helps students prioritize skills based on real job-market data."
)
