from azure.eventhub import EventHubProducerClient, EventData
import os

# Get the connection string from an environment variable.
EVENT_HUB_NAMESPACE_CONNECTION_STR = os.getenv(
    "AZURE_EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = "e-hub-one"

# Create a producer client to send messages to the event hub.
producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_NAMESPACE_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)

# Create a batch.
event_data_batch = producer.create_batch()
event_data_batch.add(
    EventData('A Payment of $100 has been received to Savings Account.'))
event_data_batch.add(
    EventData('A Payment of $200 has been received to Checking Account.'))
event_data_batch.add(
    EventData('A Payment of $300 has been received to Credit Card Account.'))
event_data_batch.add(
    EventData('A Payment of $400 has been received to Loan Account.'))
event_data_batch.add(
    EventData('A Payment of $500 has been received to Mortgage Account.'))
event_data_batch.add(
    EventData('A Payment of $600 has been received to Investment Account.'))

# Send the batch of events to the event hub.
with producer:
    producer.send_batch(event_data_batch)
    print('A batch of 6 events has been published.')
