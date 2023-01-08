# Newsroom with Azure Storage Queue 

> ref: 
> 1. https://learn.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage?tabs=python%2Cenvironment-variable-linux
> 2. https://learn.microsoft.com/en-us/training/modules/communicate-between-apps-with-azure-queue-storage/1-introduction

### *Azure Storage Queue*

#### Run Python

```
python process_message_in_storage_queue.py
```

#### Output:

```
Queue: queue-<with-unique-id> is created.

{
    "header": "This is a Breaking News Alert",
    "body": "This is the body of the alert",
    "link": "https://www.stuff.co.nz/",
    "linkText": "Click here to go to the news link",
    "messageType": "alert",
    "messageId": "1234567890"
}

Queue: queue-<with-unique-id> is deleted eventually.
```