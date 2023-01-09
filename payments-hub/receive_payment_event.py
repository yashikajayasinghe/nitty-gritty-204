import os
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore

CONNECTION_STR = os.getenv(
    "AZURE_EVENT_HUB_CONNECTION_STR")
EVENTHUB_NAME = "e-hub-one"
STORAGE_CONNECTION_STR = os.getenv("AZURE_STORAGE_ACCOUNT_CONNECTION_STR")
# the blob container resource should pre-exist
BLOB_CONTAINER_NAME = "checkpointstore-one"

def on_event(partition_context, event):
    """Callback for receiving events"""

    print("Received event from partition: {}.".format(
        partition_context.partition_id))
    partition_context.update_checkpoint(event)

# Create a consumer client for the event hub.
consumer_client = EventHubConsumerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    consumer_group='$Default',
    eventhub_name=EVENTHUB_NAME,
    checkpoint_store=BlobCheckpointStore.from_connection_string(STORAGE_CONNECTION_STR, BLOB_CONTAINER_NAME))

try:
    with consumer_client:
        # Call the receive method. This method waits indefinitely for events to be received.
        # The received events are passed to the on_event callback.
        consumer_client.receive(on_event=on_event, starting_position="-1")
except KeyboardInterrupt:
    print('Stopped receiving.')
