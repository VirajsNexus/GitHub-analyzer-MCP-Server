from mcp.server.fastmcp import FastMCP
import requests

app = FastMCP("GitHub Analyzer")

@app.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"


@app.tool()
def analyze_repo(repo_url):

    if isinstance(repo_url, list):
        repo_url = repo_url[0]

    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url)

    if response.status_code != 200:
        return {"error": "Repository not found"}

    data = response.json()

    return {
        "name": data["name"],
        "owner": data["owner"]["login"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data["language"]
    }

@app.tool()
def check_readme(repo_url):

    if isinstance(repo_url, list):
        repo_url = repo_url[0]

    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url)

    if response.status_code != 200:
        return {"error": "Repository not found"}

    data = response.json()

    return {
        "has_description": bool(data["description"]),
        "has_license": bool(data["license"]),
        "default_branch": data["default_branch"]
    }

@app.tool()
def get_language(repo_url):
    if isinstance(repo_url, list):
        repo_url = repo_url[0]

    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"

    response = requests.get(api_url)

    if response.status_code != 200:
        return {"error": "Could not fetch languages"}

    data = response.json()

    total_bytes = sum(data.values())

    percentages = {}

    for language, bytes_used in data.items():
        percentages[language] = round((bytes_used / total_bytes) * 100, 2)

    return percentages

if __name__ == "__main__":
    app.run()