from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusSender
import os

CONNECTION_STR = os.getenv("AZURE_SERVICEBUS_CONNECTION_STRING")
TOPIC_NAME = "salesperformancemessages"
SUBSCRIPTION_NAME = "EuropeAndAsia"

SB_CLIENT = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

def send_single_message(sender:ServiceBusSender):
    """
    a function to send a single message
    """
    message = ServiceBusMessage("Didn't know you were using mushroom out of cans. I don't like that pizza.")
    sender.send_messages(message)
    print("Sent a single message")

def send_message_to_topic():
    """
    This function sends a message to the topic
    """

    with SB_CLIENT.get_topic_sender(topic_name=TOPIC_NAME) as sender:
        with sender:
            send_single_message(sender)

def receive_message_from_subscription():
    """
    This function receives a message from the subscription
    """

    with SB_CLIENT:
        receiver = SB_CLIENT.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                print("Received: " + str(msg))
                receiver.complete_message(msg)

if __name__ == '__main__':
    send_message_to_topic()
    receive_message_from_subscription()