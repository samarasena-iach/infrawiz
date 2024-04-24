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
from bson import ObjectId


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
async def projects_list(request: Request):
    # projects = await collection_projects.find().to_list(length=None)
    cursor = collection_projects.find()
    projects = list(cursor)
    return templates.TemplateResponse("projects_list.html", {"request": request, "projects": projects})


@app.post("/projects_list")
async def projects_list(request: Request):
    # projects = await collection_projects.find().to_list(length=None)
    cursor = collection_projects.find()
    projects = list(cursor)
    return templates.TemplateResponse("projects_list.html", {"request": request, "projects": projects})


@app.get("/view_generated_json/{project_id}")
async def view_generated_json(request: Request, project_id: str):
    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})

    if existing_project:
        json_content = {"project": existing_project.get('project_name'), "generated_json": existing_project.get('json_data'), "img": existing_project.get('image_url')}
        return templates.TemplateResponse("view_generated_json.html", {"request": request, "json_content": json_content})
