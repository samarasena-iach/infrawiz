# Tutorial : FastAPI Simple Website with Jinja2 Template
# https://www.youtube.com/watch?v=yK2Ktl6O894

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from configurations.db import *
from configurations.openai import *
from controller import ProjectController as project_controller
from controller import PromptController as prompt_controller


app = FastAPI(title="InfraWiz",
              docs_url="/docs",
              version="0.0.1")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Routes
app.include_router(project_controller.router, prefix="/api/projects/v1")
app.include_router(prompt_controller.router, prefix="/prompt")

# Web Templates & Static Content
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/new_project")
def new_project(request: Request):
    return templates.TemplateResponse("new_project.html", {"request": request})


@app.get("/projects_list")
async def new_project(request: Request):
    projects = await collection_projects.find().to_list(length=None)
    return templates.TemplateResponse("projects_list.html", {"request": request, "projects": projects})


@app.post("/projects_list")
async def new_project(request: Request):
    projects = await collection_projects.find().to_list(length=None)
    return templates.TemplateResponse("projects_list.html", {"request": request, "projects": projects})
