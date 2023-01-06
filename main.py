import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, date, time
from config import DB_FILE


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# year_today = date.today().year
# month_interval_start = date.today().month
# month_interval_end = date.today().month - 1
day_today = date.today().day
# day_start = datetime(year=year_today, month=month_interval_end, day=day_today)


@app.get("/")
def index(request: Request):
    pairs_filter = request.query_params.get("filter", False)
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if pairs_filter == "BTC pairs":
        cursor.execute("""
        SELECT *
        FROM currencies
        WHERE quote_asset = 'BTC';
        """)

    elif pairs_filter == "USDT pairs":
        cursor.execute("""
        SELECT *
        FROM currencies
        WHERE quote_asset = 'USDT';
        """)
    elif pairs_filter == "ETH pairs":
        cursor.execute("""
        SELECT *
        FROM currencies
        WHERE quote_asset = 'ETH';
        """)
    else:
        cursor.execute("""
                    SELECT pair, base_asset, quote_asset FROM currencies ORDER BY pair 
                """)

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "pairs": rows})


@app.get("/pair/{pair}")
def pair_detail(request: Request, pair):
    # Create connection to DB
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM strategy
    """)

    strategies = cursor.fetchall()

    cursor.execute("""
                        SELECT id, pair, base_asset, quote_asset, exchange FROM currencies WHERE pair = ? 
                    """, (pair,))

    rows = cursor.fetchone()

    cursor.execute("""
                 SELECT * FROM pairs_price WHERE pair_id = ? ORDER BY open_time DESC""", (rows["id"],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("pair_detail.html", {"request": request, "pair": rows,
                                                           "prices": prices, "strategies": strategies})


@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), pair_id: int = Form(...)):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO pair_strategy (pair_id, strategy_id) VALUES (?, ?)""",
                   (pair_id, strategy_id ))

    connection.commit()

    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)

@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name
        FROM strategy
        WHERE id = ?""", (strategy_id,))

    strat = cursor.fetchone()

    cursor.execute("""
        SELECT pair
        FROM currencies JOIN pair_strategy ON pair_strategy.pair_id = currencies.id
        WHERE strategy_id = ?""", (strategy_id,))

    pairs = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request": request, "pairs": pairs, "strategy": strat})
