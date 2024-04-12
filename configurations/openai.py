import os
from openai import AzureOpenAI

# Azure OpenAI Params
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = 'infrawiz-gpt-4-vision-preview-integration'
api_version = '2023-12-01-preview'  # this might change in the future

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)