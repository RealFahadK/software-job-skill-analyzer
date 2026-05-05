# Final Report: Software Engineering Job Market Skill Analyzer

# 1. Problem Definition & Background

Software engineering students need to decide which technical skills to learn, but job market information is scattered across many postings and platforms. This project builds a database backed analysis system that organizes software engineering job postings and identifies common technical skills.

# 2. Data & Methodology

The dataset contains 9,380 software engineering job postings with fields such as job title, company, job location, first seen date, job level, job type, job summary, and job skills.

The project uses a Python ETL pipeline to clean the CSV file, remove duplicates, handle missing fields, normalize skill names, categorize job roles, and load the cleaned data into a relational SQLite database.

The database schema includes companies, locations, jobs, skills, and job_skills. The job_skills table represents a many to many relationship between job postings and technical skills.

# 3. Results & Analysis

- Top technical skills
- Role distribution
- Top companies
- Top locations
- Top skills by role

## 4. Discussion & Limitations

This project provides useful evidence about software engineering skill demand, but it has limitations. The dataset may not represent every job posting in the market, job postings may include repeated or incomplete information, and rule based skill normalization may miss some skills.

## 5. Conclusion

The project demonstrates how data management methods can transform raw job postings into structured insights. It uses data cleaning, relational database design, SQL queries, Python analysis, visualization, and an interactive dashboard to help students understand software engineering skill demand.
