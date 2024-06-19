import json

def v1_description(event, context):
    body = {
        "message": "TTS api version 1.0"
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
