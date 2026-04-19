# Job Salary Dataset — ETL Pipeline -1 -1

ETL pipeline built with **PySpark**, **Pydantic**, and **SQLAlchemy** to process a dataset of 250,000 job salary records.

## Pipeline

- **Extract** — reads `data/raw/job_salary_dataset.csv` via PySpark with inferred schema
- **Validate** — each row is validated through a Pydantic `Job` model with enums (`CompanySizes`, `RemoteWorks`) and field constraints (salary: 1,000–200,000; experience: 0–50 years)
- **Load** — valid records are persisted to a relational database via SQLAlchemy

## Dataset fields

`job_title`, `experience_years`, `education_level`, `skills_count`, `industry`, `company_size`, `location`, `remote_work`, `certifications`, `salary`

## Setup

```bash
cp .env.example .env  # set DATABASE_ADDRESS, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
```
