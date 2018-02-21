import requests
import time
import sys
import hashrate_db

class Pool:
    """
    Base class for all pools.
    """

    def __init__(self, url, currency, power_cost):
        self._url = url
        self._data = {}
        self._currency = currency
        self._power_cost = power_cost

    def fetch_btc_price(self):
        r = requests.get('https://blockchain.info/de/ticker')
        rj = r.json()
        self._bc_rate = rj[self._currency]['15m']

    def calc_profits(self, card, fetch=False):
        result = {}
        if fetch:
            try:
                self.fetch_btc_price()
                self.fetch_data()
            except ValueError:
                return result
        for coin in self._data.keys():
            algo = self._data[coin]
            if algo['algo'].lower() in hashrate_db.algos(card):
                rev = float(algo['estimate']) * hashrate_db.hashrate(card, algo['algo'])
                cost = hashrate_db.power(card, algo['algo']) * 24 * self._power_cost / 1000 / self._bc_rate
                prof = rev - cost
                result[coin] = prof
        return result

    def fetch_data(self):
        pass

class YiimpPool(Pool):
    """
    Yiimp based pools.
    """

    pool_urls = {
            'bsod.pw': 'http://api.bsod.pw/api/currencies',
            'zpool.ca': 'http://www.zpool.ca/api/currencies',
            'ahashpool.com': 'https://www.ahashpool.com/api/currencies',
    }

    def __init__(self, pool, currency, power_cost):
        Pool.__init__(self, self.pool_urls[pool], currency, power_cost)

    def fetch_data(self):
        cookies = []
        while True:
            r = requests.get(self._url, cookies=cookies)
            try:
                self._data = r.json()
                break
            except ValueError:
                if (r.cookies):
                    cookies = r.cookies
                elif r.content != 'limit':
                    sys.stderr.write('Unexpected content received:')
                    sys.stderr.write(r.content)
                    raise
            time.sleep(1)
