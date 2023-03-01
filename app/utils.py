from django.conf import settings
import requests

import json

# sending the otp user mobile number
def send_message(message, phone_number):
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = f"message={message}&language=english&route=q&numbers={phone_number},"
    headers = {
        "authorization": settings.FAST_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

    return json.loads(response.text).get("request_id")

