from binance.client import Client

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_hourly_dataframe():


    starttime = '1 week ago UTC'
    interval = '1h'
    bars = client.get_historical_klines(symbol, interval, starttime)

    for line in bars:
        del line[5:]

    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close']) #  2 dimensional tabular data
    return df


def plot_graph(df):
    df=df.astype(float)
    df[['close', '5sma','15sma']].plot()
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Close price',fontsize=18)

    plt.scatter(df.index,df['Buy'], color='purple',label='Buy',  marker='^', alpha = 1) # purple = buy
    plt.scatter(df.index,df['Sell'], color='red',label='Sell',  marker='v', alpha = 1)  # red = sell

    plt.show()


def buy_or_sell(buy_sell_list, df):
    for index, value in enumerate(buy_sell_list):
        current_price = client.get_symbol_ticker(symbol =symbol)
        print(current_price['price']) # Output is in json format, only price needs to be accessed
        if value == 1.0 : # signal to buy (either compare with current price to buy/sell or use limit order with close price)
            if current_price['price'] < df['Buy'][index]:
                print("buy buy buy....")
                buy_order = client.order_market_buy(symbol=symbol, quantity=2)
                print(buy_order)
        elif value == -1.0:
            if current_price['price'] > df['Sell'][index]:
                print("sell sell sell....")
                sell_order = client.order_market_sell(symbol=symbol, quantity=10)
                print(sell_order)
        else:
            print("nothing to do...")



def sma_trade_logic():
    symbol_df = get_hourly_dataframe()

    symbol_df['5sma'] = symbol_df['close'].rolling(5).mean()
    symbol_df['15sma'] = symbol_df['close'].rolling(15).mean()

    symbol_df.set_index('date', inplace=True)
    symbol_df.index = pd.to_datetime(symbol_df.index, unit='ms')

    symbol_df['Signal'] = np.where(symbol_df['5sma'] > symbol_df['15sma'], 1, 0)
    symbol_df['Position'] = symbol_df['Signal'].diff()
    
    symbol_df['Buy'] = np.where(symbol_df['Position'] == 1,symbol_df['close'], np.NaN )
    symbol_df['Sell'] = np.where(symbol_df['Position'] == -1,symbol_df['close'], np.NaN )


    with open('output.txt', 'w') as f:
        f.write(  symbol_df.to_string()   )


    buy_sell_list = symbol_df['Position'].tolist()

    buy_or_sell(buy_sell_list, symbol_df)


def main():
    sma_trade_logic()

if __name__ == "__main__":

    api_key = '3Jstf10slIGbeJMnU9lJwjpkmBJQK71RupXCmjnzshXwVjteOeMPflc0Us9AY28J'
    api_secret = 'GtAuM9zh85A7qmbyQ5SbuZ6pqsy9pYbIV14kTis7eh7NgZcwMkWG0PsuVDR4js6d'

    client = Client(api_key, api_secret, testnet=True)
    print("Using Binance TestNet Server")

    symbol = 'BTCBUSD'
    main()
