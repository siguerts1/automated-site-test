import requests
import json
import os
import yaml
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("Missing GITHUB_TOKEN. Set it in .env or export it.")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Paths
CONFIG_FILE = "repos.yaml"
DATA_DIR = "data"

def load_repos(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get("repos", [])

def fetch_releases(repo):
    print(f"Fetching releases for {repo}...")
    url = f"https://api.github.com/repos/{repo}/releases"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def save_releases(repo, releases):
    safe_repo = repo.replace("/", "_")
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"{safe_repo}.json")
    with open(file_path, "w") as f:
        json.dump(releases, f, indent=2)
    print(f"✅ Saved {len(releases)} releases to {file_path}")

def main():
    repos = load_repos(CONFIG_FILE)
    print(f"🔍 Found {len(repos)} repos to check.\n")

    for repo in repos:
        try:
            releases = fetch_releases(repo)
            save_releases(repo, releases)
        except Exception as e:
            print(f"❌ Failed for {repo}: {e}")

    print(f"\n🎉 All done at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()

