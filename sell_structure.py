import time
import MetaTrader5 as mt5
import ozo.candles as ocandles
import ozo.trade as otrades
import ozo.session as oSession

# Class for handling sell-related trading logic
class Sell:
    # Initialize attributes for sell phase
    entry = 0  # Entry price for the trade
    tp = 0     # Take-profit price
    sl = 0     # Stop-loss price
    c = ocandles.Candles()  # Instance for candle-related operations
    t = otrades.Trade()     # Instance for trade-related operations
    s = oSession.Session()  # Instance for session-related operations

    # Method to handle sell structure logic
    def sell_structure(self, lowest_last_bearish_candle, symbol, timeframe, volume, bot, message):
        """
        Monitors price action to identify sell structures and enter trades.
        Args:
            lowest_last_bearish_candle (list): The lowest bearish candle in the structure.
            symbol (str): The trading symbol (e.g., "EURUSD").
            timeframe: The timeframe for candle data.
            volume (float): The trade volume.
            bot: The bot instance for sending messages.
            message: The message object for replying to the user.
        Returns:
            bool: True if a trade is entered, False otherwise.
        """
        entered = False  # Flag to track if a trade has been entered
        bullish_count = 0  # Counter to track consecutive bullish candles
        lowest_last_bearish_price = lowest_last_bearish_candle[3]  # Lowest price of the last bearish candle
        time.sleep(2)  # Wait for 2 seconds before starting

        # Get the last closed candle
        last_closed_candle = self.c.get_last_closed_candle(symbol, timeframe)[0]

        # Loop until a trade is entered
        while not entered:
            changed = False  # Flag to track if the structure has changed
            a = self.c.get_last_closed_candle(symbol, timeframe)  # Get the latest closed candle
            print(a[0])  # Debugging: Print the latest candle timestamp

            # Check if the candle has changed
            if last_closed_candle != a[0]:
                last_closed_candle = a[0]  # Update the last closed candle

                # Check for a breakout (price closes below the lowest bearish price)
                if last_closed_candle[4] < last_closed_candle[1] and last_closed_candle[4] < lowest_last_bearish_price:
                    bot.reply_to(message, "entered")  # Notify trade entry
                    tick = mt5.symbol_info_tick(symbol)  # Get current tick data
                    highest_candle = self.c.get_highest_high(self.c.get_last_10_closed_candles1(symbol, timeframe))  # Get highest high of last 10 candles
                    self.tp = tick.bid - (highest_candle - tick.bid)  # Calculate take-profit
                    self.sl = highest_candle  # Set stop-loss
                    self.entry = tick.bid  # Set entry price

                    # Prepare and send trade details
                    msg = "symbol: " + str(symbol) + " volume: " + str(volume) + " sl: " + str(self.sl) + " tp: " + str(self.tp)
                    bot.reply_to(message, msg)

                    # Enter the sell trade
                    self.t.enter_sell_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                    return True  # Exit the loop after entering the trade

                # Check for a bullish candle (price closes higher than open)
                elif last_closed_candle[4] > last_closed_candle[1]:
                    bullish_count += 1  # Increment bullish count
                    bot.reply_to(message, "bullish count: " + str(bullish_count))  # Notify bullish count
                    time.sleep(280)  # Wait for 280 seconds

                # Check for a new structure after at least 2 bullish candles
                elif last_closed_candle[4] < last_closed_candle[1] and bullish_count >= 2:
                    while not changed:
                        new = self.c.get_last_closed_candle(symbol, timeframe)[0]  # Get the latest candle
                        if new[1] < new[4]:  # Check for a new bullish candle
                            bot.reply_to(message, "new structure:")  # Notify new structure
                            bot.reply_to(message, "old: " + str(lowest_last_bearish_candle))
                            bot.reply_to(message, "new: " + str(last_closed_candle))
                            structure = last_closed_candle  # Update the structure
                            lowest_last_bearish_price = structure[3]  # Update the lowest bearish price
                            bullish_count = 0  # Reset bullish count
                            changed = True  # Mark structure as changed
                            time.sleep(280)  # Wait for 280 seconds

                        # Check for a breakout in the new structure
                        elif new[4] < lowest_last_bearish_price:
                            bot.reply_to(message, "breakout, entered")  # Notify breakout
                            tick = mt5.symbol_info_tick(symbol)  # Get current tick data
                            highest_candle = self.c.get_highest_high(self.c.get_last_10_closed_candles1(symbol, timeframe))  # Get highest high of last 10 candles
                            self.tp = tick.bid - (highest_candle - tick.bid)  # Calculate take-profit
                            self.sl = highest_candle  # Set stop-loss
                            self.entry = tick.bid  # Set entry price

                            # Prepare and send trade details
                            msg = "symbol: " + str(symbol) + " volume: " + str(volume) + " sl: " + str(self.sl) + " tp: " + str(self.tp)
                            bot.reply_to(message, msg)

                            # Enter the sell trade
                            self.t.enter_sell_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                            return True  # Exit the loop after entering the trade

                        # Check for a bearish candle in the new structure
                        elif new[1] > new[4]:
                            last_closed_candle = new  # Update the last closed candle
                            bot.reply_to(message, "changed last bearish, waiting for breakout or new structure")
                            time.sleep(280)  # Wait for 280 seconds

                # If no breakout or new structure, wait for the next candle
                else:
                    bot.reply_to(message, "bearish, waiting for breakout")
                    time.sleep(280)  # Wait for 280 seconds
            else:
                time.sleep(10)  # Wait for 10 seconds if no new candle

    # Method to handle second entry logic
    def second_entry(self, session, symbol, volume, bot, message):
        """
        Monitors the price during a trading session for a second entry opportunity.
        Args:
            session (str): The current trading session.
            symbol (str): The trading symbol (e.g., "EURUSD").
            volume (float): The trade volume.
            bot: The bot instance for sending messages.
            message: The message object for replying to the user.
        Returns:
            bool: True if a second entry is made, False otherwise.
        """
        # Loop while the trading session is active
        while self.s.get_trading_session() == session:
            tick = mt5.symbol_info_tick(symbol)  # Get current tick data
            # Check if the price is above the entry price
            if tick.bid > self.entry or tick.ask > self.entry:
                # Check if the price is near the midpoint between entry and stop-loss
                if (self.entry + (self.sl - self.entry) / 2) < tick.ask:
                    # Enter the second sell trade
                    self.t.enter_sell_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                    bot.reply_to(message, "the bot has entered")
                    return True  # Exit the loop after entering the trade
        return False  # Return False if no second entry is made