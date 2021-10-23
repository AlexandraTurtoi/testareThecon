from binance.client import Client
api_key="3Jstf10slIGbeJMnU9lJwjpkmBJQK71RupXCmjnzshXwVjteOeMPflc0Us9AY28J"
api_secret="GtAuM9zh85A7qmbyQ5SbuZ6pqsy9pYbIV14kTis7eh7NgZcwMkWG0PsuVDR4js6d"
client = Client(api_key, api_secret)
klines = client.get_historical_klines("ETHBUSD", Client.KLINE_INTERVAL_1MINUTE, "27 Sept, 2021", "28 Sept, 2021")
print(klines)
