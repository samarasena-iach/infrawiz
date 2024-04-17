from configurations.azure_storage import *
from azure.storage.blob import BlobServiceClient
import os
import time

os.environ['SSL_CERT_FILE'] = 'C:/Users/AU256UR/AppData/Local/Programs/Python/Python312/Lib/site-packages/certifi/cacert.pem'


def uploadArchitectureDiagramToAzureBlobStorage(file_path, file_name):
    current_time_ms = int(round(time.time() * 1000))
    file_name = str(current_time_ms)+"_"+file_name

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    print("Uploaded File: " + file_name)

    return blob_client.url

# uploadToBlobStorage("C:\\Users\\AU256UR\\Downloads\\sample_architecture_diagram.png", "sample_architecture_diagram.png")
