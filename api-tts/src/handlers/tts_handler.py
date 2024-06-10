import json
from datetime import datetime
from src.services.polly_service import synthesize_speech
from src.services.s3_service import upload_to_s3
from src.services.dynamo_service import check_audio_exists, save_audio_record
from src.utils.id_generator import generate_id
import os

def v1_text_to_speech(event, context):
    bucket_name = os.getenv('S3_BUCKET')
    bucket_url = f"https://{bucket_name}.s3.amazonaws.com"
    print(f"S3 bucket: {bucket_name}")

    # Parse the raw body to get the text
    try:
        body = json.loads(event['body'])
        phrase = body['phrase']
        
        if not phrase.strip():
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Phrase cannot be empty."})
            }
    
    except (json.JSONDecodeError, KeyError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input format."})
        }

    # Generate ID Using Hash
    unique_id = generate_id(phrase)
    
    try:
        # Check if the audio already exists in DynamoDB
        item = check_audio_exists(unique_id)
        if item:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "received_phrase": item['received_phrase'],
                    "url_to_audio": item['url_to_audio'],
                    "created_audio": item['created_audio'],
                    "unique_id": item['id']
                })
            }
        
        # Synthesize speech using Amazon Polly
        audio_stream = synthesize_speech(phrase)

        # Create a unique filename
        file_name = f"{unique_id}.mp3"
        
        # Upload the file to S3
        upload_to_s3(bucket_name, file_name, audio_stream)

        # Record creation time
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Register the audio in DynamoDB
        item = {
            'id': unique_id,
            'received_phrase': phrase,
            'url_to_audio': f"{bucket_url}/{file_name}",
            'created_audio': created_time
        }
        save_audio_record(item)

        # Prepare the response object
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "received_phrase": phrase,
                "url_to_audio": f"{bucket_url}/{file_name}",
                "created_audio": created_time,
                "unique_id": unique_id
            })
        }
    
    except Exception as e:
        # Handle any exceptions that occur
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    return response
