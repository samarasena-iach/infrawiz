from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Params - Local Env
# api_base = os.getenv('AZURE_OPENAI_ENDPOINT_LOCALENV')
# api_key = os.getenv('AZURE_OPENAI_API_KEY_LOCALENV')
# deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME_LOCALENV')
# api_version = os.getenv('AZURE_OPENAI_API_VERSION_LOCALENV')

# Azure OpenAI Params - Cloud Env
api_base = os.getenv('AZURE_OPENAI_ENDPOINT_CLOUDENV')
api_key = os.getenv('AZURE_OPENAI_API_KEY_CLOUDENV')
deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME_CLOUDENV')
api_version = os.getenv('AZURE_OPENAI_API_VERSION_CLOUDENV')

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)