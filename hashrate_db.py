
hashes = {
        'rx470' : {
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
            'ethash': { 'hash': 30.5 / 1000, 'power': 135 },
            'nist5': { 'hash': 41.0 / 1000, 'power': 110 },
            'xevan': { 'hash': 4 / 1000, 'power': 155 },
            'neoscrypt': { 'hash': 0.940 / 1000, 'power': 120 },
            'lyra2v2': { 'hash': 40.0 / 1000, 'power': 110 },
            'lyra2re2': { 'hash': 40.0 / 1000, 'power': 110 },
            'equihash': { 'hash': 500.0 / (1000 * 1000 * 1000), 'power': 115 },
            'cryptonight': { 'hash': 600.0 / (1000 * 1000 * 1000), 'power': 100 },
            'lyra2z': { 'hash': 2250.0 / (1000 * 1000), 'power': 100 },
            'phi1612': { 'hash': 20.0 / 1000, 'power': 120 },
            },
        '1080ti': {
            'nist5': { 'hash': 56.1 / 1000, 'power': 150 },
            'skunk': { 'hash': 46.0 / 1000, 'power': 170 },
            'xevan': { 'hash': 5 / 1000, 'power': 200 },
            'neoscrypt': { 'hash': 1.340 / 1000, 'power': 170 },
            'lyra2v2': { 'hash': 59.0 / 1000, 'power': 170 },
            'lyra2re2': { 'hash': 59.0 / 1000, 'power': 170 },
            'equihash' : { 'hash': 680.0 / (1000 * 1000 * 1000), 'power': 190 },
            'cryptonight': { 'hash': 830.0 / (1000 * 1000 * 1000), 'power': 140 },
            'lyra2z': { 'hash': 3200.0 / (1000 * 1000), 'power': 140 },
            'phi1612': { 'hash': 30.0 / 1000, 'power': 170 },
            },
        }

def cards():
    return hashes.keys()

def algos(card):
    return hashes[card.lower()].keys()

def hashrate(card, algo):
    return hashes[card.lower()][algo.lower()]['hash']

def power(card, algo):
    return hashes[card.lower()][algo.lower()]['power']
