# Contract Worker Dashboard

An interactive, self-contained HTML dashboard for visualising SOW (Statement of Work) contract workers managed by **Tejaswini C** and **Radhisha R**.

## 🌐 Live Dashboard

👉 **[https://tejaswini840.github.io/contract-worker-dashboard/](https://tejaswini840.github.io/contract-worker-dashboard/)**

## 📊 Features

- **6 KPI Cards** — Total Workers, Tejaswini C count, Radhisha R count, T&M, Fixed Price, Managed Service
- **5 Interactive Charts** (Chart.js):
  - Workers by Contract Name (bar)
  - Pricing Type Split (doughnut)
  - Top 10 Suppliers (horizontal bar)
  - SOW Status Breakdown (doughnut)
  - Monthly Worker Start Trend (line)
- **Smart Filters** — Owner, Contract Name, Pricing Type, SOW Status, Personnel Area, Date Range
- **Searchable & Sortable Table** — all 4,103 workers, paginated 50 per page
- **Colour-coded badges** — pricing type & owner at a glance

## 📁 Files

| File | Description |
|---|---|
| `index.html` | Self-contained dashboard (data embedded) |
| `dashboard_data.json` | Cleaned data export (4,103 records) |
| `C user dashboard cleaned.xlsx` | Cleaned Excel with Pricing Type & Contract Name filled |
| `clean_and_export.py` | Python script used to clean & export data |

## 🧹 Data Cleaning Applied

- **Pricing Type** & **Contract Name** columns filled in both sheets using the `Validation` sheet (keyed on Statement of Work ID)
- **Duplicate Buyer References removed**: 217 from Tejaswini C sheet, 8 from Radhisha R sheet
  - Strategy: kept the most recent entry per Buyer Reference (latest SOW Worker Start Date)

## 📅 Data

- Source: `C user dashboard as on 15th Nov (2).xlsx`
- Tejaswini C: 3,821 workers (after deduplication)
- Radhisha R: 283 workers (after deduplication)
- Total records: **4,103**

## 🚀 Share

Simply send the link:  
**https://tejaswini840.github.io/contract-worker-dashboard/**

No login required — anyone with the link can view it.
