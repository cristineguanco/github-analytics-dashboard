# DevPulse Data Platform

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

DevPulse is a lightweight data engineering project that collects trending repository data from GitHub, processes it through a small data pipeline, and visualizes programming language trends using an interactive Streamlit dashboard.

The goal of this project is to demonstrate a simple modern analytics workflow using Python, a columnar data lake, and an embedded analytical database.

---

## Project Overview

The pipeline collects repository metadata from the GitHub API, transforms it into analytics-ready datasets, and stores it in a Parquet data lake.  
DuckDB is used to run analytical queries directly on the data, and the results are visualized through a Streamlit dashboard.

This project focuses on building a simple but realistic data workflow that mirrors common patterns used in modern data platforms.

---

## Features

- Collects trending repository data from the GitHub API  
- Cleans and transforms repository metrics for analysis  
- Stores processed datasets in **Parquet format**  
- Runs analytical queries using **DuckDB**  
- Visualizes insights through an **interactive Streamlit dashboard**

---

## Architecture

```
GitHub API
    ↓
Data Collection
    ↓
Data Transformation
    ↓
Parquet Data Lake
    ↓
DuckDB Analytics
    ↓
Streamlit Dashboard
```
---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data pipeline and processing |
| GitHub API | Repository data source |
| Parquet | Columnar data storage |
| DuckDB | Analytical query engine |
| Streamlit | Dashboard and visualization |

---

## Dashboard Insights

The dashboard highlights several insights from the collected repositories:

- Top programming languages by total stars  
- Programming language popularity distribution  
- Technology usage trends across repositories  

---

## Project Structure

```
devpulse-data-platform/
│
├── data_lake/
│   ├── bronze/
│   │   └── github_trending_raw.parquet       # Raw data from GitHub API
│   ├── silver/
│   │   └── github_trending_clean.parquet     # Cleaned and standardized data
│   └── gold/
│       ├── github_language_stats.parquet     # Aggregated stats by language
│       ├── github_language_trends.parquet    # Trending language metrics
│       ├── gold_pipeline.py                  # Gold Layer processing pipeline
│       └── gold_pipeline_analytics_query.py # Runs analytics queries on Gold datasets
│
├── run_pipeline.py            # Executes the full pipeline (Bronze → Silver → Gold)
├── bronze_pipeline.py         # Collects raw GitHub data
├── silver_pipeline.py         # Cleans and transforms Bronze data
├── dashboard.py               # Streamlit dashboard to visualize insights
└── README.md                  # Project documentation
```

----

## Running the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Data Pipeline

```bash
python run_pipeline.py
```

### 3. Launch the Dashboard

```bash
streamlit run dashboard.py
```
---

## Source

Repository data is collected from GitHub API, focusing on trending repositories and their associated metadata such as stars, programming languages, and repository statistics.

---
## Future Improvements

Add automated pipeline scheduling

Store historical data for trend analysis

Expand dashboard metrics and visualizations

Integrate additional repository metadata
