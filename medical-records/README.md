## Medical Records App

#### *Scenario:*

1. A Lab Technician uploads a medical record to the Azure blob storage account
2. Azure Blob Storage as the Event Source, sends this upload event to the Azure Event Grid Topic
3. Function App 'med-recs' is subscribed as the event handler for that Azure Event Grid Topic ('med-recs' is an Event Grid Triggered Function App)
4. When triggered by the blob create event, 'med-recs' will fetch the file from the blob storage, process it and feeds it to the cosmos DB. 'med-recs' has output binding to Cosmos DB


#### Steps:

1. Create Azure Storage Account
2. Create Event Grid Triggered Azure Function App (Name: med-recs)
3. Create Event Grid System Topic: ref: https://learn.microsoft.com/en-us/azure/event-grid/create-view-manage-system-topics#create-a-system-topic
4. Create Event Subscription - ref: https://learn.microsoft.com/en-us/azure/event-grid/create-view-manage-system-topics#create-an-event-subscription 
5. Add Event filter to the subscription: https://learn.microsoft.com/en-us/azure/event-grid/event-filtering
```
"filter": {
    "subjectBeginsWith": "/blobServices/default/containers/medics/blobs",
    "subjectEndsWith": ".json"
    }
```
6. Manually create a blob in the storage and monitor `med-recs`'s app insights logs to verify the successful integration
7. Implement a python function to upload a custom file to the blob storage (included in create-blob/create_and_upload_file_to_blob_storage.py )
8. Add cosmos db output binding to the function app.
9. Add cosmosdb Connection string to app settings : https://learn.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-cosmos-db-vs-code?tabs=in-process&pivots=programming-language-csharp#update-your-function-app-settings
10. E2E data flow verification: Random data generated when running create_and_upload_file_to_blob_storage.py will be inserted in to the cosmos db.

### Other Ref:

1. https://learn.microsoft.com/en-us/azure/event-grid/event-schema
2. https://learn.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&tabs=event-grid-event-schema
3. https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview
4. https://learn.microsoft.com/en-us/azure/event-grid/system-topics
5. https://learn.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python
