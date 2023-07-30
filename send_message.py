from twilio.rest import Client

account_sid = ''
auth_token = ''
sender_phone_number = ''
recipient_phone_number = ''  # Will be replaced by emergency contact's number: 112 in India. 

def send_sms(message):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body = message,
            from_ = sender_phone_number,
            to = recipient_phone_number
        )

        print("SMS Sent Successfully")
    except Exception as e:
        print("Failed to send SMS")
