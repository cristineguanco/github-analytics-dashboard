import pandas as pd

print("Loading silver dataset...")

df = pd.read_parquet("data_lake/silver/github_trending_clean.parquet")

print("Building analytics tables...")

# Top programming languages
top_languages = (
    df.groupby("language")
    .agg(
        repo_count=("name", "count"),
        total_stars=("stars", "sum")
    )
    .sort_values(by="total_stars", ascending=False)
)

print("Saving gold analytics dataset...")

top_languages.to_parquet("data_lake/gold/github_language_stats.parquet")

print("Gold layer ready")
