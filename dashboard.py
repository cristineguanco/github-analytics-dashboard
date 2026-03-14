import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import os

st.set_page_config(layout="wide")

# CSS
st.markdown("""
<style>
div[data-testid="metric-container"] { text-align: center; }

div[data-testid="metric-container"] label {
    width: 100%;
    text-align: center;
    display: block;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    justify-content: center;
}

th { text-align: center !important; }
td { text-align: center !important; }

table { width: 100%; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("DevPulse")
st.subheader("GitHub Trending Repository Analytics Platform")

now = datetime.now()
st.caption("Trending Data as of: " + now.strftime("%Y-%m-%d %H:%M") + " (UTC+8)")

# Load data safely
@st.cache_data
def load_data():
    file_path = "data/github_language_stats.parquet"  # relative path
    
    if not os.path.exists(file_path):
        st.error(f"Data file not found: {file_path}")
        return pd.DataFrame()  # empty dataframe fallback
    
    return pd.read_parquet(file_path)

df = load_data()

# If dataframe is empty, stop further processing
if df.empty:
    st.stop()

# Data cleaning
if "language" not in df.columns:
    df = df.reset_index()
    if "index" in df.columns:
        df = df.rename(columns={"index": "language"})

exclude_langs = ["Jupyter notebook", "HTML", "CSS"]

df = df[~df["language"].isin(exclude_langs)]
df = df.dropna(subset=["language", "total_stars"])
df["language"] = df["language"].astype(str).str.strip()
df = df.sort_values("total_stars", ascending=False)
df["rank"] = range(1, len(df) + 1)

# Sidebar filters
st.sidebar.title("Filters")
top_n = st.sidebar.slider("Number of languages", 5, 20, 10)

# KPIs
space1, kpi1, kpi2, kpi3, space2 = st.columns([1,2,2,2,1])

kpi1.metric("Languages", df["language"].nunique())
kpi2.metric("Repositories", f"{int(df['repo_count'].sum()):,}")
kpi3.metric("Total Stars", f"{int(df['total_stars'].sum()):,}")

st.markdown("---")

# Insights
st.markdown("### Key Insights")

top_language = df.iloc[0]["language"]
top_stars = df.iloc[0]["total_stars"]
second_language = df.iloc[1]["language"]

share = (top_stars / df["total_stars"].sum()) * 100

st.info(
f"""
🔥 **{top_language}** is the most popular language in trending repositories.

⭐ It accounts for **{share:.1f}% of all stars** in the dataset.

📊 **{second_language}** follows as the second most popular language.
"""
)

st.markdown("---")

# Table
st.markdown("### Top GitHub Repository Languages by Total Stars")

table_df = df.head(top_n).copy()
table_df = table_df.rename(columns={
    "rank": "Rank",
    "language": "Language",
    "repo_count": "Repositories",
    "total_stars": "Total Stars"
})

table_df["Repositories"] = table_df["Repositories"].map("{:,}".format)
table_df["Total Stars"] = table_df["Total Stars"].map("{:,}".format)

table_html = table_df[["Rank","Language","Repositories","Total Stars"]].to_html(index=False)
st.markdown(table_html, unsafe_allow_html=True)

csv = df.to_csv(index=False)
st.download_button(
    "Download Dataset",
    csv,
    "github_language_stats.csv",
    "text/csv"
)

st.markdown("---")

# Chart helpers
def clean_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C0C0C0")
    ax.spines["bottom"].set_color("#C0C0C0")

def star_formatter(x, pos):
    if x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"{x/1_000:.0f}K"
    return int(x)

# Language popularity
st.markdown("### GitHub Language Popularity")

top_lang = df.head(top_n)
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.barh(top_lang["language"], top_lang["total_stars"], color="#2DA44E")
ax.invert_yaxis()
ax.set_xlabel("Total Stars")
ax.xaxis.set_major_formatter(FuncFormatter(star_formatter))
clean_axis(ax)

for bar in bars:
    value = bar.get_width()
    ax.text(
        value * 0.98,
        bar.get_y() + bar.get_height()/2,
        star_formatter(value, None),
        va="center",
        ha="right",
        color="white"
    )

st.pyplot(fig)
st.markdown("---")

# Language share
st.markdown("### Language Share in GitHub Repositories")
share_df = df.copy()
total_stars = share_df["total_stars"].sum()
share_df["percent"] = (share_df["total_stars"] / total_stars) * 100
share_df = share_df.sort_values("percent", ascending=False).head(top_n)

fig2, ax2 = plt.subplots(figsize=(10,5))
bars = ax2.barh(share_df["language"], share_df["percent"], color="#2DA44E")
ax2.invert_yaxis()
ax2.set_xlabel("Percent Share")
clean_axis(ax2)

for bar in bars:
    value = bar.get_width()
    ax2.text(
        value * 0.98,
        bar.get_y() + bar.get_height()/2,
        f"{value:.1f}%",
        va="center",
        ha="right",
        color="white"
    )

st.pyplot(fig2)
st.markdown("---")

# Popularity distribution
st.markdown("### Popularity Distribution of Languages")
stars = np.log10(df["total_stars"])
fig3, ax3 = plt.subplots(figsize=(10,5))
counts, bins, patches = ax3.hist(stars, bins=8, color="#2DA44E")
ax3.set_xlabel("Log10 Total Stars")
ax3.set_ylabel("Number of Languages")
clean_axis(ax3)

for count, patch in zip(counts, patches):
    if count > 0:
        ax3.text(
            patch.get_x() + patch.get_width()/2,
            count * 0.8,
            int(count),
            ha="center",
            va="center",
            color="white"
        )

st.pyplot(fig3)
st.markdown("---")

# Technology domains
st.markdown("### Technology Domains in GitHub Repositories")
usage_df = df.copy()
usage_df["language"] = usage_df["language"].str.lower()

usage_map = {
    "python": "Data / AI",
    "javascript": "Web Development",
    "typescript": "Web Development",
    "go": "Backend Systems",
    "rust": "Systems Programming",
    "c": "Systems Programming",
    "c++": "Systems Programming",
    "c#": "Enterprise / Game",
    "java": "Enterprise Software",
    "kotlin": "Mobile Development",
    "swift": "Mobile Development",
    "dart": "Mobile Development",
    "shell": "Automation",
    "bash": "Automation",
    "powershell": "Automation"
}

usage_df["tech_usage"] = usage_df["language"].map(usage_map)
usage_df = usage_df[usage_df["tech_usage"].notna()]

usage_summary = usage_df.groupby("tech_usage")["total_stars"].sum().sort_values(ascending=True)
usage_percent = (usage_summary / usage_summary.sum()) * 100

fig4, ax4 = plt.subplots(figsize=(10,5))
bars = ax4.barh(usage_percent.index, usage_percent.values, color="#2DA44E")
ax4.set_xlabel("Percent Share")
clean_axis(ax4)

for bar in bars:
    value = bar.get_width()
    ax4.text(
        value * 0.98,
        bar.get_y() + bar.get_height()/2,
        f"{value:.1f}%",
        va="center",
        ha="right",
        color="white"
    )

st.pyplot(fig4)
st.markdown("---")

st.caption("""
Data Source: GitHub Trending  
Dashboard: DevPulse Analytics Platform
""")
