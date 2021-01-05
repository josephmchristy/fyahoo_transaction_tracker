#! python

import os
from twilio.rest import Client

account_sid = 'ACe39054eb41c155e27fcfbd60f9a1bd19'
auth_token = '7a300cc61fe0378ba6fa2f653b2fad48'
client = Client(account_sid, auth_token)

def sendSMS(body_text):
    message = client.messages.create(to='+17147681680', from_='+17144850867', body=body_text)
    print(message.sid)

text = "Henlo!"
sendSMS(text)
