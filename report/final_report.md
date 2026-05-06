# Software Engineering Job Market Skill Analyzer

**Name:** Fahad Khan  
**Course:** CS 210 - Data Management for Data Science  
**NETID:** fak49
**Project Type:** Final Project  

---

## 1. Introduction

For this project, I built a data management system that analyzes software engineering job postings and identifies common technical skills requested by employers. Students preparing for software engineering careers often look at job postings, online advice, and other sources to decide what skills to learn. However, it can be hard to manually compare hundreds or thousands of postings.

The goal of this project was to take job posting data, clean it, organize it into a database, and use it to answer questions about software engineering skills. The project focuses on data management concepts such as data cleaning, transformation, relational database design, SQL queries, and visualizations.

The main question I wanted to answer was:

**Which technical skills appear most often in software engineering job postings?**

I also looked at role categories, companies, and locations to better understand the dataset.

---

## 2. Dataset Description

The dataset used in this project is a software engineering job postings CSV file. It contains 9,380 job postings. Each row represents one job posting.

The dataset includes columns such as:

- job title
- company
- job location
- job link
- first seen date
- search city
- search country
- job level
- job type
- job summary
- job skills

This dataset was useful for the project because it already contained software engineering related job postings and included skill information. That made it possible to focus on cleaning, database design, analysis, and visualization.

---

## 3. Database Design

I used SQLite for the relational database. SQLite was chosen because it is easy to set up and works well for a class project. The database file is stored inside the project folder as `database/jobs.db`.

The database was designed using multiple related tables instead of storing everything in one flat table. The main tables are:

- `companies`
- `locations`
- `jobs`
- `skills`
- `job_skills`

The `jobs` table stores information about each job posting. The `companies` table stores company names. The `locations` table stores job locations. The `skills` table stores normalized skill names. The `job_skills` table connects jobs and skills.

This design is important because a single job can require many skills, and the same skill can appear in many different jobs. This is a many-to-many relationship, so I used the `job_skills` bridge table to represent it.

---

## 4. Data Cleaning and ETL Process

The project uses a Python ETL process. ETL stands for Extract, Transform, and Load.

First, the raw CSV file is loaded from the `data` folder. Then the data is cleaned and transformed. Finally, the cleaned data is loaded into the SQLite database.

Some cleaning steps included:

- removing duplicate rows
- handling missing values
- standardizing job titles
- standardizing company and location fields
- creating role categories
- normalizing skills
- saving a cleaned CSV file

The cleaned dataset is saved as `data/cleaned_jobs.csv`.

The role categories were created from job titles. For example, job titles containing words like “frontend” were categorized as Frontend, while titles containing “backend” were categorized as Backend. Other categories included Full-Stack, Mobile, DevOps/Cloud, Data, AI/ML, and General Software.

---

## 5. Methodology

After cleaning the data and building the database, I used Python and SQL-based analysis to answer the main project questions.

The main analysis questions were:

1. Which technical skills appear most often in software engineering job postings?
2. What are the most common software engineering role categories?
3. Which companies appear most often in the dataset?
4. Which locations appear most often in the dataset?

The project also includes a Streamlit dashboard so the results can be explored visually. The dashboard displays summary numbers, charts, and a sample table of job postings.

---

## 6. Results and Analysis

### Top Technical Skills

The most common technical skill in the dataset was Python, appearing in 3,512 postings. Java was second with 3,144 postings, and JavaScript was third with 2,718 postings.

The top skills found were:

| Skill | Posting Count |
|---|---:|
| Python | 3,512 |
| Java | 3,144 |
| JavaScript | 2,718 |
| AWS | 2,593 |
| SQL | 2,274 |
| Agile | 2,098 |
| C++ | 2,088 |
| Git | 1,810 |
| C# | 1,804 |

These results show that programming languages are still very important in software engineering postings. Python, Java, and JavaScript were the top three skills. SQL also appeared often, which shows that database knowledge is still useful for software engineering roles. AWS was also very common, showing the importance of cloud computing skills.

![Top Skills](screenshots/top_skills.png)

---

### Role Category Distribution

Most of the postings were classified as General Software. This category had 7,224 postings. Full-Stack had 695 postings, Backend had 606 postings, and Frontend had 242 postings.

| Role Category | Posting Count |
|---|---:|
| General Software | 7,224 |
| Full-Stack | 695 |
| Backend | 606 |
| Frontend | 242 |
| Mobile | 177 |
| DevOps/Cloud | 148 |
| Data | 94 |
| AI/ML | 65 |

The General Software category is much larger than the other categories. This happened because many job titles are broad, such as “Software Engineer” or “Software Developer,” and do not clearly say frontend, backend, full-stack, or another specific category.

![Role Distribution](screenshots/role_distribution.png)

---

### Top Companies

The companies with the most postings in the dataset were Jobs for Humanity, Canonical, Recruiting from Scratch, Affirm, and ClearanceJobs.

| Company | Posting Count |
|---|---:|
| Jobs for Humanity | 681 |
| Canonical | 286 |
| Recruiting from Scratch | 195 |
| Affirm | 137 |
| ClearanceJobs | 109 |

This analysis shows which companies or recruiting organizations appeared most often in the dataset. Some of these may be recruiting platforms or organizations posting many jobs, so this should be considered when interpreting the results.

![Top Companies](screenshots/top_companies.png)

---

### Top Locations

The top location was San Francisco, CA, with 133 postings. London was second with 104 postings, and New York, NY was third with 98 postings.

| Location | Posting Count |
|---|---:|
| San Francisco, CA | 133 |
| London, England, United Kingdom | 104 |
| New York, NY | 98 |
| Boston, MA | 80 |
| United States | 78 |
| Austin, TX | 77 |
| San Diego, CA | 76 |
| Chicago, IL | 76 |
| Toronto, Ontario, Canada | 75 |

These results show that many postings are concentrated in major technology and business locations. Some postings only list “United States,” which is less specific. That is a limitation of the dataset.

![Top Locations](screenshots/top_locations.png)

---

## 7. Dashboard and Implementation

I created a Streamlit dashboard to make the results easier to view. The dashboard includes summary metrics, charts, filters, and a table of sample job postings.

The dashboard allows the user to explore the job posting data without manually opening the CSV files or database. It shows the main results in a more visual format.

The project implementation includes:

- Python scripts for cleaning and database building
- SQLite relational database
- generated CSV analysis outputs
- generated PNG charts
- Streamlit dashboard
- README instructions
- GitHub repository

![Dashboard Screenshot](screenshots/dashboard_summary.png)

---

## 8. Limitations

There are some limitations in this project.

First, the dataset may not represent the entire software engineering job market. It only represents the job postings included in the CSV file.

Second, some job postings may be duplicated or posted by recruiting companies instead of direct employers.

Third, the role categorization is based on keywords in job titles. This means some jobs may be placed in General Software even if the job description is actually more specific.

Fourth, skill extraction depends on the skill data available in the dataset and the cleaning process. Some skills may be missed if they are written in an unusual way.

Finally, the project uses SQLite instead of PostgreSQL. SQLite is still a relational database and works well for this project, but PostgreSQL would be better for a larger production-level system.

---

## 9. Conclusion

This project created a database-backed system for analyzing software engineering job postings. The system cleaned the data, organized it into relational tables, generated analysis outputs, and displayed the results through charts and a Streamlit dashboard.

The results showed that Python, Java, JavaScript, AWS, and SQL were among the most common skills in the dataset. This suggests that students preparing for software engineering careers should pay attention to programming languages, databases, cloud platforms, and version control tools.

Overall, this project helped me practice important data management skills, including cleaning real-world data, designing a relational schema, writing Python scripts, using a database, generating analysis results, and communicating findings through visualizations.

---

## 10. Statement of Contributions

I worked individually on this project. I was responsible for selecting the dataset, cleaning and preparing the data, designing the relational database structure, writing the Python ETL scripts, generating analysis results, creating visualizations, building the Streamlit dashboard, writing the README instructions, and preparing the final report and demo materials.

---

## 11. References

Dataset: LinkedIn software engineering job postings dataset used from the provided CSV file.

Tools used:
- Python
- pandas
- SQLite
- matplotlib
- Streamlit
- VS Code
- GitHub