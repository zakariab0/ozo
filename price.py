import time
import MetaTrader5 as mt5

# Class for handling price-related operations
class Price:

    # Static method to detect late entry based on liquidity sweeps
    @staticmethod
    def late_enter(highest, lowest, candles):
        """
        Detects liquidity sweeps and determines the direction (from highest or lowest).
        Args:
            highest (float): The highest price level.
            lowest (float): The lowest price level.
            candles (list): List of candle data.
        Returns:
            tuple: (direction, last_structure)
                - direction: "true" if sweep from highest, "false" if sweep from lowest.
                - last_structure: The last candle structure before the sweep.
        """
        print(candles[0])  # Debugging: Print the first candle
        print("highest: ", highest)  # Debugging: Print the highest price
        print("lowest: ", lowest)  # Debugging: Print the lowest price

        a = candles[0]  # Initialize variable to track the highest sweep candle
        b = candles[0]  # Initialize variable to track the lowest sweep candle
        position_a = 0  # Position of the highest sweep candle
        position_b = 0  # Position of the lowest sweep candle

        # Iterate through candles to find the highest and lowest sweep points
        for i, c in enumerate(candles):
            if a != b:
                # Update the highest sweep candle if conditions are met
                if highest < c[2] < a[2] and c[0] < a[0]:
                    a = c
                    position_a = i
                # Update the lowest sweep candle if conditions are met
                if b[3] < c[3] < lowest and c[0] < b[0]:
                    b = c
                    position_b = i
            else:
                # Initialize the highest and lowest sweep candles
                if highest < c[2]:
                    a = c
                    position_a = i
                if lowest > c[3]:
                    b = c
                    position_b = i

        # Check if both highest and lowest sweeps occurred
        if a[2] > highest and b[3] < lowest:
            print("a")
            if a[0] < b[0]:  # Sweep from highest occurred first
                print("b")
                print("liquidity sweep from highest")
                print("get last bearish candle before ls")
                position_a -= 1
                # Find the last bearish candle before the sweep
                while position_a >= 0:
                    if candles[position_a][1] > candles[position_a][4]:  # Bearish candle condition
                        print("Bullish candle that did lq sweep from highest in function: ", a)
                        a = candles[position_a]
                        print("bearish candle before lq sweep: ", a)
                        return "true", a  # Return direction and last structure
                    else:
                        position_a -= 1
                return -1  # Return -1 if no bearish candle is found
            elif b[0] < a[0]:  # Sweep from lowest occurred first
                print("c")
                print("liquidity sweep from lowest")
                print("get last bullish candle before ls")
                position_b -= 1
                # Find the last bullish candle before the sweep
                while position_b >= 0:
                    if candles[position_b][1] < candles[position_b][4]:  # Bullish candle condition
                        print("bearish candle that did lq sweep from highest in function: ", b)
                        b = candles[position_b]
                        print("Bullish candle before lq sweep: ", b)
                        return "false", b  # Return direction and last structure
                    else:
                        position_b -= 1
        # Check if only the highest sweep occurred
        elif a[2] > highest:
            print("liquidity sweep from highest")
            print("get last bearish candle before ls")
            position_a -= 1
            print("position_a1: ", position_a)
            # Find the last bearish candle before the sweep
            while position_a >= 0:
                if candles[position_a][1] > candles[position_a][4]:  # Bearish candle condition
                    print("Bullish candle that did lq sweep from highest in function: ", a)
                    a = candles[position_a]
                    print("bearish candle before lq sweep: ", a)
                    return "true", a  # Return direction and last structure
                else:
                    position_a -= 1
        # Check if only the lowest sweep occurred
        elif b[3] < lowest:
            print("e")
            print("b: ", b[3])
            print("lowest: ", lowest)
            print("liquidity sweep from lowest")
            print("get last bullish candle before ls")
            position_b -= 1
            # Find the last bullish candle before the sweep
            while position_b >= 0:
                if candles[position_b][1] < candles[position_b][4]:  # Bullish candle condition
                    print("Bearish candle that did lq sweep from highest in function: ", b)
                    b = candles[position_b]
                    print("Bullish candle before lq sweep: ", b)
                    return "false", b  # Return direction and last structure
                else:
                    position_b -= 1
        # If no sweep is detected, return -1 and an empty tuple
        else:
            return -1, ()

    # Static method to detect liquidity sweeps in real-time
    @staticmethod
    def get_liquidity(highest_price_eu, lowest_price_eu, highest_price_gu, lowest_price_gu):
        """
        Detects liquidity sweeps in real-time for EURUSD and GBPUSD.
        Args:
            highest_price_eu (float): Highest price level for EURUSD.
            lowest_price_eu (float): Lowest price level for EURUSD.
            highest_price_gu (float): Highest price level for GBPUSD.
            lowest_price_gu (float): Lowest price level for GBPUSD.
        Returns:
            tuple: (liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu)
                - Each flag indicates if a liquidity sweep occurred for the respective condition.
        """
        liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = False, False, False, False
        symbol_eu = "EURUSD"
        symbol_gu = "GBPUSD"

        # Loop until a liquidity sweep is detected
        while not liquid_low_eu and not liquid_high_eu and not liquid_low_gu and not liquid_high_gu:
            tick_eu = mt5.symbol_info_tick(symbol_eu)  # Get tick data for EURUSD
            tick_gu = mt5.symbol_info_tick(symbol_gu)  # Get tick data for GBPUSD
            time.sleep(3)  # Wait for 3 seconds before checking again

            # Accessing the bid and ask prices from the tick data
            actual_bid_price_eu = tick_eu.bid
            actual_ask_price_eu = tick_eu.ask
            actual_bid_price_gu = tick_gu.bid
            actual_ask_price_gu = tick_gu.ask

            # Debugging: Print bid and ask prices
            print("Bid eu: ", actual_bid_price_eu, ", Ask eu: ", actual_ask_price_eu)
            print("Bid gu: ", actual_bid_price_gu, ", Ask gu: ", actual_ask_price_gu)

            # Check for liquidity sweeps
            if actual_bid_price_eu < lowest_price_eu:  # Sweep from lowest in EURUSD
                print("Liquidity is swept from lowest of EU, searching for buy3")
                return True, False, False, False
            elif actual_ask_price_eu > highest_price_eu:  # Sweep from highest in EURUSD
                print("Liquidity is swept from highest of EU, searching for sell3")
                return False, True, False, False
            elif actual_bid_price_gu < lowest_price_gu:  # Sweep from lowest in GBPUSD
                print("Liquidity is swept from lowest of GU, searching for buy3")
                return False, False, True, False
            elif actual_ask_price_gu > highest_price_gu:  # Sweep from highest in GBPUSD
                print("Liquidity is swept from highest of GU, searching for sell3")
                return False, False, False, True