#! python

import os
import ffyahoo
import gmail
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

transactions_list = ffyahoo.getTransactions('2020')

# If there is no previous transaction date stored, store it
if not os.path.isfile('last_transaction_date.txt'):
    prev_date = datetime.timestamp(transactions_list[-1]['date'])
    with open('last_transaction_date.txt', 'w') as last_trans:
        print(prev_date, file=last_trans)

# Get the last transaction date
with open('last_transaction_date.txt', 'r') as last_trans:
    prev_date = last_trans.readline().split(".",1)
    prev_date = int(prev_date[0])
    prev_date = datetime.fromtimestamp(prev_date)

msgPlain = ''
# Print transactions following last transaction date
for transaction in transactions_list:
    if transaction['date'] > prev_date:
        if transaction['type'] == 'add':
            ttype = 'added'
        elif transaction['type'] == 'drop':
            ttype = 'dropped'
        towner = transaction['owner']
        tplayer = transaction['player']
        tdate = transaction['date']
        tmsg = '{} {} {} at {}\n'.format(towner, ttype, tplayer, tdate)
        msgPlain += tmsg

print (msgPlain)

# Send the new transactions, if there are any
if msgPlain != '':
    to = "josephmchristy@gmail.com"
    sender = "josephmchristy@gmail.com.com"
    subject = "subject"
    gmail.SendMessage(sender, to, subject, msgHtml=None, msgPlain=msgPlain)
    # Store the current last transaction date
    curr_date = datetime.timestamp(list(reversed(transactions_list))[-1]['date'])
    with open('last_transaction_date.txt', 'w') as last_trans:
        print(curr_date, file=last_trans)

