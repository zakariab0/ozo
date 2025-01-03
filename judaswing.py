import datetime
import MetaTrader5 as mt5
import time
import ozo.session as osession
import ozo.price as oprice
import ozo.trade as otrade
import ozo.candles as ocandles
import ozo.buy_structure as obuy
import ozo.sell_structure as osell

# Main class for the Judaswing trading strategy
class Judaswing:
    # Initialize trading flags and variables
    buy = False  # Flag to track if a buy trade is active
    sell = False  # Flag to track if a sell trade is active
    tp = 0  # Take-profit price
    sl = 0  # Stop-loss price
    entry = 0  # Entry price
    volume = 0.1  # Trade volume
    last_candle = []  # Stores the last candle data
    last_candle_eu = []  # Stores the last candle data for EURUSD
    last_candle_gu = []  # Stores the last candle data for GBPUSD
    old_last_bearish_candle = []  # Stores the last bearish candle data
    old_last_bullish_candle = []  # Stores the last bullish candle data
    structure = []  # Stores the current market structure
    last_closed_candle = []  # Stores the last closed candle data
    today = datetime.datetime.today()  # Current date
    timeframe = mt5.TIMEFRAME_M5  # Default timeframe (5 minutes)
    late_a = ""  # Stores late entry status
    entered_london = False  # Flag to track if a trade was entered during the London session
    entered_ny = False  # Flag to track if a trade was entered during the New York session

    # Initialize instances of helper classes
    s = osession.Session()  # Session management
    p = oprice.Price()  # Price-related operations
    t = otrade.Trade()  # Trade execution
    c = ocandles.Candles()  # Candle-related operations
    b = obuy.Buy()  # Buy-related logic
    s1 = osell.Sell()  # Sell-related logic

    # Initialize MetaTrader5
    if not mt5.initialize():
        print("Initialize failed")
        mt5.shutdown()

    execution_time = datetime.datetime.now().time().minute  # Current minute for execution timing
    session = s.get_trading_session()  # Get the current trading session

    # Method to start the trading strategy
    def start(self, bot, message):
        # Loop until a trade is entered in either the London or New York session
        while not self.entered_ny and not self.entered_london:
            print("**Current Session**: {}".format(self.session))
            if self.session == "":  # If no session is active, exit
                return True

            # Handle Tokyo session (wait for the next session)
            while self.session == "Tokyo Session":
                next_session_time = datetime.datetime.now().replace(hour=8, minute=2, second=0)  # Next session start time
                now = datetime.datetime.now()  # Current time
                a = next_session_time - now  # Time difference until the next session
                bot.reply_to(message, "Actual session is Tokyo, sleeping for " + str(
                    a.total_seconds()) + " seconds until opening next session")
                time.sleep(a.total_seconds())  # Sleep until the next session starts
                self.session = self.s.get_trading_session()  # Update the current session

            bot.reply_to(message, "Actual session: " + self.session)  # Notify the current session

            # Get the high and low prices for EURUSD and GBPUSD from the previous session
            highest_price_eu, lowest_price_eu = self.s.get_high_low_old_session(self.session, "EURUSD", self.timeframe)
            highest_price_gu, lowest_price_gu = self.s.get_high_low_old_session(self.session, "GBPUSD", self.timeframe)

            is_entered = False  # Flag to track if a trade has been entered
            bot.reply_to(message, "Checking for liquidity sweep")  # Notify liquidity sweep check

            z = ""  # Variable to store the symbol with liquidity sweep
            liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = False, False, False, False  # Liquidity flags

            # Check for liquidity sweep in the current session
            if self.session == self.s.get_trading_session():
                if self.execution_time % 5 != 0:  # Check if the current minute is not a multiple of 5
                    bot.reply_to(message, "Checking passed candles to see if the price got swept or not")
                    # Check for late entry in EURUSD and GBPUSD
                    late_a_eu, self.last_candle_eu = self.p.late_enter(highest_price_eu, lowest_price_eu,
                                                                       self.s.candles_actual_session(mt5.TIMEFRAME_M1,
                                                                                                     self.session,
                                                                                                     "EURUSD"))
                    time.sleep(3)
                    late_a_gu, self.last_candle_gu = self.p.late_enter(highest_price_gu, lowest_price_gu,
                                                                       self.s.candles_actual_session(mt5.TIMEFRAME_M1,
                                                                                                     self.session,
                                                                                                     "GBPUSD"))

                    # Determine which symbol had a liquidity sweep
                    if late_a_eu == late_a_gu and late_a_eu:
                        if self.last_candle_eu[0] > self.last_candle_gu[0]:
                            self.last_candle = self.last_candle_gu
                            self.late_a = late_a_gu
                            z = "gu"
                        else:
                            self.last_candle = self.last_candle_eu
                            self.late_a = late_a_eu
                            z = "eu"
                    elif late_a_eu and not late_a_gu:
                        self.last_candle = self.last_candle_eu
                        self.late_a = late_a_eu
                        z = "eu"
                    elif late_a_gu and not late_a_eu:
                        self.last_candle = self.last_candle_gu
                        self.late_a = late_a_gu
                        z = "gu"
                    print(z)

                    # Set liquidity flags based on the symbol and sweep direction
                    if z == "eu":
                        if self.late_a == "false":
                            liquid_low_eu = True
                            liquid_high_eu = False
                            bot.reply_to(message, "Liquidity is swept from lowest in EURUSD, searching for buy")
                        elif self.late_a == "true":
                            liquid_high_eu = True
                            liquid_low_eu = False
                            bot.reply_to(message, "Liquidity is swept from highest in EURUSD, searching for sell")
                    elif z == "gu":
                        if self.late_a == "false":
                            liquid_low_gu = True
                            liquid_high_gu = False
                            bot.reply_to(message, "Liquidity is swept from lowest in GBPUSD, searching for buy")
                        elif self.late_a == "true":
                            liquid_high_gu = True
                            liquid_low_gu = False
                            bot.reply_to(message, "Liquidity is swept from highest in GBPUSD, searching for sell")
                    else:
                        # If no late entry, check for liquidity directly
                        liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = self.p.get_liquidity(
                            highest_price_eu, lowest_price_eu, highest_price_gu, lowest_price_gu)
                        print("im here1")
                else:
                    # If the current minute is a multiple of 5, check for liquidity directly
                    liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = self.p.get_liquidity(
                        highest_price_eu,
                        lowest_price_eu,
                        highest_price_gu,
                        lowest_price_gu)
                    print("im here2")
                a = 0

            # Determine the symbol and liquidity direction for trading
            liquid_low = False
            liquid_high = False
            symbol = ""
            if liquid_low_gu:
                liquid_low = True
                symbol = "GBPUSD"
                bot.reply_to(message, "Liquidity is swept from lowest in GBPUSD, searching for buy")
            if liquid_high_gu:
                liquid_high = True
                symbol = "GBPUSD"
                bot.reply_to(message, "Liquidity is swept from highest in GBPUSD, searching for sell")
            if liquid_low_eu:
                liquid_low = True
                symbol = "EURUSD"
                bot.reply_to(message, "Liquidity is swept from lowest in EURUSD, searching for buy")
            if liquid_high_eu:
                liquid_high = True
                symbol = "EURUSD"
                bot.reply_to(message, "Liquidity is swept from highest in EURUSD, searching for sell")

            # Buy phase: Enter a buy trade if liquidity is swept from the low
            while liquid_low:
                if not self.last_candle:
                    structure = self.c.get_bullish_candle(self.c.get_last_10_closed_candles1(symbol, self.timeframe))
                else:
                    structure = self.last_candle
                if self.b.buy_structure(structure, symbol, self.timeframe, self.volume, bot, message):
                    if self.session == "London Session":
                        self.entered_london = True
                        self.buy = True
                    elif self.session == "New York Session":
                        self.entered_ny = True
                        self.buy = True
                    break

            # Sell phase: Enter a sell trade if liquidity is swept from the high
            while liquid_high:
                if not self.last_candle:
                    structure = self.c.get_bearish_candle(self.c.get_last_10_closed_candles1(symbol, self.timeframe))
                else:
                    structure = self.last_candle
                if self.s1.sell_structure(structure, symbol, self.timeframe, self.volume, bot, message):
                    if self.session == "London Session":
                        self.entered_london = True
                        self.sell = True
                    elif self.session == "New York Session":
                        self.entered_ny = True
                        self.sell = True
                    break

            # Check for a second entry opportunity
            is_entered_second = False
            bot.reply_to(message,
                         "Now checking for second entry. It'll do it automatically once the price gets into half SL.")
            if self.buy:
                tick = mt5.symbol_info_tick(symbol)
                while self.tp >= tick.bid or self.tp >= tick.ask or self.sl <= tick.bid or self.sl <= tick.ask:
                    e = self.b.second_entry(self.session, symbol, self.volume, bot, message)
                    if e:
                        bot.reply_to(message, "The bot has entered second entry")
                        break
                    else:
                        bot.reply_to(message, "There is no second entry, starting to check for ", self.session)
                        break
            if self.sell:
                tick = mt5.symbol_info_tick(symbol)
                while self.tp >= tick.bid or self.tp >= tick.ask or self.sl >= tick.bid or self.sl >= tick.ask:
                    e = self.s1.second_entry(self.session, symbol, self.volume, bot, message)
                    if e:
                        bot.reply_to(message, "The bot has entered second entry")
                        break
                    else:
                        bot.reply_to(message, "There is no second entry, starting to check for ", self.session)
                        break

            time.sleep(10)  # Wait for 10 seconds before the next iteration

            # Sleep until the next session if the current session is London
            if self.session == "London Session":
                bot.reply_to(message, "Enjoy! Now the bot is going to sleep until the NY session.")
                next_session_time = datetime.datetime.now().replace(hour=12, minute=5, second=0)
                now = datetime.datetime.now()
                a = next_session_time - now
                time.sleep(a.total_seconds())
            else:
                return True