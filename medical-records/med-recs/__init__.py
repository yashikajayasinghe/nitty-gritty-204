"""
This module contains the main application code for the medical records app.
"""
import json
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobClient


def fetch_data_from_blob_storage(event_data: dict):
    """
    This function downloads the blob from blob storage,
    process and returns in a format which is compatible for cosmos db insert.
    """
    file_name = event_data["url"].split("/")[4]
    logging.info('file name is: %s', file_name)

    connection_string = os.environ["AZURE_STORAGE_ACCOUNT_CONNECTION_STR"]

    blob = BlobClient.from_connection_string(
        conn_str=connection_string, container_name="medics", blob_name=file_name)
    data_json_str = blob.download_blob()
    data_dict = json.load(data_json_str)

    return data_dict


def main(event: func.EventGridEvent, newtestreport: func.Out[func.Document]):
    """
    This function will be triggered by an event emits by Azure EventGrid.

    Event data will be written to the logs.

    After processing the event data for 'med-recs' file location, the blob will be downloaded from the storage account, processed
    and then be uploaded to the cosmos db.
    """
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    logging.info('Python EventGrid trigger processed an event: %s', result)

    test_results = fetch_data_from_blob_storage(
        event.get_json())  # download blob from storage account

    logging.info('File has been read')

    newtestreport.set(func.Document.from_dict(
        test_results))  # upload to cosmos db

    logging.info('Following Data is Inserted into Cosmos DB: %s', test_results)

    # TODO:: blob should be deleted after successfully processed and uploaded to cosmos db
