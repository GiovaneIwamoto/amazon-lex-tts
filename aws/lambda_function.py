import requests

def lambda_handler(event, context):
    # API Text to Speech
    tts_api_url = "https://<YOUR_SERVERLESS>.execute-api.us-east-1.amazonaws.com/v1/tts"
            
    # Slack Web Hook
    slack_webhook_url = "https://hooks.slack.com/services/<YOUR_WEBHOOK>"
    
    # Get intent name
    intent_name = event['sessionState']['intent']['name']
    print("Intent Name: ",intent_name)
    
    if intent_name == 'BookTicket':
        # Get slots
        slots = event['sessionState']['intent']['slots']
        print("Slots: ",slots)
        
        destiny = slots.get('#FIXME:', {}).get('value', {}).get('interpretedValue', '')
        pass_type = slots.get('#FIXME', {}).get('value', {}).get('interpretedValue', '')
        first_name = slots.get('#FIXME', {}).get('value', {}).get('interpretedValue', '')
        data_travel = slots.get('#FIXME', {}).get('value', {}).get('interpretedValue', '')
        payment_type = slots.get('#FIXME', {}).get('value', {}).get('interpretedValue', '')

        # All slots filled
        if all([destiny, pass_type, first_name, data_travel, payment_type]):
            # Custom message
            message = "Perfect! Mr. %s, your ticket to %s in category %s, on %s for day %s has been successfully booked!" % (first_name, destiny, pass_type, payment_type, data_travel)
            print("Message sent to TTS API: ",message)
            
            # Post API Text to Speech
            tts_payload = {
                "phrase": message
            }
            tts_response = requests.post(tts_api_url, json=tts_payload)
            tts_response_data = tts_response.json()
            audio_url = tts_response_data['url_to_audio']
    
            # Post Slack Webhook
            slack_message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "🔉 Click to generate confirmation in audio format"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Play audio",
                                "emoji": True
                            },
                            "url": audio_url,
                            "action_id": "button-action"
                        }
                    }
                ]
            }
            requests.post(slack_webhook_url, json=slack_message)
        
        # Return Delegate to Lex
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    "name": event['sessionState']['intent']['name'],
                    "state": "InProgress",
                    "slots": event['sessionState']['intent']['slots']
                }
            }
        }

    return response