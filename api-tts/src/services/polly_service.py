import boto3

def synthesize_speech(text):
    polly_client = boto3.client("polly")
    response = polly_client.synthesize_speech(
        Engine='neural',   
        Text=text,
        OutputFormat='mp3',
        VoiceId='Thiago'
    )
    return response['AudioStream'].read()
