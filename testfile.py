#! python

import json
import pprint
from fyahoo_query.query import FYahooQuery


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

transactions_list = []
nba = FYahooQuery(30024, 'nba')
transactions = json.loads(nba.get_league_transactions())
transactions = transactions['transactions']['transaction']
for transaction in transactions:
    new_trans = {}
    new_trans['type'] = transaction['type']
    if new_trans['type'] == 'commish':
        break
    new_trans['time'] = transaction['timestamp']
    new_trans['players'] = []
    players = transaction['players']
    player_list = []
    if players['@count'] == '1':
        player_list.append(players['player'])
    elif players['@count'] == '2':
        player_list = players['player']
    tplayer_list = extract_player_info(player_list, new_trans)
    transactions_list.append(new_trans)
pprint.pprint(transactions_list[:20])
