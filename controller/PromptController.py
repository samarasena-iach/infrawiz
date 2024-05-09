from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from configurations.db import *
from configurations.openai import *
from util.constants import *
import service.GPTIntegrationService as GptIntegrationService
from bson import ObjectId
import datetime

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Inside Prompt Controller"}


class ProjectId(BaseModel):
    project_id: str


class ModelDiagramAnalysis(BaseModel):
    project_id: str
    image_url: str


@router.post("/generate_diagram_analyzis")
async def generate_diagram_analysis(background_tasks: BackgroundTasks, data: ModelDiagramAnalysis):
    project_id = data.project_id
    image_url = data.image_url

    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})
    if existing_project:
        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_1_IMAGE_ANALYSIS_IN_PROGRESS,
            "timestamp_diagram_analysis_start": datetime.datetime.now()
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"_id": ObjectId(project_id)}, update_query)
    else:
        print(f"Project with id '{project_id}' not found.")

    background_tasks.add_task(que_generate_diagram_analysis, project_id, image_url)
    # return RedirectResponse("/projects_list")
    return JSONResponse({"message": "Process started in the background"})


def que_generate_diagram_analysis(project_id: str, image_url: str):
    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})

    if existing_project:
        response_message = GptIntegrationService.prompt_generate_diagram_analysis(image_url)

        # CALCULATING TIME ELAPSED FOR THE PROCESS
        start_time = existing_project.get("timestamp_diagram_analysis_start")
        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        time_elapsed_diagram_analysis = time_difference.total_seconds()

        # ADD RECORD TO "COLLECTION_GENERATED_DIAGRAM_ANALYSIS"
        record = {
            "project_id": existing_project.get("_id"),
            "project_name": existing_project.get('project_name'),
            "generated_diagram_analysis": response_message
        }
        collection_generated_diagram_analysis.insert_one(record)

        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_2_IMAGE_ANALYZED,
            "diagram_analysis": response_message,
            "timestamp_diagram_analysis_end": end_time,
            "time_elapsed_diagram_analysis": time_elapsed_diagram_analysis
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"_id": ObjectId(project_id)}, update_query)

    else:
        print(f"Project with id '{project_id}' not found.")


@router.post("/generate_json")
async def generate_json(background_tasks: BackgroundTasks, data: ProjectId):
    project_id = data.project_id

    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})
    if existing_project:
        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_3_JSON_GENERATION_IN_PROGRESS,
            "timestamp_json_generation_start": datetime.datetime.now()
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"_id": ObjectId(project_id)}, update_query)
    else:
        print(f"Project with id '{project_id}' not found.")

    background_tasks.add_task(queue_generate_json, project_id)
    # return RedirectResponse("/projects_list")
    return JSONResponse({"message": "Process started in the background"})


def queue_generate_json(project_id: str):
    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})

    if existing_project:
        response_message = GptIntegrationService.prompt_generate_json(project_id)

        # CALCULATING TIME ELAPSED FOR THE PROCESS
        start_time = existing_project.get("timestamp_json_generation_start")
        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        time_elapsed_json_generation = time_difference.total_seconds()

        # ADD RECORD TO "COLLECTION_GENERATED_JSON"
        record = {
            "project_id": existing_project.get("_id"),
            "project_name": existing_project.get('project_name'),
            "generated_json": response_message
        }
        collection_generated_json.insert_one(record)

        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_4_JSON_GENERATED,
            "json_status": JSON_GENERATION_GENERATED,
            "json_data": response_message,
            "timestamp_json_generation_end": end_time,
            "time_elapsed_json_generation": time_elapsed_json_generation
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"_id": ObjectId(project_id)}, update_query)

    else:
        print(f"Project with id '{project_id}' not found.")


@router.post("/generate_iac")
async def generate_iac(background_tasks: BackgroundTasks, data: ProjectId):
    project_id = data.project_id

    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})
    if existing_project:
        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_5_IAC_GENERATION_IN_PROGRESS,
            "timestamp_iac_generation_start": datetime.datetime.now()
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"_id": ObjectId(project_id)}, update_query)
    else:
        print(f"Project with id '{project_id}' not found.")

    background_tasks.add_task(queue_generate_iac, project_id)
    # return RedirectResponse("/projects_list")
    return JSONResponse({"message": "Process started in the background"})


def queue_generate_iac(project_id: str):
    existing_project = collection_projects.find_one({"_id": ObjectId(project_id)})

    if existing_project:
        response_message = GptIntegrationService.prompt_generate_iac(project_id)

        # CALCULATING TIME ELAPSED FOR THE PROCESS
        start_time = existing_project.get("timestamp_iac_generation_start")
        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        time_elapsed_iac_generation = time_difference.total_seconds()

        # ADD RECORD TO "COLLECTION_GENERATED_IAC"
        record = {
            "project_id": existing_project.get("_id"),
            "project_name": existing_project.get('project_name'),
            "generated_iac": response_message
        }
        collection_generated_iac.insert_one(record)

        # UPDATE EXISTING PROJECT RECORD
        updated_records = {
            "project_status": PROJECT_STATUS_PHASE_6_IAC_GENERATED,
            "iac_status": IAC_GENERATION_GENERATED,
            "iac_data": response_message,
            "timestamp_iac_generation_end": end_time,
            "time_elapsed_iac_generation": time_elapsed_iac_generation
        }

        update_query = {"$set": updated_records}
        collection_projects.update_one({"_id": ObjectId(project_id)}, update_query)

    else:
        print(f"Project with id '{project_id}' not found.")
