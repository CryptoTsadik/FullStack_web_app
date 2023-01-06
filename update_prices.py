import sqlite3
from binance import Client
import datetime
from config import DB_FILE

# Create connection to DB
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Call the DB to get pairs, IDs and last candle open time.
cursor.execute("""
                SELECT pair, pair_id, max(open_time)
                FROM currencies
                LEFT JOIN pairs_price ON pairs_price.pair_id = currencies.id
                GROUP BY pair
                ORDER BY open_time DESC
""")

rows = cursor.fetchall()

# Create connection to Binance API
client = Client(requests_params={"timeout": 60})
pairs = [row["pair"] for row in rows]
pair_ids = [row["pair_id"] for row in rows]
pair_dict = {}
price_values = {}
last_candle = max([row["max(open_time)"] for row in rows if row["max(open_time)"] is not None])
print(True)

# Create dicts with pair name as a key and pair id as value
# to use pair_id in DB
for row in rows:
    pair = row["pair"]
    if row["pair_id"] <= max(pair_ids):
        pair_dict[pair] = row["pair_id"]
    else:
        pair_dict[pair] = max(pair_ids) + 1

# Get prices data and write it do dictionary with pair_id as a key
for i in range(0, len(pairs)):
    pair_name = pairs[i]
    print(f"Updating pair: {pair_name}, Pair id: {pair_dict[pair_name]}, "
          f"Counter of loaded pairs: {i + 1} of {len(pair_dict)}, "
          f"from date: {datetime.datetime.fromtimestamp(int(last_candle) / 1000)}")
    klines = client.get_historical_klines(pair_name, Client.KLINE_INTERVAL_1DAY,  start_str=last_candle)
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