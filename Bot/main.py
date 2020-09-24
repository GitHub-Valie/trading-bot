import config_bot, class_bot, config
import websocket, json, time, pprint
import pandas as pd
from binance.client import Client

client = Client(
    api_key = config.binance_futures['public_key'],
    api_secret = config.binance_futures['secret_key']
)

socket = "wss://fstream3.binance.com/stream?streams="

print('Instantiating bots ...')

bots = []
for bot in config_bot.bots:
    bots.append(bot)
    # We create as many instances of the class Bot as the amount of dictionaries in our 'bots' list in config_bot.py. Each instance has its own trading pair and is stored in the 'bots' list created just before
    bots[-1]['bot'] = class_bot.Bot(
        bot['pair'],
        bot['fast_trend'],
        bot['slow_trend']
    )
    socket += bot['pair'].lower() + "@kline_1m/"
    print('Bot: {}'.format(bot))

print('Socket: {}'.format(socket))

def on_open(ws):
    print('Opened Connection')

def on_close(ws):
    print('Closed Connection')

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['data']['k']
    for bot in bots:
        if bot['pair'] == candle['s']:
            # print(candle)
            bot['bot'].next(candle)
            break # Breaks the execution of the for loop

ws = websocket.WebSocketApp(
    socket, 
    on_open = on_open, 
    on_close = on_close, 
    on_message = on_message
)

while True:
    print('Reconnection')
    ws.run_forever()