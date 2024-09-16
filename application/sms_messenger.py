# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from filefuncs import read_smsnums

#from twilio.rest import Client
from filefuncs import read_smsnums


def sms_client():
    contents = read_smsnums()
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ.get('TwilioAccountSID')
    auth_token = os.environ.get('TwilioAuthToken')
    twilio_phone_num = os.environ.get('TwilioPhoneNumber')
    client = Client(account_sid, auth_token)

    for number in contents:

        message = client.messages.create(
            from_=twilio_phone_num,
            body='person in the zone',
            to=f'{number}'
        )
        
