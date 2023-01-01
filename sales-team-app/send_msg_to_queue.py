"""
This script sends a message to the queue
"""
# Path: sales-team-app/receive_msg_from_queue.py
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = os.getenv("AZURE_SERVICEBUS_CONNECTION_STRING")
QUEUE_NAME = "salesmessages"

with ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR) as client:
    with client.get_queue_sender(queue_name=QUEUE_NAME) as sender:
        message = ServiceBusMessage("$10,000 order for bicycle parts from retailer Adventure Works.")
        sender.send_messages(message)
        print("Message sent")


