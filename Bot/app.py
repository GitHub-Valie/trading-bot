from flask import Flask, render_template
import pandas as pd
import config
from binance.client import Client
from binance.websockets import BinanceSocketManager

app = Flask(__name__)

client = Client(
    config.binance['public_key'],
    config.binance['secret_key']
)

@app.route('/')
def index ():
    title = 'BinanceTradingBot'
    futures_account = client.futures_account()
    position = futures_account['positions']
    positions = []
    for symbol in position:
        if symbol['initialMargin'] != "0":
            positions.append({'Market': symbol['symbol'],
                              'Entry': float(symbol['entryPrice']),
                              'Leverage': symbol['leverage'],
                              'PNL': float(symbol['unrealizedProfit']),
                              'Side' : symbol['positionSide']
                              })
    
    futures_account['totalWalletBalance']=float(futures_account['totalWalletBalance'])
    futures_account['totalUnrealizedProfit']=float(futures_account['totalUnrealizedProfit'])
    futures_account['totalMarginBalance']=float(futures_account['totalMarginBalance'])
    pnl = futures_account['totalUnrealizedProfit']
    
    spot_balance = []
    spot_account = client.get_account()
    balance = spot_account['balances']

    for balance in balance:
        
        if (balance['free'] != '0.00000000') and (balance['free'] != '0.00'):
            spot_balance.append({'Assets': balance['asset'],
                               'Free': balance['free'],
                               'Symbol': balance['asset'] + "USDT",
                               'Value': "0"})
    
    spot_total = 0
    
    for index in range(len(spot_balance)):
        
        try:
            value = client.get_avg_price(symbol=spot_balance[index]['Symbol'])
            tmp= float(value['price']) * float(spot_balance[index]['Free'])
            spot_total += tmp
            spot_balance[index]['Value'] = round(tmp, 4)
            spot_balance[index]['Free'] = round(float(spot_balance[index]['Free']), 4)
        
        except:
            tmp = float(spot_balance[index]['Free'])
            spot_total += tmp
            spot_balance[index]['Value'] = round(tmp, 4)
            spot_balance[index]['Free'] = round(float(spot_balance[index]['Free']), 4)

    spot_total = round(spot_total, 4)
    grand_total = round(spot_total + float(futures_account['totalMarginBalance']), 4)
    
    return render_template(
        'index.html', 
        title=title, 
        spot_balance=spot_balance, 
        pnl=pnl, 
        spot_total=spot_total, 
        grand_total=grand_total, 
        my_future_position=positions,
        my_future=futures_account
    )
