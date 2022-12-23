import sqlite3
from binance import Client

# Create connection to DB
connection = sqlite3.connect("app.db")

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
                SELECT pair FROM currencies 
            """)

rows = cursor.fetchall()

# Create connection to Binance API
client = Client()

# Get data: timezone, ServerTime, rateLimits, exchangeFilters, symbols in dict type
info = client.get_exchange_info()
# Get data only from symbols dict
symbols = info["symbols"]
exchange = "BINANCE"

# Iterate over list of symbols, check if they are in DB, and add if not
for symbol in symbols:
    try:
        if symbol["status"] == "TRADING" and symbol["symbol"] not in rows:
            print(f"Added a new pair: {symbol['symbol']}")
            cursor.execute("INSERT INTO currencies (pair, base_asset, quote_asset, exchange) VALUES (?, ?, ?, ?)",
                           (symbol["symbol"], symbol["baseAsset"], symbol["quoteAsset"], exchange))
    except Exception as e:
        print(symbol["symbol"])
        print(e)

connection.commit()