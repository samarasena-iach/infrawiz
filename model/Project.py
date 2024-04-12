from datetime import datetime
from pydantic import BaseModel


class Project(BaseModel):
    project_name: str
    cloud_service_provider: str
    description: str
    image_url: str
    project_status: str
    diagram_analysis: str
    json_status: str
    iac_status: str
    json_data: str
    iac_data: str
    created_date: datetime
