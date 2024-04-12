from configurations.db import *

async def prompt_generate_json(project_name: str):
    existing_project = await collection_projects.find_one({"project_name": project_name})
