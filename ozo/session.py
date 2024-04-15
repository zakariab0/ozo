import datetime
import MetaTrader5 as mt5
import time


class Session:
    london_start_time = datetime.time(7, 6)
    london_end_time = datetime.time(12, 5)
    ny_start_time = datetime.time(12, 6)
    ny_end_time = datetime.time(20, 5)
    tokyo_start_time = datetime.time(0, 6)
    tokyo_end_time = datetime.time(7, 5)
    today = datetime.datetime.today()
    current_session = ""
    now = datetime.datetime.now()
    two_hours_ago = now - datetime.timedelta(hours=2)
    three_days = today - datetime.timedelta(days=3)
    yesterday = today - datetime.timedelta(days=1)

    def get_trading_session(self):
        if self.london_start_time <= self.now.time() < self.london_end_time:
            self.current_session = "London Session"
        elif self.ny_start_time <= self.now.time() < self.ny_end_time:
            self.current_session = "New York Session"
        elif Session.tokyo_start_time <= self.now.time() < self.tokyo_end_time:
            self.current_session = "Tokyo Session"
        return self.current_session

    @staticmethod
    def get_high_low(symbol, timeframe, start, end):
        candles = mt5.copy_rates_range(symbol, timeframe, start, end)
        highest_price = max(candle[2] for candle in candles)
        lowest_price = min(candle[3] for candle in candles)
        print("Highest is: ", highest_price)
        print("Lowest is: ", lowest_price)
        return highest_price, lowest_price

    @staticmethod
    def get_high_low_old_session(actual_session, symbol, timeframe):
        hours = 3
        if actual_session == "London Session":
            print("Highs and lows of tokyo Session:")
            return Session.get_high_low(symbol, timeframe,
                                        int((datetime.datetime.combine(Session.today, Session.tokyo_start_time) + datetime.timedelta(hours=3)).timestamp()),
                                        int((datetime.datetime.combine(Session.today, Session.tokyo_end_time) + datetime.timedelta(hours=3)).timestamp()))
        elif actual_session == "Tokyo Session":
            print("Highs and lows of NY Session: ")
            return Session.get_high_low(symbol, timeframe,
                                        int((datetime.datetime.combine(Session.yesterday, Session.ny_start_time) + datetime.timedelta(hours=3)).timestamp()),
                                        int((datetime.datetime.combine(Session.yesterday, Session.ny_end_time) + datetime.timedelta(hours=3)).timestamp()))
        elif actual_session == "New York Session":
            print("Highs and lows of London Session: ")
            return Session.get_high_low(symbol, timeframe,
                                        int((datetime.datetime.combine(Session.today, Session.london_start_time) + datetime.timedelta(hours=3)).timestamp()),
                                        int((datetime.datetime.combine(Session.today, Session.london_end_time) + datetime.timedelta(hours=3)).timestamp()))

    @staticmethod
    def get_actual_session_candles(symbol, timeframe, start_time, end_time):
        return mt5.copy_rates_range(symbol, timeframe, int(start_time), int(end_time))

    @staticmethod
    def candles_actual_session(timeframe, session1, symbol):
        candles = []
        if session1 == "London Session":
            candles = Session.get_actual_session_candles(symbol, timeframe,
                                                         datetime.datetime.combine(Session.today,
                                                                                   Session.london_start_time).timestamp(),
                                                         datetime.datetime.combine(Session.today, (
                                                                     datetime.datetime.now() + datetime.timedelta(
                                                                 hours=3)).time()).timestamp())
            time.sleep(5)
        elif session1 == "New York Session":
            candles = Session.get_actual_session_candles(symbol, timeframe,
                                                         datetime.datetime.combine(Session.today,
                                                                                   Session.ny_start_time).timestamp(),
                                                         datetime.datetime.combine(Session.today, (
                                                                     datetime.datetime.now() + datetime.timedelta(
                                                                 hours=3)).time()).timestamp())
            time.sleep(5)
        elif session1 == "Tokyo Session":
            # yesterday = today - datetime.timedelta(days=1)
            candles = Session.get_actual_session_candles(symbol, timeframe,
                                                         datetime.datetime.combine(Session.today,
                                                                                   Session.tokyo_start_time).timestamp(),
                                                         datetime.datetime.combine(Session.today, (
                                                                     datetime.datetime.now() + datetime.timedelta(
                                                                 hours=3)).time()).timestamp())
            time.sleep(5)
        return candles
