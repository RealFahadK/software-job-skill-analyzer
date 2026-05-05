import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "database/jobs.db"
OUTPUT_DIR = "outputs"

def save_bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename, rotation=45):
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col], df[y_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"Saved {path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    top_skills = pd.read_sql_query("""
        SELECT s.skill_name, COUNT(*) AS posting_count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.id
        GROUP BY s.skill_name
        ORDER BY posting_count DESC
        LIMIT 15;
    """, conn)

    role_distribution = pd.read_sql_query("""
        SELECT role_category, COUNT(*) AS posting_count
        FROM jobs
        GROUP BY role_category
        ORDER BY posting_count DESC;
    """, conn)

    top_companies = pd.read_sql_query("""
        SELECT c.company_name, COUNT(*) AS posting_count
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        GROUP BY c.company_name
        ORDER BY posting_count DESC
        LIMIT 10;
    """, conn)

    top_locations = pd.read_sql_query("""
        SELECT l.job_location, COUNT(*) AS posting_count
        FROM jobs j
        JOIN locations l ON j.location_id = l.id
        GROUP BY l.job_location
        ORDER BY posting_count DESC
        LIMIT 10;
    """, conn)

    top_skills_by_role = pd.read_sql_query("""
        SELECT role_category, skill_name, posting_count
        FROM (
            SELECT
                j.role_category,
                s.skill_name,
                COUNT(*) AS posting_count,
                ROW_NUMBER() OVER (
                    PARTITION BY j.role_category
                    ORDER BY COUNT(*) DESC
                ) AS rn
            FROM jobs j
            JOIN job_skills js ON j.id = js.job_id
            JOIN skills s ON js.skill_id = s.id
            GROUP BY j.role_category, s.skill_name
        )
        WHERE rn <= 5
        ORDER BY role_category, posting_count DESC;
    """, conn)

    top_skills.to_csv(os.path.join(OUTPUT_DIR, "top_skills.csv"), index=False)
    role_distribution.to_csv(os.path.join(OUTPUT_DIR, "role_distribution.csv"), index=False)
    top_companies.to_csv(os.path.join(OUTPUT_DIR, "top_companies.csv"), index=False)
    top_locations.to_csv(os.path.join(OUTPUT_DIR, "top_locations.csv"), index=False)
    top_skills_by_role.to_csv(os.path.join(OUTPUT_DIR, "top_skills_by_role.csv"), index=False)

    save_bar_chart(
        top_skills, "skill_name", "posting_count",
        "Top Technical Skills in Software Engineering Job Postings",
        "Skill", "Number of Postings", "top_skills.png"
    )

    save_bar_chart(
        role_distribution, "role_category", "posting_count",
        "Software Engineering Postings by Role Category",
        "Role Category", "Number of Postings", "role_distribution.png"
    )

    save_bar_chart(
        top_companies, "company_name", "posting_count",
        "Top Companies by Number of Job Postings",
        "Company", "Number of Postings", "top_companies.png"
    )

    save_bar_chart(
        top_locations, "job_location", "posting_count",
        "Top Job Locations",
        "Location", "Number of Postings", "top_locations.png"
    )

    print("\nTop skills:")
    print(top_skills)

    print("\nTop skills by role:")
    print(top_skills_by_role)

    conn.close()

if __name__ == "__main__":
    main()
