"""
Azure Functions HTTP trigger Python sample.
"""
import logging
import json
import azure.functions as func


def main(
    request: func.HttpRequest,
    bookmark: func.DocumentList,
    newbookmark: func.Out[func.Document],
) -> func.HttpResponse:
    """HTTP trigger function to find a bookmark in the database.
    ref: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-input?tabs=in-process%2Cfunctionsv2&pivots=programming-language-python#http-trigger-look-up-id-from-query-string-python

    The requests pass in the desired key, or ID, along with the bookmark URL. The function
    responds with a message if the key already exists in our back end.
    If the key that was passed to us is not found, we'll add the new bookmark to our database.
    """

    logging.info("Python HTTP trigger function processed a request.")
    if request.method == "POST":
        try:
            id = request.params.get("id")
            if not bookmark:
                request_body = request.get_json()
                bookmark_string = {
                    "url": request_body["url"],
                    "id": id,
                }
                newbookmark.set(func.Document.from_dict(bookmark_string))
                return func.HttpResponse(
                    "A bookmark related to the searched id was not found. Hence, it's been added to the db",
                    status_code=200,
                    mimetype="application/json",
                )
            else:
                return func.HttpResponse(
                    "Bookmark already exists.",
                    status_code=422,
                    mimetype="application/json",
                )
        except ValueError:
            return func.HttpResponse(
                "Invalid request", status_code=400, mimetype="application/json"
            )

    else:
        return func.HttpResponse(
            "Only POST requests are accepted",
            status_code=405,
            mimetype="application/json",
        )
    # VERSION :1 of the code
    # if request.method == "POST":
    #     try:
    #         req_body = request.get_json()
    #         if "url"in req_body and "id" in req_body:
    #             new_body = {"url": req_body["url"]}
    #             return func.HttpResponse(
    #                 json.dumps(new_body, indent=4),
    #                 status_code=200,
    #                 mimetype="application/json",
    #             )

    #         else:
    #             return func.HttpResponse(
    #                 "Invalid request body",
    #                 status_code=400,
    #                 mimetype="application/json",
    #             )

    #     except ValueError:
    #         return func.HttpResponse(status_code=400, mimetype="application/json")
    # else:
    #     return func.HttpResponse(status_code=405, mimetype="application/json")
