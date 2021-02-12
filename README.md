# Cryptocurrency trading bot

This project aims at deploying a trading bot capable of trading multiple cryptocurrencies based on an algorithm which will execute buy and sell orders in accordance with a trading strategy

## How does it work ?

### Binance API

Uses the Binance API (requires you to setup a ```config.py``` file with api keys)

### Websockets

Connection via websocket protocol to get a live stream of json OHLC price data for a set of cryptocurrency pairs 

### Specifying cryptocurrency pairs and parameters for technical indicators

The set of cryptocurrency pairs is specified in ```config_bot.py``` (crypto pair and parameters for technical indicators)

### Bot instantiation

The program will create an instance of Bot (class Bot, see ```class_bot.py```) for each cryptocurrency pair.

### Processing data

Once the connection is done and data is streamed, and bots have been instantiated, the data will be processed. 

A median price will be calculated (high + low / 2). See the 'next' function in ```class_bot.py``` for details.

## Setup guide

## Strategy


