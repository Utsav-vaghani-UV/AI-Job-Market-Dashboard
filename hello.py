import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from collections import Counter
import re

from preswald import connect, get_df, text, plotly, slider, table

# ====== 🔌 Setup & Load Dataset ======
connect()
df = get_df("ai_job_dataset_csv")

# Data Cleanup
df['salary_usd'] = pd.to_numeric(df['salary_usd'], errors='coerce')
df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
df['application_deadline'] = pd.to_datetime(df['application_deadline'], errors='coerce')
df['posting_year'] = df['posting_date'].dt.year
df['posting_month'] = df['posting_date'].dt.month

# ====== 🧠 Header ======
text("# 🧠 AI Job Market Analysis Dashboard")
text("**Author:** Denish Asodariya  \nExplore salary trends, hiring patterns, and job roles across ~15,000 global AI job listings from 2024–2025.")

# ====== 🎯 Salary Threshold Filter ======
text("## 🎯 Filter by Salary Range")
salary_min = slider("💰 Show jobs with salary ≥", min_val=0, max_val=400000, default=50000, step=5000)
filtered_df = df[df["salary_usd"] >= salary_min]

if salary_min > df['salary_usd'].max():
    text("⚠️ You've set a salary threshold above all available listings.")
elif filtered_df.empty:
    text("⚠️ No jobs found for this salary threshold.")
else:
    fig_dyn = px.histogram(filtered_df, x="salary_usd", nbins=20, title=f"Salary Distribution ≥ ${salary_min}")
    plotly(fig_dyn)

# ====== 📊 Salary & Experience Insights ======
text("## 📊 Salary & Experience Insights")
top_titles = df["job_title"].value_counts().head(10).index.tolist()
top_locations = df["company_location"].value_counts().head(10).index.tolist()
top_data = df[df["job_title"].isin(top_titles) & df["company_location"].isin(top_locations)]

# Heatmap
heatmap_df = top_data.pivot_table(index="job_title", columns="company_location", values="salary_usd", aggfunc="mean").round(2)
fig1 = ff.create_annotated_heatmap(
    z=heatmap_df.values,
    x=heatmap_df.columns.tolist(),
    y=heatmap_df.index.tolist(),
    annotation_text=heatmap_df.values,
    colorscale="Viridis", showscale=True)
fig1.update_layout(title="Heatmap: Avg Salary by Job Title & Country")
plotly(fig1)

# Boxplot
fig2 = px.box(top_data, x="job_title", y="salary_usd", title="Salary Distribution by Top Job Titles", points="all")
plotly(fig2)

# Violin Plot
fig3 = px.violin(top_data, x="company_location", y="salary_usd", box=True, points="all", title="Salary Spread by Company Location")
plotly(fig3)

# Experience Distribution
exp_data = df[df["company_location"].isin(top_locations)]
exp_bar = exp_data.groupby(["company_location", "experience_level"]).size().reset_index(name="count")
fig4 = px.bar(exp_bar, x="company_location", y="count", color="experience_level", barmode="stack", title="Experience Level by Country")
plotly(fig4)

# ====== 📈 Salary Trends Over Time ======
text("## 📈 Salary Trends Over Time")
time_series = df[df["posting_year"].notna()] \
    .groupby(["posting_year", "experience_level"])["salary_usd"].mean().reset_index()
fig5 = px.line(time_series, x="posting_year", y="salary_usd", color="experience_level", markers=True, title="📈 Avg Salary by Experience Level Over Time")
plotly(fig5)

# ====== 📌 Data Scientist 2024 Static View ======
text("## 📌 Data Scientist Salaries in 2024")
ds_2024 = df[(df["job_title"] == "Data Scientist") & (df["posting_year"] == 2024)]
if not ds_2024.empty:
    fig6 = px.histogram(ds_2024, x="salary_usd", nbins=20, title="Data Scientist Salary Distribution (2024)")
    plotly(fig6)
else:
    text("⚠️ No Data Scientist job data found for 2024.")

# ====== 🛠️ Top Required Skills ======
text("## 🛠️ Top Required Skills")
skills_series = df["required_skills"].dropna().apply(lambda x: re.split(r',\s*', x))
all_skills = [skill.strip() for sublist in skills_series for skill in sublist if skill.strip()]
skill_counts = pd.DataFrame(Counter(all_skills).most_common(15), columns=["Skill", "Count"])
fig_skills = px.bar(skill_counts, x="Skill", y="Count", title="Top 15 Required Skills")
plotly(fig_skills)

# ====== 💼 Avg Salary by Top Skills ======
text("## 💼 Avg Salary by Top Skills")
df_skills = df[["salary_usd", "required_skills"]].dropna()
df_skills["required_skills"] = df_skills["required_skills"].apply(lambda x: [s.strip() for s in x.split(",")])
exploded_skills = df_skills.explode("required_skills")
top_10_skills = skill_counts["Skill"].head(10).tolist()
skill_salary = exploded_skills[exploded_skills["required_skills"].isin(top_10_skills)] \
    .groupby("required_skills")["salary_usd"].mean().reset_index().sort_values(by="salary_usd", ascending=False)
fig_skill_salary = px.bar(skill_salary, x="required_skills", y="salary_usd", title="💰 Avg Salary by Top 10 Skills")
plotly(fig_skill_salary)

# ====== 📐 Job Description Length vs Salary ======
text("## 📐 Job Description Length vs Salary")
fig_len = px.scatter(df, x="job_description_length", y="salary_usd", title="📝 Job Description Length vs Salary")
plotly(fig_len)

# ====== 🏠 Salary by Remote Ratio ======
text("## 🏠 Salary by Remote Ratio")
fig_remote = px.box(df, x="remote_ratio", y="salary_usd", title="💼 Salary Distribution by Remote Ratio")
plotly(fig_remote)

# ====== 🔍 Top Job Titles & Salary Ranges ======
text("## 🔍 Top Job Titles & Salary Ranges")
job_freq = df["job_title"].value_counts().head(15).reset_index()
job_freq.columns = ["job_title", "count"]
fig7 = px.bar(job_freq, x="job_title", y="count", color="count", color_continuous_scale="Cividis", title="Top 15 Most Common AI Job Titles")
plotly(fig7)

salary_ranges = df.groupby("job_title")["salary_usd"].agg(["min", "max", "mean"]).reset_index()
fig8 = go.Figure([
    go.Bar(
        x=salary_ranges["job_title"],
        y=salary_ranges["max"] - salary_ranges["min"],
        base=salary_ranges["min"],
        text=salary_ranges["mean"].round(0),
        name="Salary Range",
        hovertemplate="Min: %{base}<br>Max: %{y}<br>Mean: %{text}<extra></extra>"
    )
])
fig8.update_layout(title="📏 Salary Range by Job Title", xaxis_tickangle=45, yaxis_title="Salary (USD)", xaxis_title="Job Title")
plotly(fig8)

# ====== 📅 Seasonal Trends ======
text("## 📅 AI Job Postings by Month")
monthly = df.groupby("posting_month").size().reset_index(name="count")
fig9 = px.line(monthly, x="posting_month", y="count", markers=True, title="📅 Monthly Job Posting Trends")
fig9.update_xaxes(tickmode="array", tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
plotly(fig9)

# ====== 🌍 Salary by Experience Level & Country ======
text("## 🌍 Salary by Experience Level Across Countries")
exp_country = df[df["company_location"].isin(top_locations)] \
    .groupby(["company_location", "experience_level"])["salary_usd"].mean().reset_index()
fig10 = px.bar(exp_country, x="company_location", y="salary_usd", color="experience_level", barmode="group", title="🌎 Avg Salary by Experience & Country")
plotly(fig10)

# ====== 🗺️ Global Salary Choropleth ======
text("## 🌐 Global AI Salary Distribution")
map_data = df[df["company_location"].isin(df["company_location"].value_counts().head(30).index)]
map_avg = map_data.groupby("company_location")["salary_usd"].mean().reset_index()
map_avg.columns = ["country", "average_salary"]
fig_world = px.choropleth(map_avg, locations="country", locationmode="country names", color="average_salary", hover_name="country", color_continuous_scale="Plasma", title="🌍 Global Average AI Salary")
plotly(fig_world)

# ====== 🏢 Top Paying Companies ======
text("## 🏢 Top Paying Companies")
top_companies = df.groupby("company_name")["salary_usd"].mean().sort_values(ascending=False).head(5).reset_index()
table(top_companies, title="🏆 Top 5 Companies by Average Salary")


# ====== 🧑‍💼 Employment Type Distribution ======
text("## 🧑‍💼 Employment Type Distribution")
emp_counts = df["employment_type"].value_counts().reset_index()
emp_counts.columns = ["employment_type", "count"]
fig_emp = px.pie(emp_counts, names="employment_type", values="count", title="Employment Type Distribution")
plotly(fig_emp)

# ====== 🏢 Company Size vs Salary ======
text("## 🏢 Salary Distribution by Company Size")
fig_size = px.box(df, x="company_size", y="salary_usd", title="🏢 Salary by Company Size")
plotly(fig_size)

# ====== 📚 Education Level vs Salary ======
text("## 📚 Salary by Education Requirement")
fig_edu = px.box(df, x="education_required", y="salary_usd", title="🎓 Salary by Education Level")
plotly(fig_edu)

# ====== 🧓 Years of Experience vs Salary ======
text("## 🧓 Experience vs Salary")
fig_exp = px.scatter(df, x="years_experience", y="salary_usd", trendline="ols", title="📈 Years of Experience vs Salary")
plotly(fig_exp)

# ====== ⏰ Deadline Analysis ======
text("## ⏰ Application Deadlines")
df["deadline_days"] = (df["application_deadline"] - df["posting_date"]).dt.days
fig_deadline = px.histogram(df.dropna(subset=["deadline_days"]), x="deadline_days", nbins=30, title="📅 Time Between Job Posting and Deadline")
plotly(fig_deadline)

# ====== 🏭 Industry Salary View ======
text("## 🏭 Salary by Industry")
industry_salary = df.groupby("industry")["salary_usd"].mean().sort_values(ascending=False).reset_index()
fig_industry = px.bar(industry_salary.head(15), x="industry", y="salary_usd", title="💼 Top Industries by Avg Salary")
plotly(fig_industry)

# ====== 📋 Salary Stats ======
text("## 📋 Salary Statistics Summary")
stats = df["salary_usd"].describe().round(2)
text(
    f"**Summary (USD):**\n"
    f"- Count: {stats['count']}\n"
    f"- Mean: ${stats['mean']}\n"
    f"- Std Dev: ${stats['std']}\n"
    f"- Min: ${stats['min']}\n"
    f"- 25%: ${stats['25%']}\n"
    f"- Median: ${stats['50%']}\n"
    f"- 75%: ${stats['75%']}\n"
    f"- Max: ${stats['max']}"
)

# ====== 🎨 Visual Theme ======
text("## 🎨 Visual Design Notes")
text("We used **Viridis**, **Cividis**, and **Plasma** color scales for visual clarity. Future improvements may include dropdown filters and dark/light toggle themes.")
