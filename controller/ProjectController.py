from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from util.constants import *
from configurations.db import *
from service.ImageStorageService import *
import datetime

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Inside Project Controller"}


@router.post("/create_project")
async def create_project(project_name: str = Form(...),
                         cloud_service_provider: str = Form(...),
                         description: str = Form(...),
                         file_upload: UploadFile = File(...)):
    cloud_sp = ''
    if cloud_service_provider == '1':
        cloud_sp = 'Microsoft Azure'
    elif cloud_service_provider == '2':
        cloud_sp = 'Amazon Web Services'
    elif cloud_service_provider == '3':
        cloud_sp = 'Google Cloud Platform'
    else:
        cloud_sp = 'N/A'

    file_content = await file_upload.read()

    # Write image content locally
    with open(f"static/images/uploads/{file_upload.filename}", "wb") as f:
        f.write(file_content)

    local_path = f"C:\\Projects\\Python\\fastapi_jinja_website\\static\\images\\uploads\\{file_upload.filename}"

    # Upload the static image (saved locally in previous step) to the Azure Blob Storage
    # Azure Blob Storage will return Public access URL for the uploaded image
    img_url = uploadArchitectureDiagramToAzureBlobStorage(local_path, file_upload.filename)

    # Prepare new record for the mongo collection 'projects'
    record = {
        "project_name": project_name,
        "cloud_service_provider": cloud_sp,
        "description": description,
        "image_url": img_url,
        "project_status": PROJECT_STATUS_INITIATED,
        "diagram_analysis": "-",
        "json_status": JSON_GENERATION_PENDING,
        "iac_status": IAC_GENERATION_PENDING,
        "json_data": "-",
        "iac_data": "-",
        "created_date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    # Add record to 'projects' mongo collection
    collection_projects.insert_one(record)

    return RedirectResponse("/projects_list")


@router.get("/get_project_metrics_by_project_name")
def get_project_metrics_by_project_name(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        image_url = existing_project.get('image_url')
        json_content = {"project": project_name, "image_url": image_url}
        return json_content


@router.get("/get_diagram_analysis_by_project_name")
def get_diagram_analysis_by_project_name(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        diagram_analysis = existing_project.get('diagram_analysis')
        json_content = {"project": project_name, "diagram_analysis": diagram_analysis}
        analyze_content = json_content["diagram_analysis"]
        formatted_content = analyze_content.replace("\n", "<br>")
        return formatted_content


@router.get("/get_generated_json_by_project_name")
def get_generated_json_by_project_name(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        generated_json = existing_project.get('json_data')
        json_content = {"project": project_name, "generated_json": generated_json}
        analyze_content = json_content["generated_json"]
        return analyze_content


@router.get("/get_generated_iac_by_project_name")
def get_generated_iac_by_project_name(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    if existing_project:
        generated_iac = existing_project.get('iac_data')
        json_content = {"project": project_name, "generated_iac": generated_iac}
        analyze_content = json_content["generated_iac"]
        return analyze_content
