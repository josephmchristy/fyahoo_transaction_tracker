#! python

import os
import json
import gmail
from datetime import datetime
from fyahoo_query.query import FYahooQuery
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Get the player info from json data
def extract_player_info(players, new_trans):
    for player in players:
        tplayer = player['name']['full']
        player_ttype = player['transaction_data']['type']
        new_trans['players'].append((tplayer, player_ttype))
        if 'owner' not in new_trans:
            if player_ttype == 'drop':
                new_trans['owner'] = player['transaction_data']['source_team_name']
            elif player_ttype == 'add':
                new_trans['owner'] = player['transaction_data']['destination_team_name']


# Create transaction list from json data
def create_transactions_list(transactions):
    transactions_list = []
    transactions = transactions['transactions']['transaction']
    for transaction in transactions:
        new_trans = {}
        new_trans['type'] = transaction['type']
        if new_trans['type'] == 'commish':
            break
        new_trans['date'] = transaction['timestamp']
        new_trans['players'] = []
        players = transaction['players']
        player_list = []
        if players['@count'] == '1':
            player_list.append(players['player'])
        elif players['@count'] == '2':
            player_list = players['player']
        tplayer_list = extract_player_info(player_list, new_trans)
        transactions_list.append(new_trans)
    return transactions_list


# Get the most recent stored transaction date
def get_last_transaction_date():
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
        return prev_date


# Create a message from the most recent transactions
def create_message(transaction_list, prev_date):
    transaction_msg = ''
    # Print transactions following last transaction date
    for transaction in transactions_list:
        if datetime.fromtimestamp(int(transaction['date'])) > prev_date:
            for player in transaction['players']:
                if player[1] == 'add':
                    ttype = 'added'
                elif player[1] == 'drop':
                    ttype = 'dropped'
                towner = transaction['owner']
                tplayer = player[0]
                tdate = datetime.fromtimestamp(int(transaction['date']))
                tmsg = '{} {} {} at {}\n'.format(towner, ttype, tplayer, tdate)
                transaction_msg += tmsg
    return transaction_msg


# Send the transaction message to email addresses
def send_transactions(transaction_msg):
    # Send the new transactions, if there are any
    if transaction_msg != '':
        to = "josephmchristy@gmail.com"
        sender = "josephmchristy@gmail.com.com"
        subject = "subject"
        gmail.SendMessage(sender, to, subject, msgHtml=None, msgPlain=transaction_msg)
        # Store the current last transaction date
        curr_date = datetime.timestamp(list(reversed(transactions_list))[-1]['date'])
        with open('last_transaction_date.txt', 'w') as last_trans:
            print(curr_date, file=last_trans)


nba = FYahooQuery(30024, 'nba')
transactions = json.loads(nba.get_league_transactions())
transactions_list = create_transactions_list(transactions)
prev_date = get_last_transaction_date()
transaction_msg = create_message(transactions_list, prev_date)
print (transaction_msg)
