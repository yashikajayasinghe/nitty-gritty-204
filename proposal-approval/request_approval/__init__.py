# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
#  https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode?tabs=linux

import logging
import json
from datetime import timedelta
import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    """
    if the Approval function doesn't respond within 20 seconds,
    the Escalation function is called.
    It also changes the call to Approval function to wait for an external input.

    The context object in Python represents the orchestration context. 
    Access the main Azure Functions context using the function_context property on the orchestration context.
    Context object can be used to invoke other functions by name, pass parameters, and return function output.
    """
    # Put the orchestrator to sleep for 20 secs
    # Orchestrations will continue to process other incoming events while waiting for a timer task to expire.
    due_by = context.current_utc_datetime + timedelta(seconds=20)
    durable_timeout_task = context.create_timer(due_by)
    activity_task = context.wait_for_external_event("Approval")
    # The task_any function returns the first task that completes.
    # get the first result, then come back to the beginning where it can be checked if there are more things to do. 
    # If there are, then push those.
    winner = yield context.task_any([durable_timeout_task, activity_task])
    result = []
    if(winner == activity_task):
        logging.info("Activity Task Approval/Rejection received!")
        result = yield context.call_activity("Approval", "Approved")
    else:
        logging.info("Timeout Task received!")
        result2 = yield context.call_activity("Escalation", "Manager")
        result.append(result2)
    
    if(not durable_timeout_task.is_completed):
        logging.info("Timeout Task completed!")
        #  All pending timers must be complete or canceled before the function exits.
        durable_timeout_task.cancel()

    return [result]

main = df.Orchestrator.create(orchestrator_function)
