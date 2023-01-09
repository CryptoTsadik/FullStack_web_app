# FullStack_web_app
FullStack_web_app

Under development

Web app downloads data from Binance.com API, saves it to Sqlite DB, calculates technical indicators' values and conduct different filtering and backtesting.

Developed features:
  - Create DB and it's schema.
  - Download all tradeable pairs from Binance.com
  - Download historical price and volume data from exchange and save it to DB.
  - Update price and volume data in DB.
  - Delete pairs' all related data from DB in case of delisting from exchange.
  - Display a web page with list of all available pairs and some additional data. Some basic filtering may be applied through dropdown menu.
  - Display a web page for every symbol with interective chart and price history.
  
Bugs to fix:
  - Display the OHLC data of low priced altcoins with decimals, suppressing scientific notations.

Bugs fixed:
  - Fixed the missing of inserting a pair_id in DB while updating the price data.
  
  
Features to be developed:
  - Calculation of techical indicators' values and store them in DB.
  - Add advanced filtering, including filtering by indicators' values.
  - Implement module to conduct backtesting. 
        As a result of backtesting, in addition to the basic statistics of the strategy performance, 
        the application shows the probability of reaching certain price ranges, 
        based on historical ruturns, which followed after certain indicators' values.
  
    Should include parameters: 
      - select techical indicator or a group of indicators to backtest
      - select  type of takeprofit
      - select type of stoploss 
  - Module to execute trades and track their performance.
