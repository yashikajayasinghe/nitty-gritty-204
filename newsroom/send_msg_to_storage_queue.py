"""
This script sends a message to a storage queue.
"""
import os
import uuid
import json
import base64
import time

from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy,
)

# Create the QueueClient
CONNECTION_STR = os.getenv("AZURE_STORAGE_ACCOUNT_CONNECTION_STR")
QUEUE_NAME = "queue-" + str(uuid.uuid4())


queue_client = QueueClient.from_connection_string(
    conn_str=CONNECTION_STR,
    queue_name=QUEUE_NAME,
    message_encode_policy=BinaryBase64EncodePolicy(),
    message_decode_policy=BinaryBase64DecodePolicy(),
)
queue_client.create_queue()
print(f"Queue: {QUEUE_NAME} is created.")

# Send a message to the queue
news = {
    "header": "This is a Breaking News Alert",
    "body": "This is the body of the alert",
    "link": "https://www.stuff.co.nz/",
    "linkText": "Click here to go to the news link",
    "messageType": "alert",
    "messageId": "1234567890"
}
news_str = json.dumps(news, indent=4)
queue_client.send_message(base64.b64encode(news_str.encode("utf-8")))

# peak the message then delete it
messages = queue_client.peek_messages()
for message in messages:
    print(base64.b64decode(message.content).decode('utf-8'))
    # queue_client.delete_message(message.id, None)

# Eventually Delete the queue
# time.sleep(10)
queue_client.delete_queue()
print(f"Queue: {QUEUE_NAME} is deleted eventually.")
