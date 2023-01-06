import sqlite3

connection = sqlite3.connect("app.db")

cursor = connection.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY,
            pair TEXT NOT NULL UNIQUE,
            base_asset TEXT NOT NULL,
            quote_asset TEXT NOT NULL,
            exchange TEXT NOT NULL
            )
            """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS pairs_price (
            id INTEGER PRIMARY KEY,
            pair_id INTEGER,
            open_time INTEGER NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL,
            quote_asset_volume REAL NOT NULL,
            number_of_trades REAL NOT NULL,
            taker_buy_base_asset_volume REAL NOT NULL,
            taker_buy_quote_asset_volume REAL NOT NULL,
            FOREIGN KEY (pair_id) REFERENCES currencies (id) 
            ON DELETE CASCADE
            )
            """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategy (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
            )
            """)

cursor.execute("""
        CREATE TABLE IF NOT EXISTS pair_strategy (
            pair_id INTEGER NOT NULL,
            strategy_id INTEGER NOT NULL,
            FOREIGN KEY (pair_id) REFERENCES currencies (id),
            FOREIGN KEY (strategy_id) REFERENCES strategy (id)
            )
            """)

strategies = ["Strategy_1", "Strategy_2"]

for strategy in strategies:
    cursor.execute("""
        INSERT INTO strategy (name) VALUES (?)""", (strategy,))

connection.commit()
