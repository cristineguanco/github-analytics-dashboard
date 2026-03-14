import pandas as pd

print("Loading bronze data...")

df = pd.read_parquet("data_lake/bronze/github_trending_raw.parquet")

print("Cleaning data...")

# remove missing languages
df = df.dropna(subset=["language"])

# standardize text
df["language"] = df["language"].str.lower()

# sort by stars
df = df.sort_values(by="stars", ascending=False)

print("Saving silver dataset...")

df.to_parquet("data_lake/silver/github_trending_clean.parquet")

print("Silver pipeline complete")
