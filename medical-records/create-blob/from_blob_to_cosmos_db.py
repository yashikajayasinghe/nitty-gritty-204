"""
This script is used only for the testing purpose.
Downloads a blob from the medics container in the storage account
and then upload data to the cosmos db 

"""
import os
import json
from azure.storage.blob import BlobClient
from azure.cosmos import CosmosClient

file_name = "<change create_and_upload_file_to_blob_storage.py to upload a file and add file name here>"

connection_string = os.getenv("AZURE_STORAGE_ACCOUNT_CONNECTION_STR")
blob = BlobClient.from_connection_string(
    conn_str=connection_string, container_name="medics", blob_name=file_name)
data_json_str = blob.download_blob()
data_dict = json.load(data_json_str)


# connect with cosmos db

COSMOS_ENDPOINT = "<COPY FROM AZ PORTAL>"
COSMOS_KEY = "<COPY FROM AZ PORTAL>"
COSMOS_DATABASE = "lipid-profiles"
COSMOS_CONTAINER = "Items"

client = CosmosClient(url=COSMOS_ENDPOINT, credential=COSMOS_KEY)

container = client.get_database_client(
    COSMOS_DATABASE).get_container_client(COSMOS_CONTAINER)
container.create_item(data_dict)

# Output:
# {'id': 'b1b2b3b4-b5b6-b7b8-b9b0-b1b2b3b4b5b6', 
# 'Patient': 'Sarah Gray', 'Age': 34, 
# 'ReportType': 'Lipid Blood Test', 
# 'Results': {'Cholesterol': 200, 'HDL': 50, 'LDL': 120, 'Triglycerides': 120}}
