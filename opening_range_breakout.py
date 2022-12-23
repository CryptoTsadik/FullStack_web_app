import sqlite3
from binance import Client
import datetime as date

connection = sqlite3.connect("app.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id FROM strategy
    WHERE name = 'Strategy_1'
    """)

strategy_id = cursor.fetchone()["id"]

cursor.execute("""
    SELECT pair
    FROM currencies
    JOIN pair_strategy ON pair_strategy.pair_id = currencies.id
    WHERE pair_strategy.strategy_id = ?""", (strategy_id,))

pairs = cursor.fetchall()
symbols = [pair["pair"] for pair in pairs]
print(symbols)




