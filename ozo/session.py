import datetime
import MetaTrader5 as mt5
import time

# Class for handling trading session-related operations
class Session:
    # Define session start and end times
    london_start_time = datetime.time(7, 6)  # London session start time
    london_end_time = datetime.time(12, 5)   # London session end time
    ny_start_time = datetime.time(12, 6)     # New York session start time
    ny_end_time = datetime.time(20, 5)       # New York session end time
    tokyo_start_time = datetime.time(0, 6)   # Tokyo session start time
    tokyo_end_time = datetime.time(7, 5)     # Tokyo session end time

    # Define date and time variables
    today = datetime.datetime.today()  # Current date
    now = datetime.datetime.now()      # Current date and time
    two_hours_ago = now - datetime.timedelta(hours=2)  # Time 2 hours ago
    three_days = today - datetime.timedelta(days=3)    # Date 3 days ago
    yesterday = today - datetime.timedelta(days=1)     # Yesterday's date

    # Variable to store the current trading session
    current_session = ""

    # Method to get the current trading session
    def get_trading_session(self):
        """
        Determines the current trading session based on the current time.
        Returns:
            str: The current trading session ("London Session", "New York Session", or "Tokyo Session").
        """
        if self.london_start_time <= self.now.time() < self.london_end_time:
            self.current_session = "London Session"
        elif self.ny_start_time <= self.now.time() < self.ny_end_time:
            self.current_session = "New York Session"
        elif self.tokyo_start_time <= self.now.time() < self.tokyo_end_time:
            self.current_session = "Tokyo Session"
        return self.current_session

    # Static method to get the highest and lowest prices for a given symbol and timeframe
    @staticmethod
    def get_high_low(symbol, timeframe, start, end):
        """
        Fetches the highest and lowest prices for a given symbol and timeframe within a specified range.
        Args:
            symbol (str): The trading symbol (e.g., "EURUSD").
            timeframe: The timeframe for candle data.
            start (int): Start timestamp for the range.
            end (int): End timestamp for the range.
        Returns:
            tuple: (highest_price, lowest_price)
        """
        candles = mt5.copy_rates_range(symbol, timeframe, start, end)  # Fetch candles within the range
        highest_price = max(candle[2] for candle in candles)  # Get the highest price
        lowest_price = min(candle[3] for candle in candles)   # Get the lowest price
        print("Highest is: ", highest_price)  # Debugging: Print the highest price
        print("Lowest is: ", lowest_price)    # Debugging: Print the lowest price
        return highest_price, lowest_price

    # Static method to get the high and low prices of the previous session
    @staticmethod
    def get_high_low_old_session(actual_session, symbol, timeframe):
        """
        Fetches the highest and lowest prices of the previous session.
        Args:
            actual_session (str): The current trading session.
            symbol (str): The trading symbol (e.g., "EURUSD").
            timeframe: The timeframe for candle data.
        Returns:
            tuple: (highest_price, lowest_price)
        """
        hours = 3  # Time adjustment for session timestamps
        if actual_session == "London Session":
            print("Highs and lows of Tokyo Session:")
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

    # Static method to get candles for the current session
    @staticmethod
    def get_actual_session_candles(symbol, timeframe, start_time, end_time):
        """
        Fetches candles for the current session within a specified range.
        Args:
            symbol (str): The trading symbol (e.g., "EURUSD").
            timeframe: The timeframe for candle data.
            start_time (int): Start timestamp for the range.
            end_time (int): End timestamp for the range.
        Returns:
            list: List of candles within the range.
        """
        return mt5.copy_rates_range(symbol, timeframe, int(start_time), int(end_time))

    # Static method to get candles for the current session
    @staticmethod
    def candles_actual_session(timeframe, session1, symbol):
        """
        Fetches candles for the current session.
        Args:
            timeframe: The timeframe for candle data.
            session1 (str): The current trading session.
            symbol (str): The trading symbol (e.g., "EURUSD").
        Returns:
            list: List of candles for the current session.
        """
        candles = []
        if session1 == "London Session":
            candles = Session.get_actual_session_candles(symbol, timeframe,
                                                         datetime.datetime.combine(Session.today, Session.london_start_time).timestamp(),
                                                         datetime.datetime.combine(Session.today, (datetime.datetime.now() + datetime.timedelta(hours=3)).time()).timestamp())
            time.sleep(5)
        elif session1 == "New York Session":
            candles = Session.get_actual_session_candles(symbol, timeframe,
                                                         datetime.datetime.combine(Session.today, Session.ny_start_time).timestamp(),
                                                         datetime.datetime.combine(Session.today, (datetime.datetime.now() + datetime.timedelta(hours=3)).time()).timestamp())
            time.sleep(5)
        elif session1 == "Tokyo Session":
            candles = Session.get_actual_session_candles(symbol, timeframe,
                                                         datetime.datetime.combine(Session.today, Session.tokyo_start_time).timestamp(),
                                                         datetime.datetime.combine(Session.today, (datetime.datetime.now() + datetime.timedelta(hours=3)).time()).timestamp())
            time.sleep(5)
        return candles