from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL
import config
import websocket, json, talib, numpy

numpy.set_printoptions(precision=8)

trade_symbol = 'BATBTC'
fast_sma_period = 2
slow_sma_period = 6
trade_quantity = 12
socket = "wss://stream.binance.com:9443/ws/{}@kline_1m".format(trade_symbol.lower())

pnl = []
fees = []
closes = []
in_position = False

client = Client(
    config.binance_spot['public_key'],
    config.binance_spot['secret_key']
)

exchange_info = client.get_exchange_info()
for k in exchange_info["symbols"]:
    if k["symbol"] == trade_symbol:
        base_asset = k["baseAsset"]
        quote_asset = k["quoteAsset"]

base_asset_balance = client.get_asset_balance(
    asset=base_asset
)

quote_asset_balance = client.get_asset_balance(
    asset=quote_asset
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
    global closes, in_position # Step 1: Receive message
    
    # print('RECEIVED MESSAGE') 
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    print( # Step 2: Read message content
        "\nSymbol:    ", json_message['s'],
        "\nOpen:      ", candle['o'],
        "\nHigh:      ", candle['h'],
        "\nLow:       ", candle['l'],
        "\nClose:     ", close,
        "\nVolume:    ", candle['v']
    ) 
    if is_candle_closed: # Step 3: Check if candle is closed
        print("\nCANDLE CLOSED AT {:.8f}".format(float(close)))
        closes.append(float(close))
        print("\nCLOSES") # Step 4: Print information about last close values
        print(closes)

        get_orders = client.get_all_orders(
            symbol=trade_symbol
        )

        my_trades = client.get_my_trades(
            symbol=trade_symbol
        )

        # Check BUY-SELL profit/loss
        last_order = get_orders[-1]
        last_order_id = last_order['orderId']
        last_order_side = last_order['side']

        second_to_last_order = get_orders[-2]
        second_to_last_order_id = second_to_last_order['orderId']
        second_to_last_order_side = second_to_last_order['side']

        last_trade = my_trades[-1]
        last_trade_id = last_trade['orderId']

        second_to_last_trade = my_trades[-1]
        second_to_last_trade_id = last_trade['orderId']

        # Check if sell order id = sell trade id ; buy order id = buy trade id
        if second_to_last_order_id == second_to_last_trade_id and last_order_id == last_trade_id:

            # Check if last trade was on side SELL and if second to last trade was on side BUY
            if second_to_last_order_side == 'BUY' and last_order_side == 'SELL':
                print('BUY-SELL CONDITION: CHECKED')
                
                # Calculate buy price and sell price and commissions
                buy_price = float(second_to_last_trade['price'])
                buy_fee = float(second_to_last_trade['commission'])

                sell_price = float(last_trade['price'])
                sell_fee = float(last_trade['commission'])

                last_pnl = sell_price - buy_price
                pnl.append(last_pnl)

                buysell_fees = buy_fee + sell_fee
                fees.append(buysell_fees)

                last_trade_fee_asset = last_trade['commissionAsset']
                second_to_last_trade_fee_asset = second_to_last_trade['commissionAsset']

                # Display pnl and fees from last buy-sell operation
                print('\nLAST PNL:    {}'.format(last_pnl))
                if last_trade_fee_asset == second_to_last_trade_fee_asset:
                    print('FEES:        {} {}'.format(buysell_fees, last_trade_fee_asset))
                
                # Display total pnl and fees
                print('\nTOTAL PNL SO FAR:    {}'.format(sum(pnl)))
                print('TOTAL FEES SO FAR:     {}'.format(sum(fees)))
                # Display asset balances
                print('\n{} BALANCE:    {}'.format(base_asset, base_asset_balance))
                print('{} BALANCE:    {}'.format(quote_asset, quote_asset_balance))

        # Step 5: Check if there are enough values to calculate technical indicators
        if len(closes) >= slow_sma_period: 
            closes_float = [float(x) for x in closes]
            np_closes = numpy.array(closes_float)
            
            fast_sma = talib.SMA(
                np_closes,
                fast_sma_period
            )
            slow_sma = talib.SMA(
                np_closes,
                slow_sma_period
            )

            last_fast_sma = fast_sma[-1]
            last_slow_sma = slow_sma[-1]
            
            print(
                "\nCURRENT FAST SMA: {:.8f}".format(last_fast_sma),
                "\nCURRENT SLOW SMA: {:.8f}".format(last_slow_sma)
            )

            # Step 6: Write down the strategy
            if last_fast_sma > last_slow_sma:
                if in_position:
                    # If fast sma > slow sma but already in position, nothing to do
                    print('SHOULD BUY, BUT ALREADY IN POSITION')
                else:
                    # If not in position, Buy
                    print('FAST SMA > SLOW SMA: SHOULD BUY')
                    order_succeeded = order(
                        side=SIDE_BUY,
                        quantity=trade_quantity,
                        symbol=trade_symbol,
                        order_type=ORDER_TYPE_MARKET
                    )
                    if order_succeeded:
                        print('{} BUY ORDER SUCCESSFUL'.format(trade_symbol))
                        in_position = True

            if last_fast_sma < last_slow_sma:
                if in_position:
                    # When fast SMA < slow SMA and already in position, Sell
                    print('FAST SMA < SLOW SMA: SHOULD SELL')
                    order_succeeded = order(
                        side=SIDE_SELL,
                        quantity=trade_quantity,
                        symbol=trade_symbol,
                        order_type=ORDER_TYPE_MARKET
                    )
                    if order_succeeded:
                        # Check if order is successful
                        print('{} SELL ORDER SUCCESSFUL'.format(trade_symbol))
                        in_position = False
                                
                else:
                    # If fast sma < slow sma buy not in position: Nothing to do
                    print('SHOULD SELL, BUT NOT IN POSITION')

while True:
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()