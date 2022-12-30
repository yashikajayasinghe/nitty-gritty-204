# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging


def main(name: str) -> str:
    """
    function that is called when the Approval function doesn't respond within 20 seconds.
    """
    logging.info("Escalation task has been triggered.")
    
    return f"ESCALATION : You have not approved the project design proposal - reassigning to your Manager: {name}!"
