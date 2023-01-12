"""
This script creates a file in the current directory and uploads it to a blob storage container.
"""
import os
import uuid
import random
import json
import time
from azure.storage.blob import BlobClient

# generates a random data set
first_names_set = ["Elaine", "Sarah", "Jack", "Clayton", "John"]
last_names_set = ["Mills", "Gray", "Middleton", "Rich"]
first_name = random.choice(first_names_set)
last_name = random.choice(last_names_set)
name: str = first_name+" "+last_name
test_report_dict = {
    "Patient": name,
    "Age": random.randint(25, 50),
    "ReportType": "Lipid Blood Test",
    "Results": {
        "Cholesterol": random.randint(180, 240),
        "HDL": random.randint(40, 70),
        "LDL": random.randint(100, 160),
        "Triglycerides": random.randint(100, 180)
    }
}

# Creates a local directory - (if not exist) -to hold data files.
# getcwd() returns the current working directory.
dir_path = os.path.join(os.getcwd(), "data")
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)

# Creates a json file in the local directory.
file_name = str(uuid.uuid4()) + "_"+ first_name + "_"+last_name + "_med_recs.json"
local_file_path = os.path.join(dir_path, file_name)
with open(local_file_path, "w") as f:
    json.dump(test_report_dict, f, indent=4)
    f.close()

time.sleep(5)

# Gets a reference to a BlobClient using a connection string.

connection_string = os.getenv("AZURE_STORAGE_ACCOUNT_CONNECTION_STR")
blob = BlobClient.from_connection_string(
    conn_str=connection_string, container_name="medics", blob_name=file_name)

# Uploads the local json file to the blob by calling the upload_blob method.
with open(local_file_path, "rb") as data:
    blob.upload_blob(data)
    data.close()
