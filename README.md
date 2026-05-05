# Software Engineering Job Market Skill Analyzer

This project analyzes software engineering job postings to identify common technical skills, role categories, locations, companies, and hiring patterns.

# Project Overview

The system uses a CSV job posting dataset, cleans the data with Python, loads it into a relational SQLite database, runs SQL/Python analysis, generates visualizations, and provides an interactive Streamlit dashboard.

# Dataset

Input file: `data/raw_jobs.csv`

Important columns:
- `job_title`
- `company`
- `job_location`
- `first_seen`
- `search_city`
- `search_country`
- `job level`
- `job_type`
- `job_summary`
- `job_skills`

# Database Design

The SQLite database uses normalized relational tables:

- `companies`
- `locations`
- `jobs`
- `skills`
- `job_skills`

The `job_skills` table is a bridge table that represents the many to many relationship between jobs and skills.

# How to Run

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Clean the dataset

```bash
python src/01_clean_data.py
```

### 4. Build the database

```bash
python src/02_build_database.py
```

### 5. Run analysis and generate charts

```bash
python src/03_analysis.py
```

### 6. Run the dashboard

```bash
streamlit run src/04_app.py
```

# Main Research Questions

1. Which technical skills appear most often in software engineering job postings?
2. Which skills are most common across backend, frontend, full stack, data, and general software roles?
3. Which companies and locations appear most frequently in the dataset?
4. How can cleaned job posting data help students make evidence-based decisions about which technical skills to learn?

# Outputs

Generated files:
- `data/cleaned_jobs.csv`
- `database/jobs.db`
- `outputs/top_skills.png`
- `outputs/role_distribution.png`
- `outputs/top_companies.png`
- `outputs/top_locations.png`
- `outputs/top_skills_by_role.csv`

# Tools Used

- Python
- Pandas
- SQLite
- SQL
- Matplotlib
- Streamlit
- GitHub
