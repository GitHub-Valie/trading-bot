from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET
import config as cf
import websocket, json, talib, numpy

numpy.set_printoptions(precision=8)

TRADE_SYMBOL = 'BNBBTC'
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_1m".format(TRADE_SYMBOL.lower())

closes = []
in_position = False

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('SENDING ORDER')
        order = client.create_order(
            symbol=symbol, 
            side=side, 
            type=order_type, 
            quantity=quantity
        )
        print(order)
    except Exception as e:
        print("Exception occured - {}".format(e))
        return False

    return True

def on_open(ws):
    print('OPENED CONNECTION')

def on_close(ws):
    print('CLOSED CONNECTION')

def on_message(ws, message):
    global closes, in_position
    
    print('RECEIVED MESSAGE')
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    print(
        json_message['s'],
        "\nopen:      ", candle['o'],
        "\nhigh:      ", candle['h'],
        "\nlow:       ", candle['l'],
        "\nclose:     ", close,
        "\nvolume:    ", candle['v']
    )
    if is_candle_closed:
        print("\nCANDLE CLOSED AT {:.8f}".format(float(close)))

while True:
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()