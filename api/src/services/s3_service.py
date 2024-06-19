import boto3

def upload_to_s3(bucket_name, file_name, audio_stream):
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=audio_stream)
