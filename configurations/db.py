from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Params
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["infrawiz"]

# MongoDB Collections
collection_projects = db["projects"]
collection_generated_diagram_analysis = db["generated_diagram_analysis"]
collection_generated_json = db["generated_json"]
collection_generated_iac = db["generated_iac"]
