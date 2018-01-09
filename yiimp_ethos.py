#!/usr/bin/python2
from __future__ import print_function
import requests
import sys
import time
import hashrate_db

currency = 'EUR'
power_cost = 0.15

if len(sys.argv) < 2 or not sys.argv[1].lower() in hashrate_db.cards():
    print('Need to give exactly one card: ' + ', '.join(hashrate_db.cards()))
    exit(0)
card = sys.argv[1]

pools = {
        'bsod.pw': 'http://bsod.pw/api/currencies',
        'zpool.ca': 'http://www.zpool.ca/api/currencies',
        'ahashpool.com': 'https://www.ahashpool.com/api/currencies',
}
pool = 'bsod.pw'
if len(sys.argv) >= 3:
    pool = sys.argv[2]
    if pool not in pools.keys():
        print('Pool not found. Available pools: ' + ', '.join(pools.keys()))
        exit(0)

r = requests.get('https://blockchain.info/de/ticker')
rj = r.json()
bc_rate = rj[currency]['15m']
print ("Bitcoin price: {} {}/BTC\n".format(bc_rate, currency))

print ("Using yiimp pool: {} ".format(pool), end='')

cookies = []

while True:
    sys.stdout.write('.')
    sys.stdout.flush()
    r = requests.get(pools[pool], cookies=cookies)
    try:
        rj = r.json()
        break
    except ValueError:
        if (r.cookies):
            cookies = r.cookies
        elif r.content != 'limit':
            print('Unexpected content received:')
            print(r.content)
            exit(0)
    time.sleep(1)

print('')

headers = ['currency', 'algo', 'estimate']
headers.append(card + " rev")
headers.append(card + " cost")
headers.append(card + " profit")
headers.append(card + " " + currency)

row_format_headers = '{:<14}{:<14}{:>14}' + '{:>14}' * 4
row_format = '{:<14}{:<14}{:>14.8f}' + '{:>14.8f}' * 4
print (row_format_headers.format(*headers))


if rj:
    for coin in rj.keys():
        algo = rj[coin]
        fields = [coin, algo['algo'], float(algo['estimate'])]

        rev = 0
        cost = 0
        prof = 0
        prof_cur = 0
        if algo['algo'].lower() in hashrate_db.algos(card):
            rev = float(algo['estimate']) * hashrate_db.hashrate(card, algo['algo'])
            cost = hashrate_db.power(card, algo['algo']) * 24 * power_cost / 1000 / bc_rate
            prof = rev - cost
            prof_cur = prof * bc_rate
        fields.append(rev)
        fields.append(cost)
        fields.append(prof)
        fields.append(prof_cur)

        if rev != 0:
            print(row_format.format(*fields))
