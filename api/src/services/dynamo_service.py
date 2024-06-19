import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = os.getenv('DYNAMODB_TABLE')
print(f"DynamoDB Table: {table_name}")

table = dynamodb.Table(table_name)

def check_audio_exists(unique_id):
    response = table.get_item(Key={'id': unique_id})
    return response.get('Item')

def save_audio_record(item):
    table.put_item(Item=item)
