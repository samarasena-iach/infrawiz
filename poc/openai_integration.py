from openai import AzureOpenAI
import os

api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = 'infrawiz-gpt-4-vision-preview-integration'
api_version = '2023-12-01-preview'  # this might change in the future

# print(api_base)
# print(api_key)

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)

# image_url = "https://<your-storage-account>.blob.core.windows.net/<container-name>/static/images/sample/aws_arch_sample_01.png"
image_url = "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2022/11/07/usage-reports-2-2.png"

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": [
            {
                "type": "text",
                "text": "Describe what is happening in this diagram:"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        ] }
    ],
    max_tokens=2000
)
response_message = response.choices[0].message.content
print(response_message)