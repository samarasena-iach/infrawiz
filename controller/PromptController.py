from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from configurations.db import *
from configurations.openai import *
from util.constants import *
import service.GPTIntegrationService as GptIntegrationService

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Inside Prompt Controller"}


class ProjectName(BaseModel):
    project_name: str


class ModelDiagramAnalysis(BaseModel):
    project_name: str
    image_url: str


@router.post("/generate_diagram_analyzis")
async def generate_diagram_analysis(background_tasks: BackgroundTasks, data: ModelDiagramAnalysis):
    project_name = data.project_name
    image_url = data.image_url

    existing_project = collection_projects.find_one({"project_name": project_name})
    if existing_project:
        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_1_IMAGE_ANALYSIS_IN_PROGRESS
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"project_name": project_name}, update_query)
    else:
        print(f"Project with name '{project_name}' not found.")

    background_tasks.add_task(que_generate_diagram_analysis, project_name, image_url)
    # return RedirectResponse("/projects_list")
    return JSONResponse({"message": "Process started in the background"})


def que_generate_diagram_analysis(project_name: str, image_url: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        response_message = GptIntegrationService.prompt_generate_diagram_analysis(image_url)

        # ADD RECORD TO "COLLECTION_GENERATED_DIAGRAM_ANALYSIS"
        record = {
            "project_name": project_name,
            "generated_diagram_analysis": response_message
        }
        collection_generated_diagram_analysis.insert_one(record)

        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_2_IMAGE_ANALYZED,
            "diagram_analysis": response_message
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"project_name": project_name}, update_query)

    else:
        print(f"Project with name '{project_name}' not found.")


@router.post("/generate_json")
async def generate_json(background_tasks: BackgroundTasks, data: ProjectName):
    project_name = data.project_name

    existing_project = collection_projects.find_one({"project_name": project_name})
    if existing_project:
        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_3_JSON_GENERATION_IN_PROGRESS
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"project_name": project_name}, update_query)
    else:
        print(f"Project with name '{project_name}' not found.")

    background_tasks.add_task(queue_generate_json, project_name)
    # return RedirectResponse("/projects_list")
    return JSONResponse({"message": "Process started in the background"})


def queue_generate_json(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        response_message = GptIntegrationService.prompt_generate_json(project_name)

        # ADD RECORD TO "COLLECTION_GENERATED_JSON"
        record = {
            "project_name": project_name,
            "generated_json": response_message
        }
        collection_generated_json.insert_one(record)

        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_4_JSON_GENERATED,
            "json_status": JSON_GENERATION_GENERATED,
            "json_data": response_message
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"project_name": project_name}, update_query)

    else:
        print(f"Project with name '{project_name}' not found.")


@router.post("/generate_iac")
async def generate_iac(background_tasks: BackgroundTasks, data: ProjectName):
    project_name = data.project_name

    existing_project = collection_projects.find_one({"project_name": project_name})
    if existing_project:
        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_5_IAC_GENERATION_IN_PROGRESS
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"project_name": project_name}, update_query)
    else:
        print(f"Project with name '{project_name}' not found.")

    background_tasks.add_task(queue_generate_iac, project_name)
    # return RedirectResponse("/projects_list")
    return JSONResponse({"message": "Process started in the background"})


def queue_generate_iac(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        response_message = GptIntegrationService.prompt_generate_iac(project_name)

        # ADD RECORD TO "COLLECTION_GENERATED_IAC"
        record = {
            "project_name": project_name,
            "generated_iac": response_message
        }
        collection_generated_iac.insert_one(record)

        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_6_IAC_GENERATED,
            "iac_status": IAC_GENERATION_GENERATED,
            "iac_data": response_message
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"project_name": project_name}, update_query)

    else:
        print(f"Project with name '{project_name}' not found.")
