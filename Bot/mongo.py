from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING
import config

client = MongoClient(config.mongodb['host'])

db = client[config.mongodb['database']]

def db_insert(Symbol, TimeOpen, PriceOpen, Quantity, Side, FeesOpen):
    '''
    Fuction Docstring
    '''
    collection = db['bot_transaction']
    collection.insert_one({
        'symbol' : Symbol,
        'time_open' : TimeOpen,
        'price_open' : PriceOpen,
        'quantity' : Quantity,
        'side' : Side,
        'fees_entry' : FeesOpen
    })

def db_update_tp(Symbol, TimeOpen, TimeClose, PriceClose, FeesClose, PNL):
    '''
    Function docstring
    '''
    collection = db['bot_transaction']
    collection.update_one(
        {
            'symbol' : Symbol,
            'time_open' : TimeOpen
        },{
            '$set' : {
                'time_close_tp' : TimeClose,
                'price_close_tp' : PriceClose,
                'fees_close' : FeesClose,
                'pnl_tp' : PNL
            }
        }
    )

def db_update(Symbol, TimeOpen, TimeClose, PriceClose, FeesClose, PNL):
    '''
    Function Docstring
    '''
    collection = db['bot_transaction']
    collection.update_one(
        {
            'symbol' : Symbol,
            'time_open' : TimeOpen
        },{
            '$set' : {
                'time_close' : TimeClose,
                'price_close' : PriceClose,
                'fees_close' : FeesClose,
                'pnl' : PNL
            }
        }
    )