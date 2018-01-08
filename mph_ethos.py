#!/usr/bin/python2
import requests
import sys
import hashrate_db

currency = 'EUR'
power_cost = 0.15

if len(sys.argv) < 2 or not sys.argv[1].lower() in hashrate_db.cards():
    print('Need to give exactly one card: ' + ', '.join(hashrate_db.cards()))
    exit(0)
card = sys.argv[1]

r = requests.get('https://blockchain.info/de/ticker')
rj = r.json()
bc_rate = rj[currency]['15m']
print "Bitcoin price: {} {}/BTC\n".format(bc_rate, currency)

r = requests.get('https://miningpoolhub.com/index.php?page=api&action=getautoswitchingandprofitsstatistics')
rj = r.json()

headers = ['Algo', 'Profit', 'AMD', 'NVIDIA' ]
headers.append(card + " rev")
headers.append(card + " cost")
headers.append(card + " profit")
headers.append(card + " " + currency)

row_format_headers = '{:<14}{:>14}{:>14}{:>14}' + '{:>14}' * 4
row_format = '{:<14}{:>14.8f}{:>14.8f}{:>14.8f}' + '{:>14.8f}' * 4
print row_format_headers.format(*headers)

if rj['success']:
    for algo in rj['return']:
        fields = [algo['algo'], algo['profit'], algo['normalized_profit_amd'], algo['normalized_profit_nvidia']]

        rev = 0
        cost = 0
        prof = 0
        prof_cur = 0
        if algo['algo'].lower() in hashrate_db.algos(card):
            rev = algo['profit'] * hashrate_db.hashrate(card, algo['algo'])
            cost = hashrate_db.power(card, algo['algo']) * 24 * power_cost / 1000 / bc_rate
            prof = rev - cost
            prof_cur = prof * bc_rate
        fields.append(rev)
        fields.append(cost)
        fields.append(prof)
        fields.append(prof_cur)

        if rev != 0:
            print row_format.format(*fields)
