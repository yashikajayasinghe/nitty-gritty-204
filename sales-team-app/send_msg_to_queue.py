"""
This script sends a message to the queue
"""
# Path: sales-team-app/receive_msg_from_queue.py
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = os.getenv("AZURE_SERVICEBUS_CONNECTION_STRING")
QUEUE_NAME = "salesmessages"
SB_CLIENT = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

def send_msg_to_queue():
    """
    This function sends a message to the queue
    """

    with SB_CLIENT.get_queue_sender(queue_name=QUEUE_NAME) as sender:
        message = ServiceBusMessage("$10,000 order for bicycle parts from retailer Adventure Works.")
        sender.send_messages(message)
        print("Message sent")

def receive_message_from_queue():
    """
    This function receives a message from the queue
    """

    with SB_CLIENT.get_queue_receiver(queue_name=QUEUE_NAME) as receiver:
        messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
        for orgmessage in messages:
            print(f"Message received: {orgmessage}")

if __name__ == '__main__':
    send_msg_to_queue()
    receive_message_from_queue()
