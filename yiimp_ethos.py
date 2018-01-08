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
print "Bitcoin price: {} {}/BTC\n".format(bc_rate, currency)

print "Using yiimp pool: {}".format(pool)
r = requests.get(pools[pool])
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
        if algo['algo'].lower() in hashrate_db.algos(card):
            rev = float(algo['estimate']) * hashrate_db.hashrate(card, algo['algo'])
            cost = hashrate_db.power(card, algo['algo']) * 24 * power_cost / 1000 / bc_rate
            prof = rev - cost
            prof_cur = prof * bc_rate
        fields.append(rev)
        fields.append(cost)
        fields.append(prof)
        fields.append(prof_cur)

        print row_format.format(*fields)
