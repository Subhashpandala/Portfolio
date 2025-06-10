# Healthcare Claims Analysis Dashboard – BigQuery & Tableau

## Overview  
This project delivers an end-to-end healthcare cost analysis using a public dataset, with insights deployed through a stakeholder-facing Tableau dashboard. It explores how demographic and lifestyle factors influence insurance charges, simulating analytical workflows used in healthcare and payer organizations.

The backend analysis was performed in Google BigQuery using advanced SQL logic, and the outputs were visualized using Tableau to support interactive decision-making.

---

## Objectives  
- Identify cost-driving variables influencing healthcare charges  
- Segment trends by smoker status, region, age, BMI, and number of children  
- Build a clean, filterable Tableau dashboard for business-ready consumption  

---

## Tools & Technologies  
- **Google BigQuery** – SQL-based analysis and aggregation  
- **Tableau Desktop** – Interactive dashboard design  
- **Public Healthcare Dataset** – Demographics, charges, lifestyle factors  

---

## Key Analyses (SQL – BigQuery)  
- Average charges by **smoker status**  
- Regional cost variation segmented by **smoker type**  
- Correlation of **age and BMI** with insurance charges  
- Impact of **number of children** on cost trends  

All cleaned and transformed outputs were exported to Tableau as the final reporting layer.

---

## Dashboard Features (Tableau)  
- **Dropdown filter**: Smoker vs Non-Smoker  
- **Bar Charts**: Charges by Region and Smoker Status  
- **Scatter Plots**: Age vs BMI grouped by charges  
- **Category Highlights**: Children impact on healthcare costs  

The dashboard was designed for non-technical business stakeholders and supports real-world health cost evaluations.

---

## Business Relevance  
This analysis mirrors real-world use cases in payer analytics, population health management, and actuarial pricing. It demonstrates how SQL-based cloud analytics combined with effective dashboarding can surface high-risk groups and cost leakage areas.

---
## 🖼 Dashboard Preview  
![Healthcare Claims Dashboard](dashboard_preview.png)

---
## Files Included  
- `dashboard_preview.png` – Tableau dashboard snapshot  
- `bigquery_sql_scripts.sql` – Query logic for data transformation  

---

## Key Outcomes  
- Deployed **parameterized SQL logic** in BigQuery for cost segmentation  
- Designed a **filterable Tableau dashboard** tailored to business insights  
- Communicated cost trends visually for **executive health analytics**  

---

## Use Cases  
- Healthcare plan cost optimization  
- Risk segmentation and demographic profiling  
- Insurance strategy and pricing models  
- Executive insights for healthcare providers or insurers 
