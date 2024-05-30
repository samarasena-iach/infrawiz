from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Azure Storage Configs - Local Env
# storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY_LOCALENV')
# storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME_LOCALENV')
# connection_string = os.getenv('CONNECTION_STRING_LOCALENV')
# container_name = os.getenv('CONTAINER_NAME_LOCALENV')

# Azure Storage Configs - Cloud Env
storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY_CLOUDENV')
storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME_CLOUDENV')
connection_string = os.getenv('CONNECTION_STRING_CLOUDENV')
container_name = os.getenv('CONTAINER_NAME_CLOUDENV')