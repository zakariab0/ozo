import datetime
import MetaTrader5 as mt5
import time

import ozo.trade as oTrade
import ozo.candles as oCandles

t = oTrade.Trade()
c = oCandles.Candles()

class Msnr:
    today = datetime.date.today()
    symbol = "XAUUSD"
    while True:
        if not mt5.initialize():
            print("Initialize failed")
            mt5.shutdown()
        h1_delta = datetime.timedelta(hours=3)
        current_time = (datetime.datetime.now() + h1_delta).time()
        candles = c.get_last_custom_closed_candles(symbol, mt5.TIMEFRAME_H4, 4)
        if len(candles) >= 4:
            # Extract candle information
            candle1 = candles[-3]
            print("candle1", candle1)
            candle2 = candles[-2]
            print("candle2", candle2)
            candle3 = candles[-1]
            print("candle3", candle3)
            buy_tp = candle2[3] + 3
            buy_sl = candle2[3] - 2
            sell_tp = candle2[3] - 3
            sell_sl = candle2[3] + 2
            # Check candle directions
            if candle1[4] > candle1[1] and candle2[4] < candle2[1] and candle3[4] < candle3[1]:
                print("i am here1")
                sell_limit_price = candle2[4]
                t.enter_sell_limit_trade(volume=0.1, tp=sell_tp, sl=sell_sl, symbol=symbol, price=sell_limit_price)
            elif candle1[4] < candle1[1] and candle2[4] > candle2[1] and candle3[4] > candle3[1]:
                print(candle1[4], " > ", candle1[1])
                print(candle2[4], " > ", candle2[1])
                print("i am here2")
                buy_limit_price = candle2[4]
                t.enter_buy_limit_trade(volume=0.1, tp=buy_tp, sl=buy_sl, symbol=symbol, price=buy_limit_price)
            if candle2[4] > candle2[1] and candle3[1] > candle3[4]:
                print("i am here3")
                buy_limit_price = candle2[4]
                t.enter_buy_limit_trade(volume=0.1, tp=buy_tp, sl=buy_sl, symbol=symbol, price=buy_limit_price)
            elif candle2[4] < candle2[1] and candle3[1] < candle3[4]:
                print("i am here4")
                sell_limit_price = candle2[4]
                t.enter_sell_limit_trade(volume=0.1, tp=sell_tp, sl=sell_sl, symbol=symbol, price=sell_limit_price)

        time.sleep(3600 * 4)
