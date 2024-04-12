from configurations.azure_storage import *
from azure.storage.blob import BlobServiceClient
import os

os.environ['SSL_CERT_FILE'] = 'C:/Users/AU256UR/AppData/Local/Programs/Python/Python312/Lib/site-packages/certifi/cacert.pem'


def uploadToBlobStorage(file_path, file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    print("Uploaded File: " + file_name)

    return blob_client.url


# uploadToBlobStorage("C:\\Users\\AU256UR\\Downloads\\ey_nexus_architecture_diagram_01.png",
#                     "ey_nexus_architecture_diagram_01.png")
