from binance.client import Client
import config

client = Client(
    api_key = config.binance_futures['public_key'],
    api_secret = config.binance_futures['secret_key']
)

def Sum(list):
    sum = 0
    for item in list:
        sum += float(item['med'])
    return sum/len(list)

# TODO: Add order function here

# TODO: Add close position function here

class Bot:
    def __init__(self, symbol, fast, slow):
        self.symbol = symbol
        self.fast = fast
        self.slow = slow
        self.candle = []
        self.position = 0
    
        klines = client.futures_klines(
            symbol = symbol,
            interval = Client.KLINE_INTERVAL_1MINUTE,
            limit = slow + 5
        )

        for index in range(len(klines)):
            if len(self.candle) < self.slow:
                self.candle.append({
                    'time_open' : klines[index][0],
                    'open' : klines[index][1],
                    'high' : klines[index][2],
                    'med': (float(klines[index][2]) + float(klines[index][3])) / 2,
                    'low' : klines[index][3],
                    'close' : klines[index][4],
                    'time_close' : klines[index][6],
                    'AweOsc' : None
                })
            else:
                self.candle.append({
                    'time_open' : klines[index][0],
                    'open' : klines[index][1],
                    'high' : klines[index][2],
                    'med': (float(klines[index][2]) + float(klines[index][3])) / 2,
                    'low' : klines[index][3],
                    'close' : klines[index][4],
                    'time_close' : klines[index][6],
                    'AweOsc' : Sum(self.candle[-self.fast:]) - Sum(self.candle[-self.slow:])
                })

    def next(self, kline):
        if kline['t'] != self.candle[-1]['time_open']:
            self.candle.pop(0)
            self.candle.append({
                'time_open' : kline['t'],
                'open' : kline['o'],
                'high' : kline['h'],
                'med': (float(kline['h']) + float(kline['l'])) / 2,
                'low' : kline['l'],
                'close' : kline['c'],
                'time_close' : kline['T'],
                'AweOsc' : Sum(self.candle[-self.fast:])-Sum(self.candle[-self.slow:])
            })
        else:
            self.candle[-1] = {
                'time_open' : kline['t'],
                'open': kline['o'],
                'high': kline['h'],
                'med': (float(kline['h']) + float(kline['l'])) / 2,
                'low' : kline['l'],
                'close': kline['c'],
                'time_close': kline['T'],
                'AweOsc' : Sum(self.candle[-self.fast:])-Sum(self.candle[-self.slow:])
            }
        
        if self.position == 0:
            if (self.candle[-1]['AweOsc'] > self.candle[-2]['AweOsc'] < self.candle[-3]['AweOsc']):
                if config.production:
                    try:
                        print('LIVE ORDER | LONG POSITION | BUYING {}'.format(self.symbol))
                        self.position = 1
                    except Exception as e:
                        print('{}: Error {}'.format(self.symbol, e))
                else:
                    print('\nAweOsc -3: ', self.candle[-3]['AweOsc'], '\nAweOsc -2: ', self.candle[-2]['AweOsc'], '\nAweOsc -1: ', self.candle[-1]['AweOsc'])
                    print('TEST ORDER | LONG POSITION | BUYING {}'.format(self.symbol))
                    self.position = 1
                    pass
                    
            if (self.candle[-1]['AweOsc'] < self.candle[-2]['AweOsc'] > self.candle[-3]['AweOsc']):
                if config.production:
                    try:
                        print('LIVE ORDER | SHORT POSITION | SELLING {}'.format(self.symbol))
                        self.position = -1
                    except Exception as e:
                        print('{}: Error {}'.format(self.symbol, e))
                else:
                    print('\nAweOsc -3: ', self.candle[-3]['AweOsc'], '\nAweOsc -2: ', self.candle[-2]['AweOsc'], '\nAweOsc -1: ', self.candle[-1]['AweOsc'])
                    print('TEST ORDER | SHORT POSITION | SELLING {}'.format(self.symbol))
                    self.position = -1
        
        if config.production:
            # TODO: Add stop-loss / take-profit logic here
            print('Take profit conditions and info')

        if self.position == 1 and self.candle[-1]['AweOsc'] < self.candle[-2]['AweOsc']:
            if config.production:
                try:
                    print('LIVE ORDER | CLOSING LONG POSITION, OPENING SHORT | SYMBOL : {}'.format(self.symbol))
                    self.position = -1
                except Exception as e:
                    print('{}: Error {}'.format(self.symbol, e))
                    pass
            
            else:
                print('\nAweOsc -3: ', self.candle[-3]['AweOsc'], '\nAweOsc -2: ', self.candle[-2]['AweOsc'], '\nAweOsc -1: ', self.candle[-1]['AweOsc'])
                print('TEST ORDER | CLOSING LONG POSITION, OPENING SHORT | SYMBOL : {}'.format(self.symbol))
                self.position = -1
        
        if self.position == -1 and self.candle[-1]['AweOsc'] > self.candle[-2]['AweOsc']:
            if config.production:
                try:
                    print('LIVE ORDER | CLOSING SHORT POSITION, OPENING LONG | SYMBOL : {}'.format(self.symbol))
                    self.position = 1
                except Exception as e:
                    print('{}: Error {}'.format(self.symbol, e))
                    pass

            else:
                print('\nAweOsc -3: ', self.candle[-3]['AweOsc'], '\nAweOsc -2: ', self.candle[-2]['AweOsc'], '\nAweOsc -1: ', self.candle[-1]['AweOsc'])
                print('TEST ORDER | CLOSING SHORT POSITION, OPENING LONG | SYMBOL : {}'.format(self.symbol))
                self.position = 1

