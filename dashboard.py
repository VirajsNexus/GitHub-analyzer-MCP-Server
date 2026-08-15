from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

from fastapi.templating import Jinja2Templates

from reportlab.pdfgen import canvas

import requests


# FastAPI app create
app = FastAPI()


# templates folder connect
templates = Jinja2Templates(directory="templates")


# Home Page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Analyze Repository
@app.post("/analyze", response_class=HTMLResponse)
def analyze_repo(request: Request, repo_url: str = Form(...)):

    try:

        # URL split
        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        # GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        response = requests.get(api_url)

        data = response.json()

        # Language API
        language_url = f"https://api.github.com/repos/{owner}/{repo}/languages"

        language_response = requests.get(language_url)

        language_data = language_response.json()

        # Send data to HTML
        return templates.TemplateResponse(
            request=request,
            name="index.html",

            context={

                "request": request,

                "repo": {

                    "name": data["name"],

                    "owner": data["owner"]["login"],

                    "stars": data["stargazers_count"],

                    "forks": data["forks_count"],

                    "watchers": data["watchers_count"],

                    "issues": data["open_issues_count"],

                    "language": data["language"],

                    "description": data["description"],

                    "languages": language_data,

                    "repo_url": repo_url
                }
            }
        )

    except:

        return templates.TemplateResponse(
            request=request,
            name="index.html",

            context={
                "request": request,

                "error": "Invalid GitHub Repository URL"
            }
        )


# PDF Report Generator
@app.get("/report/{owner}/{repo}")
def generate_report(owner: str, repo: str):

    # API URL
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url)

    data = response.json()

    # PDF file name
    filename = f"Github Repository Report.pdf"

    # Create PDF
    c = canvas.Canvas(filename)

    # Title
    c.setFont("Helvetica-Bold", 20)

    c.drawString(170, 800, "GitHub Repository Report")

    # Normal text
    c.setFont("Helvetica", 14)

    c.drawString(100, 740, f"Repository: {data['name']}")

    c.drawString(100, 710, f"Owner: {data['owner']['login']}")

    c.drawString(100, 680, f"Stars: {data['stargazers_count']}")

    c.drawString(100, 650, f"Forks: {data['forks_count']}")

    c.drawString(100, 620, f"Watchers: {data['watchers_count']}")

    c.drawString(100, 590, f"Open Issues: {data['open_issues_count']}")

    c.drawString(100, 560, f"Primary Language: {data['language']}")

    # Save PDF
    c.save()

    # Download PDF
    return FileResponse(
    path=filename,

    media_type="application/pdf",
    
    filename=filename
)