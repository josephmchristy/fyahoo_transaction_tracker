#! python

import os
from twilio.rest import Client

account_sid = 'ACe39054eb41c155e27fcfbd60f9a1bd19'
auth_token = '7a300cc61fe0378ba6fa2f653b2fad48'
client = Client(account_sid, auth_token)

message = client.messages.create(to='+17147681680', from_='+17144850867', body='This is a test.')

print(message.sid)
