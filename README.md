# 🏦 Customer Segmentation & Churn Pattern Analytics in European Banking

> **Unified Mentor Data Science Internship Project**

A segmentation-driven analytics project uncovering customer churn patterns across European banking customers in France, Spain, and Germany — with an interactive Streamlit dashboard.

---

## 📌 Project Overview

Customer churn is one of the largest hidden costs in retail banking. This project addresses the challenge of identifying **which customers are most at risk of leaving**, and **why** — using systematic segmentation across geography, demographics, credit profile, and financial behaviour.

**Dataset:** 10,000 customers | **Source:** European Central Bank (simulated retail banking data)

---

## 🔍 Key Findings

| Insight | Value |
|---|---|
| Overall Churn Rate | **20.4%** |
| Highest Churn Geography | **Germany (32.4%)** |
| Highest Churn Age Group | **46–60 years (51.1%)** |
| Female vs Male Churn | **25.1% vs 16.5%** |
| Inactive Member Churn | **26.9% vs 14.3% (active)** |
| High-Value Customer Churn | **23.0%** |
| Revenue at Risk (HV Churners) | **€58.7 Million** |

---

## 📊 Features

### Streamlit Dashboard
- **Overview** — KPI cards, churn distribution, geography and age breakdown
- **Geography Analysis** — Regional heatmaps, geography × age interaction, gender split
- **Demographics** — Credit score bands, tenure groups, engagement analysis, age histograms
- **High-Value Customers** — Premium customer churn, revenue at risk, balance distribution
- **Segment Explorer** — Interactive drill-down across any combination of dimensions

### Analytical Methodology
1. Data Ingestion & Validation
2. Data Cleaning & Preparation
3. Customer Segmentation Design (Geography, Age, Credit, Tenure, Balance)
4. Churn Distribution Analysis
5. Comparative Demographic Analysis
6. High-Value Customer Churn Analysis

---

## 🗂️ Dataset Description

| Column | Description |
|---|---|
| CustomerId | Unique customer identifier |
| CreditScore | Customer creditworthiness |
| Geography | France / Spain / Germany |
| Gender | Male / Female |
| Age | Customer age |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of bank products held |
| HasCrCard | Credit card ownership (0/1) |
| IsActiveMember | Activity indicator (0/1) |
| EstimatedSalary | Estimated annual salary |
| Exited | Churn indicator — **target variable** (0/1) |

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/european-bank-churn-analytics.git
cd european-bank-churn-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
european-bank-churn-analytics/
│
├── app.py                  # Streamlit dashboard
├── European_Bank.xlsx      # Dataset
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 📦 Deliverables

- ✅ Interactive Streamlit Dashboard (live deployment)
- ✅ Excel Analysis Report (5 sheets — KPIs, Segmentation, Demographics, High-Value, Raw Data)
- ✅ Research Paper (EDA, insights, recommendations)
- ✅ Executive Summary for stakeholders

---

## 🛠️ Tech Stack

- **Python** — pandas, numpy, plotly
- **Streamlit** — web application framework
- **Excel/openpyxl** — structured reporting

---

## 👩‍💻 Author

**Srija** | Data Science Intern — Unified Mentor  
Project: Customer Segmentation & Churn Pattern Analytics in European Banking
