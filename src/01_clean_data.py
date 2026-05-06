import os
import re
import pandas as pd

RAW_PATH = "data/raw_jobs.csv"
CLEAN_PATH = "data/cleaned_jobs.csv"

SKILL_NORMALIZATION = {
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "python": "Python",
    "java": "Java",
    "c#": "C#",
    "c++": "C++",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "react": "React",
    "react.js": "React",
    "node": "Node.js",
    "node.js": "Node.js",
    "angular": "Angular",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "git": "Git",
    "github": "GitHub",
    "linux": "Linux",
    "html": "HTML/CSS",
    "css": "HTML/CSS",
    "html/css": "HTML/CSS",
    ".net": ".NET",
    "asp.net": "ASP.NET",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "django": "Django",
    "flask": "Flask",
    "rest": "REST API",
    "rest api": "REST API",
    "api": "API",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "scala": "Scala",
    "go": "Go",
    "golang": "Go",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence"
}

COMMON_SKILLS = sorted(set(SKILL_NORMALIZATION.values()))

def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

def normalize_skill(skill):
    raw = clean_text(skill)
    if not raw:
        return None
    lowered = raw.lower().strip()
    return SKILL_NORMALIZATION.get(lowered, raw.strip())

def split_and_normalize_skills(skill_string):
    if pd.isna(skill_string) or str(skill_string).strip() == "":
        return []
    pieces = re.split(r",|;|\||/", str(skill_string))
    normalized = []
    for piece in pieces:
        skill = normalize_skill(piece)
        if skill and len(skill) <= 40:
            normalized.append(skill)
    return sorted(set(normalized))

def categorize_role(title):
    title = str(title).lower()
    if "front end" in title or "frontend" in title or "front-end" in title:
        return "Frontend"
    if "back end" in title or "backend" in title or "back-end" in title:
        return "Backend"
    if "full stack" in title or "fullstack" in title or "full-stack" in title:
        return "Full-Stack"
    if "data" in title:
        return "Data"
    if "machine learning" in title or "ml " in title or "ai " in title:
        return "AI/ML"
    if "devops" in title or "cloud" in title or "site reliability" in title or "sre" in title:
        return "DevOps/Cloud"
    if "mobile" in title or "ios" in title or "android" in title:
        return "Mobile"
    if "software" in title or "developer" in title or "engineer" in title:
        return "General Software"
    return "Other"

def main():
    os.makedirs("data", exist_ok=True)

    df = pd.read_csv(RAW_PATH)
    print(f"Raw rows: {len(df)}")
    print(f"Raw columns: {list(df.columns)}")

    df = df.rename(columns={
        "job level": "job_level"
    })

    for col in df.columns:
        df[col] = df[col].apply(clean_text)

    if "job_link" in df.columns:
        df = df.drop_duplicates(subset=["job_link"])
    df = df.drop_duplicates(subset=["job_title", "company", "job_location", "job_summary"])

    df["job_summary"] = df["job_summary"].fillna("")
    df["job_skills"] = df["job_skills"].fillna("")

    df["first_seen"] = pd.to_datetime(df["first_seen"], errors="coerce").dt.date.astype(str)

    df["role_category"] = df["job_title"].apply(categorize_role)

    df["normalized_skills"] = df["job_skills"].apply(lambda x: "|".join(split_and_normalize_skills(x)))
    df["skill_count"] = df["normalized_skills"].apply(lambda x: 0 if x == "" else len(x.split("|")))

    keep_cols = [
        "job_title", "company", "job_location", "job_link", "first_seen",
        "search_city", "search_country", "job_level", "job_type",
        "job_summary", "job_skills", "role_category", "normalized_skills", "skill_count"
    ]
    df = df[keep_cols]

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Cleaned rows: {len(df)}")
    print(f"Saved cleaned data to {CLEAN_PATH}")
    print(df[["job_title", "company", "role_category", "normalized_skills"]].head())

if __name__ == "__main__":
    main()
