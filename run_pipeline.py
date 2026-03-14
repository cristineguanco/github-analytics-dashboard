import subprocess

print("Starting DevPulse data platform pipeline...")

print("Running ingestion pipeline...")
subprocess.run(["python", "ingestion/github_collector.py"])

print("Running silver cleaning pipeline...")
subprocess.run(["python", "pipelines/clean_github_data.py"])

print("Running gold analytics pipeline...")
subprocess.run(["python", "pipelines/build_github_analytics.py"])

print("Running analytics queries...")
subprocess.run(["python", "analytics/query_github_data.py"])

print("All pipelines completed!")
