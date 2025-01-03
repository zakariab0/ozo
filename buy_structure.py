import time
import MetaTrader5 as mt5
import ozo.candles as ocandles
import ozo.trade as otrades
import ozo.session as oSession

# Class for handling buy-related trading logic
class Buy:
    # Initialize attributes for buy phase
    entry = 0  # Entry price for the trade
    tp = 0     # Take-profit price
    sl = 0     # Stop-loss price
    c = ocandles.Candles()  # Instance for candle-related operations
    t = otrades.Trade()     # Instance for trade-related operations
    s = oSession.Session()  # Instance for session-related operations

    # Method to handle buy structure logic
    def buy_structure(self, highest_last_bullish_candle, symbol, timeframe, volume, bot, message):
        bearish_count = 0  # Counter to track consecutive bearish candles
        entered = False    # Flag to track if a trade has been entered
        highest_last_bullish_price = highest_last_bullish_candle[2]  # Highest price of the last bullish candle
        time.sleep(2)  # Wait for 2 seconds before starting

        # Get the last closed candle
        last_closed_candle = self.c.get_last_closed_candle(symbol, timeframe)[0]

        # Loop until a trade is entered
        while not entered:
            changed = False  # Flag to track if the structure has changed
            a = self.c.get_last_closed_candle(symbol, timeframe)  # Get the latest closed candle
            print(a)  # Debugging: Print the latest candle data

            # Check if the candle has changed
            if a[0] != last_closed_candle:
                last_closed_candle = a[0]  # Update the last closed candle
                time.sleep(5)  # Wait for 5 seconds

                # Check for a breakout (price closes above the highest bullish price)
                if last_closed_candle[4] > last_closed_candle[1] and last_closed_candle[4] > highest_last_bullish_price:
                    bot.reply_to(message, "breakout, entered")  # Notify breakout
                    tick = mt5.symbol_info_tick(symbol)  # Get current tick data
                    lowest_candle = self.c.get_lowest_low(self.c.get_last_10_closed_candles1(symbol, timeframe))  # Get lowest low of last 10 candles
                    self.tp = tick.bid + (tick.bid - lowest_candle)  # Calculate take-profit
                    self.sl = lowest_candle  # Set stop-loss
                    self.entry = tick.bid  # Set entry price

                    # Prepare and send trade details
                    msg = "symbol: " + str(symbol) + " volume: " + str(volume) + " sl: " + str(self.sl) + " tp: " + str(self.tp)
                    bot.reply_to(message, msg)

                    # Enter the buy trade
                    self.t.enter_buy_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                    return True  # Exit the loop after entering the trade

                # Check for a bearish candle (price closes lower than open)
                elif last_closed_candle[4] < last_closed_candle[1]:
                    bearish_count += 1  # Increment bearish count
                    str1 = "bearish count: " + str(bearish_count)
                    bot.reply_to(message, str1)  # Notify bearish count
                    time.sleep(280)  # Wait for 280 seconds

                # Check for a new structure after at least 2 bearish candles
                elif last_closed_candle[4] > last_closed_candle[1] and bearish_count >= 2:
                    while not changed:
                        new = self.c.get_last_closed_candle(symbol, timeframe)[0]  # Get the latest candle
                        if new[1] > new[4]:  # Check for a new bearish candle
                            bot.reply_to(message, "new structure:")  # Notify new structure
                            bot.reply_to(message, "old: " + str(highest_last_bullish_candle))
                            bot.reply_to(message, "new: " + str(last_closed_candle))
                            highest_last_bullish_candle = last_closed_candle  # Update the highest bullish candle
                            highest_last_bullish_price = highest_last_bullish_candle[3]  # Update the highest price
                            bearish_count = 0  # Reset bearish count
                            changed = True  # Mark structure as changed
                            time.sleep(280)  # Wait for 280 seconds

                        # Check for a breakout in the new structure
                        elif new[4] > highest_last_bullish_price:
                            bot.reply_to(message, "breakout, entered")  # Notify breakout
                            tick = mt5.symbol_info_tick(symbol)  # Get current tick data
                            lowest_candle = self.c.get_lowest_low(self.c.get_last_10_closed_candles1(symbol, timeframe))  # Get lowest low of last 10 candles
                            self.tp = tick.bid + (tick.bid - lowest_candle)  # Calculate take-profit
                            self.sl = lowest_candle  # Set stop-loss

                            # Prepare and send trade details
                            msg = "symbol: " + str(symbol) + " volume: " + str(volume) + " sl: " + str(self.sl) + " tp: " + str(self.tp)
                            bot.reply_to(message, msg)

                            # Enter the buy trade
                            self.t.enter_buy_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                            return True  # Exit the loop after entering the trade

                        # Check for a bullish candle in the new structure
                        elif new[1] < new[4]:
                            last_closed_candle = new  # Update the last closed candle
                            bot.reply_to(message, "changed last bullish, waiting for breakout or new structure")
                            time.sleep(280)  # Wait for 280 seconds

                # If no breakout or new structure, wait for the next candle
                else:
                    bot.reply_to(message, "bullish, waiting for breakout")
                    time.sleep(280)  # Wait for 280 seconds
            else:
                time.sleep(10)  # Wait for 10 seconds if no new candle

    # Method to handle second entry logic
    def second_entry(self, session, symbol, volume, bot, message):
        # Loop while the trading session is active
        while self.s.get_trading_session() == session:
            tick = mt5.symbol_info_tick(symbol)  # Get current tick data
            # Check if the price is below the entry price
            if tick.bid < self.entry or tick.ask < self.entry:
                # Check if the price is near the midpoint between entry and stop-loss
                if (self.sl + ((self.entry - self.sl) / 2)) > tick.bid or (self.sl + ((self.entry - self.sl) / 2)) > tick.ask:
                    # Enter the second buy trade
                    self.t.enter_buy_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                    bot.reply_to(message, "the bot has entered the second entry")
                    return True  # Exit the loop after entering the trade
        return False  # Return False if no second entry is made