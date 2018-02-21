#!/usr/bin/python2
from __future__ import print_function
import requests
import sys
import time
import hashrate_db
import pools

currency = 'EUR'
power_cost = 0.15

if len(sys.argv) < 2 or not sys.argv[1].lower() in hashrate_db.cards():
    print('Need to give exactly one card: ' + ', '.join(hashrate_db.cards()))
    exit(0)
card = sys.argv[1]

pool = 'bsod.pw'
if len(sys.argv) >= 3:
    pool = sys.argv[2]
    if pool not in pools.YiimpPool.pool_urls.keys():
        print('Pool not found. Available pools: ' + ', '.join(pools.YiimpPool.pool_urls.keys()))
        exit(0)

p = pools.YiimpPool(pool, currency, power_cost)
res = p.calc_profits(card, fetch=True)

headers = ['time']
headers.extend(res.keys())

row_format_headers = '{:<20}' + '{:>12}' * len(res.keys())
row_format = '{:<20}' + '{:>12.8f}' * len(res.keys())
print (row_format_headers.format(*headers))

while True:
    if res:
        fields = []
        fields.append(time.strftime('%Y-%m-%d %H:%M:%S'))
        for coin in res.keys():
            fields.append(res[coin])
        print(row_format.format(*fields))
        sys.stdout.flush()
    time.sleep(600)
    res = p.calc_profits(card, fetch=True)
