"""
This module contains the main application code for the medical records app.
"""
import json
import logging

import azure.functions as func


def main(event: func.EventGridEvent):
    """
    This function will be triggered by an EventGrid event with the subject 
    "sample". The event data will be written to the logs.
    """
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    logging.info('Python EventGrid trigger processed an event: %s', result)
