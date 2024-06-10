import json

def health(event, context):
    body = {
        "message": "Serverless executed successfully!",
        "input": event,
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
