from django.conf import settings
import requests

import json

# sending the otp user mobile number
def send_message(message, phone_number):
    url = f"https://www.fast2sms.com/dev/bulkV2?authorization=MPz6zj2TX7VmU4kU0ED9k7IztZusXadifXQZW03GKdSmokLdRmYN4PpW01MK&variables_values={message}&route=otp&numbers={phone_number}"

    response = requests.request("GET", url)
    print(response.text)

    return json.loads(response.text).get("request_id")

