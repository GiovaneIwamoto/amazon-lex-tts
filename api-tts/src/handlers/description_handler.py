import json

def v1_description(event, context):
    body = {
        "message": "Text to Speech"
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
