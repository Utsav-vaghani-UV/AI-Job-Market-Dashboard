
# 🧠 AI Job Market Analysis Dashboard

This is a fully interactive data dashboard created as part of the **Structured Labs Software Engineering Assessment**. Built entirely using the **Preswald framework**, the app explores key trends and insights from a comprehensive dataset of global AI job listings, providing employers, candidates, and data enthusiasts a dynamic lens into the future of the AI job market in 2024–2025.

---

## 📦 Dataset Overview

- **Source**: [Kaggle - Global AI Job Market and Salary Trends (2025)](https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025)
- **File Used**: `ai_job_dataset.csv`
- **Size**: 15,000+ job postings
- **Date Range**: Late 2024 to mid-2025
- **Key Fields**:
  - `job_title`, `salary_usd`, `experience_level`, `remote_ratio`, `company_location`, `education_required`, `required_skills`, `industry`, `years_experience`, `company_size`, `job_description_length`, etc.

---

## 🎯 Project Goals

- Build a responsive, interactive dashboard using **Preswald** 
- Provide deep insights into salary distributions, experience levels, skills, locations, and hiring trends
- Utilize diverse types of visualizations for maximum interpretability
- Deliver a clean, readable codebase with real-time controls and filters

---

## 🚀 Key Features & Visuals

### 🎚️ Salary Filter
- Interactive slider for salary thresholds
- Real-time updates to job listings and histograms

### 📊 Salary & Role Analysis
- **Heatmap** of avg salary by job title × company location
- **Boxplots** and **violin plots** for salary distributions
- **Bar charts** for experience level by country
- **Grouped bar** for average salary by experience level and country

### ⏳ Time & Seasonality
- Time series of average salary over posting years by experience level
- Line plot showing monthly hiring trends (seasonality)

### 🧠 Skills Analysis
- Top 15 most frequently required skills
- Average salary comparison for jobs listing each skill
- Exploded skills column for granular breakdown

### 🏢 Employer Insights
- Top 5 companies by average salary
- Company size vs salary (boxplot)
- Employment type distribution (pie chart)

### 🌍 Global Salary Overview
- Choropleth map of average salaries by country (top 30)
- Regional and global economic comparisons

### 📌 Specific Insights
- Static view: Data Scientist roles in 2024
- Job description length vs salary correlation
- Years of experience vs salary (with trendline)
- Time from posting to application deadline (histogram)

### 📋 Statistical Summary
- Count, mean, median, std dev, and salary quartiles
- Summary printed at the bottom for at-a-glance reference

---

## 🗂️ Project Structure

```
my_assessment_app/
├── data/
│   └── ai_job_dataset.csv        # Dataset file
├── hello.py                      # Core dashboard code
├── preswald.toml                 # Dataset configuration
└── README.md                     # Documentation (this file)
```

---

## ⚙️ Setup Instructions

To run this dashboard locally, follow the steps below.

### ✅ 1. Create a Virtual Environment

```bash
python -m venv venv
```

### ▶️ 2. Activate the Environment (Windows)

```bash
venv\Scripts\activate
```

### 📦 3. Install Dependencies

```bash
pip install duckdb --prefer-binary
pip install preswald
$env:PYTHONUTF8="1"
```

### 🏗️ 4. Run Preswald App

```bash

cd my_assessment_app
preswald run
```

Visit your app at: [http://localhost:8000](http://localhost:8000)

> 📌 Be sure the file `ai_job_dataset.csv` is saved inside the `data/` folder.  
> Also, update the dataset name in `preswald.toml` like:
>
> ```toml
> [sources]
> ai_job_dataset_csv = "data/ai_job_dataset.csv"
> ```

---

## 🙋 About the Author

**Utsav Vaghani**  
M.S. in Computer Science, Governors State University
Email: waghaniutsav6608@gmail.com

---

## ⭐ Acknowledgments

- Thanks to **Structured Labs** for this unique opportunity.
- Framework powered by [Preswald](https://github.com/StructuredLabs/preswald) — don't forget to star it!


---

## ✅ Submission Checklist

- [x] Uses only Preswald (no external UI libraries)
- [x] Fully interactive dashboard
- [x] Real-time filters and dynamic charts
- [x] Diverse, relevant insights from every major column in the dataset
- [x] Clean and documented code
- [x] README with instructions, credits, and project summary

---
