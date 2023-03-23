from django.conf import settings
import requests
import urllib.parse
import json

# sending the otp user mobile number
def send_message(message, phone_number):
    url = f"https://www.fast2sms.com/dev/bulkV2?authorization=MPz6zj2TX7VmU4kU0ED9k7IztZusXadifXQZW03GKdSmokLdRmYN4PpW01MK&variables_values={message}&route=otp&numbers={phone_number}"

    response = requests.request("GET", url)
    print(response.text)

    return json.loads(response.text).get("request_id")



# sending the otp user mobile number
def opt_in_gapshup( phone_number):

    url = f"https://media.smsgupshup.com/GatewayAPI/rest?method=OPT_IN&format=json&userid=2000190754&password=GQ3aGQeXK&phone_number=91{phone_number}&v=1.1&auth_scheme=plain&channel=WHATSAPP"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def gapshup_send_message( phone_number,msg):

    url = f"https://media.smsgupshup.com/GatewayAPI/rest?method=SendMessage&userid=2000190754&password=GQ3aGQeXK&CHANNEL=WHATSAPP&send_to={phone_number}&msg_type=HSM&msg={msg}&auth_scheme=plain&v=1.1"

    response = requests.request("POST", url)
    print(response.text)
    return response.text


def encoder_of_url(phone_number,test_list :list,date_time):
    print("phone_number",phone_number)
    # test_list=['1',"1"]
    f=""
    for test in range(len(test_list)):
        f=f+f"*{test_list[test].test}*  | "

    d=f"""👨🏻‍⚕️ 📃 🩸 Your personalized Testing Profile is here! 

*DISCOVER: Our algorithm developed by our team of doctors *  has suggested the following lab tests based on your answers 
{f}
TESTING


Let's get started with your journey towards good health and help you reach your health goals.
Discover suggests tests based on : 

1️⃣ Your health goal
2️⃣ Your answers 
3️⃣ Your demographic and lifestyle factors
4️⃣ Research evidence

Our team of doctors will be in touch with you shortly and will guide you on the next steps
    """
    print("",d)
    encoded_string = urllib.parse.quote(d)
    return gapshup_send_message(phone_number,encoded_string)