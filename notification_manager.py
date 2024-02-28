import os
from twilio.rest import Client


class NotificationManager:
    def __init__(self, body, from_number, to):
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]

        client = Client(account_sid, auth_token)

        self.body = body
        self.from_number = from_number
        self.to = to

        message = client.messages \
            .create(
            body=self.body,
            from_=self.from_number,
            to=self.to
        )
