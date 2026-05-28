from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/analyze/{owner}/{repo}")
def analyze(owner: str, repo: str):

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url)

    data = response.json()

    return {
        "name": data["name"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data["language"]
    }