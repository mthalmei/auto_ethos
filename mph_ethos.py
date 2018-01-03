#!/bin/python2
import requests
import sys

currency = 'EUR'
power_cost = 0.15

hashes = {
        'RX470' : {
            'Cryptonight': { 'hash': 700.0 / (1000 * 1000 * 1000), 'power': 90 },
            'Ethash': { 'hash': 27.0 / 1000, 'power': 120 },
            },
        # '1070': {
        # 'Ethash': { 'hash': 30.0 / 1000, 'power': 120 },
        # 'Groestl': { 'hash': 35.5 / 1000, 'power': 130 },
        # 'X11': { 'hash': 11.5 / 1000, 'power': 120 },
        # 'Cryptonight': { 'hash': 500.0 / (1000 * 1000 * 1000), 'power': 100 },
        # 'Equihash': { 'hash': 430.0 / (1000 * 1000 * 1000), 'power': 120 },
        # 'Lyra2RE2': { 'hash': 35.5 / 1000, 'power': 130 },
        # 'NeoScrypt': { 'hash': 1000.0 / ( 1000 * 1000), 'power': 155 },
        # },
        '1070ti': {
            'Lyra2RE2': { 'hash': 41.0 / 1000, 'power': 110 },
            'Equihash': { 'hash': 500.0 / (1000 * 1000 * 1000), 'power': 115 },
            'Cryptonight': { 'hash': 600.0 / (1000 * 1000 * 1000), 'power': 100 },
            'Lyra2z': { 'hash': 2250.0 / (1000 * 1000), 'power': 100 },
            },
        '1080ti': {
            'Lyra2RE2': { 'hash': 56.1 / 1000, 'power': 150 },
            'Equihash' : { 'hash': 680.0 / (1000 * 1000 * 1000), 'power': 190 },
            'Cryptonight': { 'hash': 830.0 / (1000 * 1000 * 1000), 'power': 140 },
            'Lyra2z': { 'hash': 3200.0 / (1000 * 1000), 'power': 140 },
            },
        }

if len(sys.argv) < 2 or not sys.argv[1] in hashes.keys():
    print('Need to give exactly one card: ' + ', '.join(hashes.keys()))
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

row_format_headers = '{:<14}{:>14}{:>14}{:>14}' + '{:>14}' * 3
row_format = '{:<14}{:>14.8f}{:>14.8f}{:>14.8f}' + '{:>14.8f}' * 3
print row_format_headers.format(*headers)

if rj['success']:
    for algo in rj['return']:
        fields = [algo['algo'], algo['profit'], algo['normalized_profit_amd'], algo['normalized_profit_nvidia']]

        rev = 0
        cost = 0
        prof = 0
        if algo['algo'] in hashes[card]:
            rev = algo['profit'] * hashes[card][algo['algo']]['hash']
            cost = hashes[card][algo['algo']]['power'] * 24 * power_cost / 1000 / bc_rate
            prof = rev - cost
        fields.append(rev)
        fields.append(cost)
        fields.append(prof)

        print row_format.format(*fields)
