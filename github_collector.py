  print("SCRIPT STARTED")

import requests
import pandas as pd

print("Requesting GitHub data...")

url = "https://api.github.com/search/repositories?q=stars:>50000&sort=stars"

response = requests.get(url)
data = response.json()

print("Data received")

repos = []

for repo in data.get("items", []):
    repos.append({
        "name": repo["name"],
        "language": repo["language"],
        "stars": repo["stargazers_count"]
    })

print("Repositories parsed:", len(repos))

df = pd.DataFrame(repos)

print("Saving to data lake...")

df.to_parquet("data_lake/bronze/github_trending_raw.parquet")

print("Data collected successfully!")



