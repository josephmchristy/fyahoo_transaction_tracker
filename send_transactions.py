#! python

import os
import ffyahoo
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

# Print transactions following last transaction date
for transaction in transactions_list:
    if transaction['date'] > prev_date:
        print(transaction)

# Store the current last transaction date
curr_date = datetime.timestamp(transactions_list[-1]['date'])
with open('last_transaction_date.txt', 'w') as last_trans:
    print(curr_date, file=last_trans)
