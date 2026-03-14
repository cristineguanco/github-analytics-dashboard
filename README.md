DevPulse Data Platform

DevPulse is a data engineering project that collects trending repository data from GitHub, processes it through a small data pipeline, and visualizes programming language popularity using an interactive Streamlit dashboard.

Features

- Collects trending repository data from the GitHub API
- Processes and transforms repository metrics
- Stores analytics-ready data in a columnar format
- Visualizes language popularity and technology usage trends

Architecture

GitHub API → Data Collection → Transformation → Parquet Data Lake → DuckDB Analytics → Streamlit Dashboard

Tech Stack

- Python
- Parquet Data Lake
- DuckDB
- Streamlit
- GitHub API

Dashboard Insights

The dashboard provides insights such as:

- Top programming languages by total stars
- Language popularity share
- Technology usage distribution across repositories

Project Structure

devpulse-data-platform
│
├── dashboard.py
├── run_pipeline.py
├── test.py
├── README.md

How to Run

Install dependencies

pip install -r requirements.txt

Run the pipeline

python run_pipeline.py

Launch the dashboard

streamlit run dashboard.py

Data Source

Trending repository data collected from the GitHub API.

