import datetime
import MetaTrader5 as mt5
import time
import ozo.session as osession

# Initialize session instance
s = osession.Session()
today = datetime.datetime.today()

# Class for handling candle-related operations
class Candles:

    # Static method to get the last 10 closed candles for a given symbol and timeframe
    @staticmethod
    def get_last_10_closed_candles1(symbol1, timeframe1):
        candles1 = mt5.copy_rates_from_pos(symbol1, timeframe1, 1, 10)  # Fetch last 10 candles
        return candles1

    # Static method to get a custom number of closed candles for a given symbol and timeframe
    @staticmethod
    def get_last_custom_closed_candles(symbol1, timeframe1, count):
        candles1 = mt5.copy_rates_from_pos(symbol1, timeframe1, 1, count)  # Fetch 'count' number of candles
        return candles1  # Return the fetched candles (excludes the latest candle if it's still forming)

    # Static method to find the latest bullish candle in a list of candles
    @staticmethod
    def get_bullish_candle(candles):
        latest_bullish_candle = None  # Initialize variable to store the latest bullish candle
        n = len(candles)  # Get the total number of candles
        i = n - 1  # Start from the last candle and move backwards
        while i >= 1:
            current_candle = candles[i]  # Get the current candle
            if current_candle[4] > current_candle[1]:  # Check if close price (index 4) > open price (index 1)
                latest_bullish_candle = current_candle  # Store the latest bullish candle
                break  # Exit the loop once the latest bullish candle is found
            i -= 1  # Move to the previous candle
        return latest_bullish_candle  # Return the latest bullish candle (or None if none found)

    # Static method to find the latest bearish candle in a list of candles
    @staticmethod
    def get_bearish_candle(candles):
        latest_bearish_candle = None  # Initialize variable to store the latest bearish candle
        n = len(candles)  # Get the total number of candles
        i = n - 1  # Start from the last candle and move backwards
        while i >= 1:
            current_candle = candles[i]  # Get the current candle
            if current_candle[1] > current_candle[4]:  # Check if open price (index 1) > close price (index 4)
                latest_bearish_candle = current_candle  # Store the latest bearish candle
                break  # Exit the loop once the latest bearish candle is found
            i -= 1  # Move to the previous candle
        return latest_bearish_candle  # Return the latest bearish candle (or None if none found)

    # Static method to find the lowest low price in a list of candles
    @staticmethod
    def get_lowest_low(candles):
        lowest_low = float('inf')  # Initialize with positive infinity
        for candle in candles:
            low_price = candle[3]  # Get the low price (index 3)
            if low_price < lowest_low:  # Check if the current low is lower than the recorded lowest
                lowest_low = low_price  # Update the lowest low
        return lowest_low  # Return the lowest low price

    # Static method to find the highest high price in a list of candles
    @staticmethod
    def get_highest_high(candles):
        highest_high = float('-inf')  # Initialize with negative infinity
        for candle in candles:
            high_price = candle[2]  # Get the high price (index 2)
            if high_price > highest_high:  # Check if the current high is higher than the recorded highest
                highest_high = high_price  # Update the highest high
        return highest_high  # Return the highest high price

    # Static method to get the last closed candle for a given symbol and timeframe
    @staticmethod
    def get_last_closed_candle(symbol1, timeframe1):
        candle1 = mt5.copy_rates_from_pos(symbol1, timeframe1, 1, 1)  # Fetch the last closed candle
        return candle1  # Return the last closed candle