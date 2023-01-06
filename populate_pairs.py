import sqlite3
from binance import Client
from config import DB_FILE


# Create connection to DB
connection = sqlite3.connect(DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
                SELECT pair FROM currencies 
            """)

rows = cursor.fetchall()
pairs_in_db = [row["pair"] for row in rows]

# Create connection to Binance API
client = Client()

# Get data: timezone, ServerTime, rateLimits, exchangeFilters, symbols in dict type
info = client.get_exchange_info()

# Get data only from symbols dict
symbols = info["symbols"]

exchange = "BINANCE"
number_of_added_pairs = 0
number_of_delisted_pairs = 0

# Iterate over list of symbols, check if they are in DB, and add if not pairs pair is added to DB.
# If pair is delisted from exchange symbol and connected data are deleted from DB.
for symbol in symbols:
    try:
        if symbol["status"] == "TRADING" and symbol["symbol"] not in pairs_in_db:
            print(f"Added a new pair: {symbol['symbol']}")
            number_of_added_pairs += 1
            cursor.execute("INSERT INTO currencies (pair, base_asset, quote_asset, exchange) VALUES (?, ?, ?, ?)",
                           (symbol["symbol"], symbol["baseAsset"], symbol["quoteAsset"], exchange))
        elif symbol["status"] == "BREAK" and symbol["symbol"] in pairs_in_db:
            print(f"Exchange delisted a pair: {symbol['symbol']}")
            number_of_delisted_pairs += 1
            cursor.execute("""DELETE FROM currencies WHERE pair = ?""", (symbol["symbol"],))
    except Exception as e:
        print(symbol["symbol"])
        print(e)

if number_of_added_pairs == 0:
    print("No new pairs were listed on exchange")
if number_of_delisted_pairs == 0:
    print("No pairs were delisted from exchange")

connection.commit()