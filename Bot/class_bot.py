from binance.client import Client
from binance.enums import ORDER_RESP_TYPE_RESULT, ORDER_TYPE_MARKET, SIDE_SELL, SIDE_BUY
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

def Order(Symbol, Leverage, Precision, Percentage, Side, Price):
    '''
    Creates a market-type order on the futures market, given certain arguments: Symbol, Leverage, Precision, Side and Price.
    The function will first check the ```production``` boolean in the ```config.py``` file. The function will then calculate a 
    quantity based on the user's total wallet balance given by ```futures_account['totalWalletBalance']```
    '''
    if config.production:
        futures_account = client.futures_account()
        Quantity = float(Percentage) / 100 * float(futures_account['totalWalletBalance']) / float(Price)
        if Quantity > 0:
            client.futures_change_leverage(
                symbol = Symbol,
                leverage = Leverage
            )
            close = client.futures_create_order(
                symbol = Symbol,
                side = Side,
                newOrderRespType = ORDER_RESP_TYPE_RESULT,
                type = ORDER_TYPE_MARKET,
                quantity = Quantity
            )
            return close
    else:
            print('TEST NEW ORDER')

def ClosePosition(Symbol, Side, Quantity):
    '''
    Function to be used for take or save profits purposes. Given a ```Symbol```, ```Side``` and ```Quantity``` the function 
    will create an order ```ORDER_TYPE_MARKET``` to close the current position on the market.
    '''
    if config.production:
        close = client.futures_create_order(
            symbol = Symbol,
            side = Side,
            newOrderRespType = ORDER_RESP_TYPE_RESULT,
            type = ORDER_TYPE_MARKET,
            quantity = Quantity
        )
        return close
    else:
        print('TEST CLOSE POSITION')

class Bot:
    def __init__(self, symbol, fast, slow, leverage, precision, percentage):
        self.symbol = symbol
        self.fast = fast
        self.slow = slow
        self.data = []
        self.position = 0
        self.take_profit = 0
        self.quantity_take_profit = 0
        self.price_open = 0
        self.leverage = leverage
        self.precision = precision
        self.percentage = percentage
        self.qtity = 0
        self.fees_open = 0
        self.fees_close = 0
        self.total_fees = 0
        self.price_close = 0
        self.pnl_gross = 0
        self.pnl = 0
    
        klines = client.futures_klines(
            symbol = symbol,
            interval = Client.KLINE_INTERVAL_1MINUTE,
            limit = slow + 5
        )

        for index in range(len(klines)):
            
            if len(self.data) < self.slow:
                self.data.append({
                    'time_open' : klines[index][0],
                    'open' : float(klines[index][1]),
                    'high' : float(klines[index][2]),
                    'med': (float(klines[index][2]) + float(klines[index][3])) / 2,
                    'low' : float(klines[index][3]),
                    'close' : float(klines[index][4]),
                    'time_close' : klines[index][6],
                    'AweOsc' : None
                })
            
            else:
                self.data.append({
                    'time_open' : klines[index][0],
                    'open' : float(klines[index][1]),
                    'high' : float(klines[index][2]),
                    'med': (float(klines[index][2]) + float(klines[index][3])) / 2,
                    'low' : float(klines[index][3]),
                    'close' : float(klines[index][4]),
                    'time_close' : klines[index][6],
                    'AweOsc' : Sum(self.data[-self.fast:]) - Sum(self.data[-self.slow:])
                })

    def next(self, kline):
        '''
        Doctring for function 'next'
        '''
        if kline['t'] != self.data[-1]['time_open']:
            self.data.pop(0)
            self.data.append({
                'time_open' : kline['t'],
                'open' : float(kline['o']),
                'high' : float(kline['h']),
                'med': (float(kline['h']) + float(kline['l'])) / 2,
                'low' : float(kline['l']),
                'close' : float(kline['c']),
                'time_close' : kline['T'],
                'AweOsc' : Sum(self.data[-self.fast:])-Sum(self.data[-self.slow:])
            })
        
        else:
            self.data[-1] = {
                'time_open' : kline['t'],
                'open': float(kline['o']),
                'high': float(kline['h']),
                'med': (float(kline['h']) + float(kline['l'])) / 2,
                'low' : float(kline['l']),
                'close': float(kline['c']),
                'time_close': kline['T'],
                'AweOsc' : Sum(self.data[-self.fast:])-Sum(self.data[-self.slow:])
            }

        if self.position == 0: # Not in position

            if (self.data[-1]['AweOsc'] > self.data[-2]['AweOsc'] < self.data[-3]['AweOsc']): # Long condition
                if config.production:
                    try:
                        trade = Order(
                            Symbol=self.symbol,
                            Leverage=self.leverage,
                            Precision=self.precision,
                            Percentage=self.percentage,
                            Side=SIDE_BUY,
                            Price=self.data[-1]['close']
                        )
                        self.fees_open = float(trade['executedQty']) * float(trade['avgPrice']) * 0.0035
                        self.qtity = float(trade['executedQty'])
                        self.price_open = float(trade['avgPrice'])
                        self.time_open = trade['updateTime']
                        self.position = 1
                        # mongodb insert
                        print('LIVE ORDER | LONG POSITION | BUYING {}'.format(self.symbol))
                    except Exception as e:
                        print('{}: Error {}'.format(self.symbol, e))
                        pass
                else:
                    print('TEST ORDER | LONG POSITION | BUYING {}'.format(self.symbol))
                    self.position = 1
        
            if (self.data[-1]['AweOsc'] < self.data[-2]['AweOsc'] > self.data[-3]['AweOsc']): # Short condition
                if config.production:
                    try:
                        trade = Order(
                            Symbol=self.symbol,
                            Leverage=self.leverage,
                            Precision=self.precision,
                            Percentage=self.percentage,
                            Side=SIDE_SELL,
                            Price=self.data[-1]['close']
                        )
                        self.fees_open = float(trade['executedQty']) * float(trade['avgPrice']) * 0.0035
                        self.qtity = float(trade['executedQty'])
                        self.price_open = float(trade['avgPrice'])
                        self.time_open = trade['updateTime']
                        self.position = -1
                        # mongodb insert
                        print('LIVE ORDER | SHORT POSITION | SELLING {}'.format(self.symbol))
                    except Exception as e:
                        print('{}: Error {}'.format(self.symbol, e))
                else:
                    print('TEST ORDER | SHORT POSITION | SELLING {}'.format(self.symbol))
                    self.position = -1
        
        if config.production: # In production mode
            
            if self.position == 1 and self.take_profit == 0: # If we're in long position and no TP yet
                
                if ((self.data[-1]['close'] - self.price_open) / self.price_open) * self.leverage > 0.035:
                    # TODO: Quantity
                    self.quantity_take_profit = round(self.qtity / 2, self.precision)
                    self.qtity = self.qtity - self.quantity_take_profit
                    tmp = ClosePosition(
                        Symbol = self.symbol,
                        Side = SIDE_SELL,
                        Quantity = self.quantity_take_profit
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) *  0.00035
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = self.price_close - self.price_open * self.quantity_take_profit
                    self.pnl = self.pnl_gross - self.fees_close

                    self.take_profit = 1
                    print('TAKING PROFIT FOR LONG POSITION ON {} | PNL: {}'.format(self.symbol, self.pnl))
            
            if self.position == -1 and self.take_profit == 0: # If we're in short position and no TP yet
                
                if ((self.data[-1]['close'] - self.price_open) / self.price_open) * self.leverage < -0.035:
                    # TODO: Quantity
                    self.quantity_take_profit = round(self.qtity / 2, self.precision)
                    self.qtity = self.qtity - self.quantity_take_profit
                    tmp = ClosePosition(
                        Symbol = self.symbol,
                        Side = SIDE_BUY,
                        Quantity = self.quantity_take_profit
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) *  0.00035
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = self.price_close - self.price_open * self.quantity_take_profit
                    self.pnl = self.pnl_gross - self.total_fees # or self.fees_close ?

                    self.take_profit = 1
                    print('TAKING PROFIT FOR SHORT POSITION ON {} | PNL: {}'.format(self.symbol, self.pnl))
            
            if self.position == 1 and self.take_profit == 1: # If we're in long position and in TP
                
                if ((float(self.data[-1]['close']) - self.price_open) / self.price_open) * self.leverage > 0.05 : # High Save profit
                    # TODO : Quantity
                    tmp = ClosePosition(
                        Symbol = self.symbol, 
                        Side = SIDE_SELL, 
                        Quantity= self.qtity
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) * 0.00035
                    self.fees_total = self.fees_open + self.fees_close
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = (self.price_close - self.price_open) * self.quantity_take_profit
                    self.pnl = self.pnl_gross - self.fees_total
                    
                    self.take_profit = 0
                    self.position = 0
                    print('CLOSING HIGH SAVE FOR {} | PNL: {}'.format(self.symbol, self.pnl))
                
                elif ((float(self.data[-1]['close']) - self.price_open) / self.price_open) * self.leverage < 0.01: # Low save profit
                    tmp = ClosePosition(
                        Symbol=self.symbol,
                        Side=SIDE_SELL,
                        Quantity=self.qtity
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) * 0.00035
                    self.fees_total = self.fees_open + self.fees_close
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = (self.price_close - self.price_open) * self.quantity_take_profit
                    self.pnl = self.pnl_gross - self.fees_total
                    # mongodb insert
                    self.take_profit = 0
                    self.position = 0
                    print('CLOSING LOW SAVE FOR {} | PNL: {}'.format(self.symbol, self.pnl))

                else: # Between .01 and .05
                    
                    pass

            if self.position == -1 and self.take_profit == 1: # If we're in short position and in TP

                if ((float(self.data[-1]['close']) - self.price_open) / self.price_open) * self.leverage < -0.05: # High Save profit
                    tmp = ClosePosition(
                        Symbol=self.symbol,
                        Side=SIDE_BUY,
                        Quantity=self.qtity
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) * 0.00035
                    self.fees_total = self.fees_open + self.fees_close
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = (self.price_open - self.price_close) * self.quantity_take_profit
                    self.pnl = self.pnl_gross - self.fees_total
                    # mongodb insert
                    self.take_profit = 0
                    self.position = 0
                    print('CLOSING HIGH SAVE FOR {} | PNL: {}'.format(self.symbol, self.pnl))

                elif ((float(self.data[-1]['close']) - self.price_open) / self.price_open) * self.leverage > -0.01: # Low Save profit
                    tmp = ClosePosition(
                        Symbol=self.symbol,
                        Side=SIDE_SELL,
                        Quantity=self.qtity
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) * 0.00035
                    self.fees_total = self.fees_open + self.fees_close
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = (self.price_open - self.price_close) * self.quantity_take_profit
                    self.pnl = self.pnl_gross - self.fees_total
                    # mongodb insert
                    self.take_profit = 0
                    self.position = 0
                    print('CLOSING LOW SAVE FOR {} | PNL: {}'.format(self.symbol, self.pnl))
                
                else: # Between -.05 and -.01

                    pass

        if self.position == 1 and self.data[-1]['AweOsc'] < self.data[-2]['AweOsc']: # If we're in long position and crossing under
            
            if config.production:
                
                try:
                    tmp = ClosePosition(
                        Symbol=self.symbol, 
                        Side = SIDE_SELL, 
                        Quantity=self.qtity
                    )
                    trade = Order(
                        Symbol=self.symbol, 
                        Leverage=self.leverage, 
                        Precision=self.precision, 
                        Percentage=self.percentage, 
                        Side=SIDE_SELL, 
                        Price=self.data[-1]['close']
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) * 0.00035
                    self.fees_total = self.fees_open + self.fees_close
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = (self.price_close - self.price_open)*self.qtity
                    self.pnl = self.pnl_gross - self.fees_total
                    # mongodb insert
                    self.qtity = float(trade['executedQty'])
                    self.price_open = float(trade['avgPrice'])
                    self.time_open = trade['updateTime']
                    self.fees_open = float(trade['executedQty']) * float(trade['avgPrice']) * 0.00035
                    self.position = -1
                    # mongodb insert
                    print('LIVE ORDER | {} CLOSING LONG POSITION, OPENING SHORT | PNL: {}'.format(self.symbol, self.pnl))

                except Exception as e:
                        print('{}: Error {}'.format(self.symbol, e))
                        pass
            
            else:
                print('TEST ORDER | CLOSING LONG POSITION, OPENING SHORT | SYMBOL : {}'.format(self.symbol))
                self.position = -1

        if self.position == -1 and self.data[-1]['AweOsc'] > self.data[-2]['AweOsc']: # If we're in short position and crossing over
            
            if config.production:

                try:
                    tmp = ClosePosition(
                        Symbol=self.symbol, 
                        Side = SIDE_BUY, 
                        Quantity=self.qtity
                    )
                    trade = Order(
                        Symbol=self.symbol, 
                        Leverage=self.leverage, 
                        Precision=self.precision, 
                        Percentage=self.percentage, 
                        Side=SIDE_BUY, 
                        Price=self.data[-1]['close']
                    )
                    self.fees_close = float(tmp['executedQty']) * float(tmp['avgPrice']) * 0.00035
                    self.fees_total = self.fees_open + self.fees_close
                    self.price_close = float(tmp['avgPrice'])
                    self.pnl_gross = (self.price_close - self.price_open) * self.qtity
                    self.pnl = self.pnl_gross - self.fees_total
                    # mongodb insert
                    self.qtity = float(trade['executedQty'])
                    self.price_open = float(trade['avgPrice'])
                    self.time_open = trade['updateTime']
                    self.fees_open = float(trade['executedQty']) * float(trade['avgPrice']) * 0.00035
                    self.position = 1
                    # mongodb insert
                    print('LIVE ORDER | {} CLOSING SHORT POSITION, OPENING LONG | PNL: {}'.format(self.symbol, self.pnl))
                
                except Exception as e:
                    print('{}: Error {}'.format(self.symbol, e))
                    pass
            
            else:
                print('TEST ORDER | CLOSING SHORT POSITION, OPENING LONG | SYMBOL : {}'.format(self.symbol))
                self.position = 1

