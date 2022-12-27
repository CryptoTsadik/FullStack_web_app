import sqlite3
from binance import Client
import datetime

# Create connection to DB
connection = sqlite3.connect("app.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Call the DB to get IDs and pairs
cursor.execute("""
                SELECT id, pair FROM currencies
""")

rows = cursor.fetchall()

# Create connection to Binance API
client = Client(requests_params={"timeout": 60})
pairs = [row["pair"] for row in rows]
pair_dict = {}
price_values = {}

# Create dicts with pair name as a key and pair id as value
# to use pair_id in DB
for row in rows:
    pair = row["pair"]
    pair_dict[pair] = row["id"]


# Get prices data, save it to dictionary
for i in range(0, len(pairs)):
    pair_name = pairs[i]
    print(f"Processing pair: {pair_name}, Pair id: {pair_dict[pair_name]}, Counter of loaded pairs: {i + 1} of {len(pair_dict)}")
    klines = client.get_historical_klines(pair_name, Client.KLINE_INTERVAL_1DAY ,  start_str="2017-08-01", end_str="2022-01-01")
    pair_id = pair_dict[pair_name]
    price_values[pair_id] = klines

# Iterate over dictionary with prices and IDs to insert values into DB.
for pair_id, list_of_prices in price_values.items():
    for value in list_of_prices:
        open_time = value[0]
        open = value[1]
        high = value[2]
        low = value[3]
        close = value[4]
        volume = value[5]
        quote_asset_volume = value[7]
        number_of_trades = value[8]
        taker_buy_base_asset_volume = value[9]
        taker_buy_quote_asset_volume = value[10]
        cursor.execute("""
                INSERT INTO pairs_price (pair_id, open_time, open, high, low, close, volume,
                quote_asset_volume, number_of_trades, taker_buy_base_asset_volume,
                taker_buy_quote_asset_volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
                       (pair_id, open_time, open, high, low, close, volume, quote_asset_volume, number_of_trades,
                        taker_buy_base_asset_volume, taker_buy_quote_asset_volume))

connection.commit()