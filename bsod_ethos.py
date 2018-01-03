#!/usr/bin/python2
import requests
import sys

currency = 'EUR'
power_cost = 0.15

hashes = {
        'RX470' : {
            'cryptonight': { 'hash': 700.0 / (1000 * 1000 * 1000), 'power': 90 },
            'ethash': { 'hash': 27.0 / 1000, 'power': 120 },
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
            'nist5': { 'hash': 41.0 / 1000, 'power': 110 },
            'xevan': { 'hash': 4 / 1000, 'power': 155 },
            'neoscrypt': { 'hash': 1.2 / 1000, 'power': 140 },
            'lyra2v2': { 'hash': 41.0 / 1000, 'power': 110 },
            'equihash': { 'hash': 500.0 / (1000 * 1000 * 1000), 'power': 115 },
            'cryptonight': { 'hash': 600.0 / (1000 * 1000 * 1000), 'power': 100 },
            'lyra2z': { 'hash': 2250.0 / (1000 * 1000), 'power': 100 },
            },
        '1080ti': {
            'nist5': { 'hash': 56.1 / 1000, 'power': 150 },
            'skunk': { 'hash': 47.5 / 1000, 'power': 190 },
            'xevan': { 'hash': 5 / 1000, 'power': 200 },
            'neoscrypt': { 'hash': 1.5 / 1000, 'power': 210 },
            'lyra2v2': { 'hash': 56.1 / 1000, 'power': 150 },
            'equihash' : { 'hash': 680.0 / (1000 * 1000 * 1000), 'power': 190 },
            'cryptonight': { 'hash': 830.0 / (1000 * 1000 * 1000), 'power': 140 },
            'lyra2z': { 'hash': 3200.0 / (1000 * 1000), 'power': 140 },
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

r = requests.get('http://bsod.pw/api/currencies')
rj = r.json()

headers = ['currency', 'algo', 'estimate']
headers.append(card + " rev")
headers.append(card + " cost")
headers.append(card + " profit")
headers.append(card + " " + currency)

row_format_headers = '{:<14}{:<14}{:>14}' + '{:>14}' * 4
row_format = '{:<14}{:<14}{:>14.8f}' + '{:>14.8f}' * 4
print row_format_headers.format(*headers)


if rj:
    for coin in rj.keys():
        algo = rj[coin]
        fields = [coin, algo['algo'], float(algo['estimate'])]

        rev = 0
        cost = 0
        prof = 0
        prof_cur = 0
        if algo['algo'] in hashes[card]:
            rev = float(algo['estimate']) * hashes[card][algo['algo']]['hash']
            cost = hashes[card][algo['algo']]['power'] * 24 * power_cost / 1000 / bc_rate
            prof = rev - cost
            prof_cur = prof * bc_rate
        fields.append(rev)
        fields.append(cost)
        fields.append(prof)
        fields.append(prof_cur)

        print row_format.format(*fields)
