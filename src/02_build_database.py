import os
import sqlite3
import pandas as pd

CLEAN_PATH = "data/cleaned_jobs.csv"
DB_PATH = "database/jobs.db"

def get_or_create(cursor, table, column, value):
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
    return cursor.lastrowid

def main():
    os.makedirs("database", exist_ok=True)

    df = pd.read_csv(CLEAN_PATH).fillna("")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS job_skills;
    DROP TABLE IF EXISTS jobs;
    DROP TABLE IF EXISTS skills;
    DROP TABLE IF EXISTS companies;
    DROP TABLE IF EXISTS locations;

    CREATE TABLE companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_location TEXT UNIQUE NOT NULL
    );

    CREATE TABLE skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT NOT NULL,
        company_id INTEGER,
        location_id INTEGER,
        job_link TEXT,
        first_seen TEXT,
        search_city TEXT,
        search_country TEXT,
        job_level TEXT,
        job_type TEXT,
        job_summary TEXT,
        role_category TEXT,
        skill_count INTEGER,
        FOREIGN KEY (company_id) REFERENCES companies(id),
        FOREIGN KEY (location_id) REFERENCES locations(id)
    );

    CREATE TABLE job_skills (
        job_id INTEGER,
        skill_id INTEGER,
        PRIMARY KEY (job_id, skill_id),
        FOREIGN KEY (job_id) REFERENCES jobs(id),
        FOREIGN KEY (skill_id) REFERENCES skills(id)
    );
    """)

    for _, row in df.iterrows():
        company_id = get_or_create(cur, "companies", "company_name", row["company"])
        location_id = get_or_create(cur, "locations", "job_location", row["job_location"])

        cur.execute("""
            INSERT INTO jobs (
                job_title, company_id, location_id, job_link, first_seen,
                search_city, search_country, job_level, job_type, job_summary,
                role_category, skill_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["job_title"], company_id, location_id, row["job_link"], row["first_seen"],
            row["search_city"], row["search_country"], row["job_level"], row["job_type"],
            row["job_summary"], row["role_category"], int(row["skill_count"])
        ))

        job_id = cur.lastrowid

        skills = [s for s in str(row["normalized_skills"]).split("|") if s.strip()]
        for skill in skills:
            skill_id = get_or_create(cur, "skills", "skill_name", skill)
            cur.execute("""
                INSERT OR IGNORE INTO job_skills (job_id, skill_id)
                VALUES (?, ?)
            """, (job_id, skill_id))

    conn.commit()

    # Print table counts for documentation/report.
    for table in ["companies", "locations", "skills", "jobs", "job_skills"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]} rows")

    conn.close()
    print(f"Database saved to {DB_PATH}")

if __name__ == "__main__":
    main()
