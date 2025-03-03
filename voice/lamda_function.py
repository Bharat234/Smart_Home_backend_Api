def lambda_handler(event, context):
    if event['directive']['header']['namespace'] == 'Alexa.PowerController':
        # Handle power control (e.g., turn on/off smart plug)
        return {
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "messageId": event['directive']['header']['messageId'],
                    "payloadVersion": "3"
                },
                "payload": {}
            }
        }
    elif event['directive']['header']['namespace'] == 'Alexa.Authorization':
        # Handle OAuth2 token validation
        return {
            "event": {
                "header": {
                    "namespace": "Alexa.Authorization",
                    "name": "AcceptGrant.Response",
                    "messageId": event['directive']['header']['messageId'],
                    "payloadVersion": "3"
                },
                "payload": {}
            }
        }