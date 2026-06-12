# 🛒 E-Commerce Sales Analysis

An end-to-end data analytics project: taking a messy 5,000-row retail dataset from raw export to clean data, analysing it in **SQL**, and presenting the results in **three interactive Tableau dashboards** — each answering a real business question.

> **Raw data ➜ Clean data ➜ SQL analysis ➜ Dashboards ➜ Business insights**

---

## 📊 Live Dashboards

All three dashboards are published on Tableau Public:

| Dashboard | Business question | Link |
|-----------|-------------------|------|
| **1 · Executive Overview** | How is the business performing overall? | [View »](https://public.tableau.com/app/profile/abolade.farombi/viz/E-CommerceSales_17812693469420/Dashboard1) |
| **2 · Customer & Market Insights** | Who are our customers and where are they? | [View »](https://public.tableau.com/app/profile/abolade.farombi/viz/E-CommerceSales_17812693469420/Dashboard2) |
| **3 · Pricing & Promotions** | Are our discounts actually working? | [View »](https://public.tableau.com/app/profile/abolade.farombi/viz/E-CommerceSales_17812693469420/Dashboard3) |

👤 Full Tableau Public profile: **[abolade.farombi](https://public.tableau.com/app/profile/abolade.farombi)**

---

## 📌 Project Overview

An online retailer sells across four categories — **Electronics, Fashion, Home Appliances, and Beauty Products**. The raw data export was full of real-world problems: missing values, duplicate rows, inconsistent spellings, currency symbols stuck inside number columns, invalid emails, impossible ages, mixed date formats, and incorrect order totals.

This project cleans that data, analyses it in SQL, and turns it into clear business insights — handled the way a working analyst would: **no fabricated values, anomalies flagged rather than hidden, and every cleaning decision documented.**

---

## 🧰 Tools Used

| Step | Tools |
|------|-------|
| Data cleaning | **Python (pandas)**, **Excel**, **Power Query** *(cleaned three different ways)* |
| Database & querying | **Microsoft SQL Server (SSMS)** |
| Visualisation | **Tableau Public** |
| Version control | **Git + GitHub** |

> 💡 The dataset was cleaned **three independent ways** — a Python/pandas script, a manual Excel walkthrough, and a Power Query pipeline — to demonstrate fluency across the tools an analyst is likely to use day-to-day.

---

## 🗂️ Repository Contents

```
ecommerce-sales-analysis/
├── README.md                       <- you are here
├── ecommerce_sales_dirty.csv       <- raw, messy data (5,000 rows)
├── ecommerce_sales_clean.csv       <- cleaned output
├── clean_data.py                   <- Python (pandas) cleaning script
└── dashboard_insights.sql          <- SQL analysis queries (organised by dashboard)
```

---

## 🔧 Data Cleaning — what was fixed

- Removed **duplicate** rows and **fully-empty** rows
- Stripped **whitespace** and stray **special characters**
- Standardised **product categories** (`electronik`, `Electronic` ➜ `Electronics`)
- Standardised **payment methods** (`CC`, `credit_card` ➜ `Credit Card`)
- Removed **currency symbols** (`$ £ € ₦`) and converted price/total columns to real numbers
- Normalised **discounts** into a single decimal format
- **Recomputed Total_Sales** = `Quantity × Unit_Price × (1 − Discount)` to fix incorrect totals
- Flagged & blanked **invalid emails**
- Set **impossible ages** (negative, zero, or absurdly high) to missing rather than guessing
- Parsed **7 different date formats** into one ISO standard (`YYYY-MM-DD`)

Wherever data was genuinely unknown, it was **left blank rather than invented** — and a note kept for any value that couldn't be confidently recovered.

---

## 📈 Key Insights

### 1 · Executive Overview
- 💰 **~£10.4M** total revenue across **~4,856 orders**, with an average order value of **~£2,265**.
- 🥇 **Electronics** is the dominant category (~45% of revenue), led by **Laptops** and **Refrigerators**.
- ⭐ Average customer rating is **3.76 / 5**, fairly consistent across categories.
- 📅 A revenue spike in **Sept 2024** was driven by a small number of high-value orders — flagged and annotated rather than removed.

### 2 · Customer & Market Insights
- 🌍 **Canada** is the strongest market, ahead of the UK, Germany, and India.
- 👥 **Female customers** generate the majority of revenue.
- 👴 The **45–54 and 55+** age groups together drive **~64% of revenue** — older, higher-value shoppers, which runs counter to the usual "young online shopper" assumption.

### 3 · Pricing & Promotions
- 🎯 **Discounted orders carry ~18% higher value** (**£2,432** vs **£2,054** AOV) — but contain ~1 fewer item each, meaning the **big-ticket products are the ones being discounted**.
- 💳 **Apple Pay** is the top payment method by revenue (~£3.0M, nearly double the next).
- 📊 Among discounted orders, the **11–20% discount band** is the revenue sweet spot — earning more than the 1–10% band despite fewer orders.

---

## ▶️ How to Reproduce

```bash
# 1. Clean the data with Python
python clean_data.py          # reads ecommerce_sales_dirty.csv -> writes ecommerce_sales_clean.csv

# 2. Load ecommerce_sales_clean.csv into SQL Server (Import Flat File wizard)
#    Run the queries in dashboard_insights.sql to reproduce the analysis

# 3. Connect Tableau to the clean CSV (or SQL Server) and build the dashboards
```

---

## 👤 Author

**Abolade Farombi** — Data Analyst · SQL · Power BI · BSc Mathematical Sciences

🔗 [Tableau Public](https://public.tableau.com/app/profile/abolade.farombi)
