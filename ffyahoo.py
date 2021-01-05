#! python

import xml.etree.ElementTree as ET
import re
import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

from yahoo_oauth import OAuth2

oauth = OAuth2(None, None, from_file='private.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

url = "https://fantasysports.yahooapis.com/fantasy/v2"
game_league_ids = {
        '2020': ('402', '30024') 
        }

# Get the transactions for the league
def getTransactions(year):
    g_id = game_league_ids[year][0]
    l_id = game_league_ids[year][1]
    req_url = url + "/league/"+g_id+".l."+l_id+"/transactions"
    r=oauth.session.get(req_url)
    xmlstring = r.text
    xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)
    root = ET.fromstring(xmlstring)
    transactions_list = []
    for transaction in root.iter('transaction'):
        # For all add/drop or trade transactions
        transaction_type = transaction.find('type').text
        if transaction_type != 'commish':
            # Get the transaction date
            transaction_timestamp = transaction.find('timestamp').text
            transaction_date = datetime.datetime.fromtimestamp(int(transaction_timestamp))
            # Get each player in the transaction
            players = transaction.find('players')
            for player in players:
                transaction_data = player.find('transaction_data')
                # Get the player's name
                player_name = player.find('name')
                p_transaction_name = player_name.find('full').text
                # Get the transaction type (add, drop, or trade)
                p_transaction_type = transaction_data.find('type').text
                # If a player is added via trade or add, get the new owner and check for waiver
                if p_transaction_type == 'add':
                    p_transaction_owner = transaction_data.find('destination_team_name').text
                    p_source_type = transaction_data.find('source_type').text
                    if p_source_type == 'waivers':
                        p_transaction_type = 'waiver'
                # If a player is dropped
                else:
                    p_transaction_owner = transaction_data.find('source_team_name').text
                # Add player transaction data to the transactions list
                p_transaction = {'date': transaction_date, 'type': p_transaction_type,
                                 'owner': p_transaction_owner, 'player': p_transaction_name}
                transactions_list.append(p_transaction)
    return transactions_list

#transactions_list = getTransactions('2020')
#for transaction in transactions_list:
#    print(transaction)

