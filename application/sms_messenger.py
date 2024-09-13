# Download the helper library from https://www.twilio.com/docs/python/install
import os
#from twilio.rest import Client
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
    #client = Client(account_sid, auth_token)

    for number in contents:
        print(number)
        """
        message = client.messages.create(
            from_=twilio_phone_num,
            body='person in the zone',
            to=f'{number}'
        )
        """
        print("sent message")



"""


def sms_client():
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC236b69f98b25a4d0f4656f204038d0f5'
    auth_token = '7d86ca4cb929bbf8874b271929cfcbaf'
    #account_sid = os.environ['TWILIO_ACCOUNT_SID']
    #auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    phone_numbers = read_smsnums()
    print(phone_numbers)
    for number in phone_numbers:
        message = client.messages \
                        .create(
                             body="Person in the zone.",
                             from_='+18668402379',
                             to=str(number)
                         )

        print(message.sid)













from twilio.rest import Client

account_sid = 'AC236b69f98b25a4d0f4656f204038d0f5'
auth_token = '7d86ca4cb929bbf8874b271929cfcbaf'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18668402379',
  body='person in the zone',
  to=str()
)

print(message.sid)























from twilio.rest import Client
from filefuncs import read_smsnums

def sms_clientttt():
    contents = read_smsnums()
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC236b69f98b25a4d0f4656f204038d0f5'
    auth_token = '7d86ca4cb929bbf8874b271929cfcbaf'
    client = Client(account_sid, auth_token)
    
    for number in contents:
    messageeee = client.messages.create(
        from_='+18668402379',
        body='person in the zone',
        to=str(number)
    )

    print(message.sid)

"""