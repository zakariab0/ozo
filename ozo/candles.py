import datetime
import MetaTrader5 as mt5
import time
import ozo.session as osession

s = osession.Session()
today = datetime.datetime.today()

class Candles:

    @staticmethod
    def get_last_10_closed_candles1(symbol1, timeframe1):
        candles1 = mt5.copy_rates_from_pos(symbol1, timeframe1, 1, 10)
        return candles1

    @staticmethod
    def get_last_custom_closed_candles(symbol1, timeframe1, count):
        candles1 = mt5.copy_rates_from_pos(symbol1, timeframe1, 1, count)
        return candles1  # Exclude the latest candle



    @staticmethod
    def get_bullish_candle(candles):
        latest_bullish_candle = None
        n = len(candles)
        i = n - 1  # Start from the last candle and move backwards
        while i >= 1:
            current_candle = candles[i]
            if current_candle[4] > current_candle[1]:  # Compare close price (index 4) with open price (index 1)
                latest_bullish_candle = current_candle
                break  # We found the latest bullish candle, so we can stop searching
            i -= 1
        return latest_bullish_candle

    @staticmethod
    def get_bearish_candle(candles):
        latest_bearish_candle = None
        n = len(candles)
        i = n - 1
        while i >= 1:
            current_candle = candles[i]
            if current_candle[1] > current_candle[4]:  # Compare close price (index 4) with open price (index 1)
                latest_bearish_candle = current_candle
                break  # We found the latest bearish candle, so we can stop searching
            i -= 1
        return latest_bearish_candle

    @staticmethod
    def get_lowest_low(candles):
        lowest_low = float('inf')  # Initialize with positive infinity
        for candle in candles:
            low_price = candle[3]  # Index 3 corresponds to the low price
            if low_price < lowest_low:
                lowest_low = low_price
        return lowest_low

    @staticmethod
    def get_highest_high(candles):
        highest_high = float('-inf')  # Initialize with negative infinity
        for candle in candles:
            high_price = candle[2]  # Index 2 corresponds to the high price
            if high_price > highest_high:
                highest_high = high_price
        return highest_high

    @staticmethod
    def get_last_closed_candle(symbol1, timeframe1):
        candle1 = mt5.copy_rates_from_pos(symbol1, timeframe1, 1, 1)
        return candle1
