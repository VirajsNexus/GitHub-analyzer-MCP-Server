from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from reportlab.pdfgen import canvas

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

@app.get("/report/{owner}/{repo}")
def generate_report(owner: str, repo: str):

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url)

    data = response.json()

    filename = f"{repo}_report.pdf"

    c = canvas.Canvas(filename)

    c.drawString(100, 800, f"Repository: {data['name']}")
    c.drawString(100, 780, f"Owner: {data['owner']['login']}")
    c.drawString(100, 760, f"Stars: {data['stargazers_count']}")
    c.drawString(100, 740, f"Forks: {data['forks_count']}")
    c.drawString(100, 720, f"Language: {data['language']}")

    c.save()

    return {
        "message": "PDF report generated",
        "file": filename
    }