# from motor.motor_asyncio import AsyncIOMotorClient
#
# # MongoDB Params
# MONGO_URI = "mongodb://localhost:27017"
# client = AsyncIOMotorClient(MONGO_URI)
# db = client["infrawiz"]
#
# # MongoDB Collections
# collection_projects = db["projects"]
# collection_generated_diagram_analysis = db["generated_diagram_analysis"]
# collection_generated_json = db["generated_json"]
# collection_generated_iac = db["generated_iac"]

from dotenv import load_dotenv
import os
from pymongo import MongoClient

# MongoDB Params
# Connection Str - Local Env
# MONGO_URI = os.getenv('MONGO_URI_LOCALENV')

# Connection Str - Cloud Env
MONGO_URI = os.getenv('MONGO_URI_CLOUDENV')

client = MongoClient(MONGO_URI)
db = client["infrawiz"]

try:
    client.admin.command('ping')
    print("*** Successfully connected to MongoDB! ***")
except Exception as e:
    print(e)

# MongoDB Collections
collection_projects = db["projects"]
collection_generated_diagram_analysis = db["generated_diagram_analysis"]
collection_generated_json = db["generated_json"]
collection_generated_iac = db["generated_iac"]