import datetime
import MetaTrader5 as mt5
import time
import ozo.session as osession
import ozo.price as oprice
import ozo.trade as otrade
import ozo.candles as ocandles
import ozo.buy_structure as obuy
import ozo.sell_structure as osell


class Judaswing:
    buy = False
    sell = False
    tp = 0
    sl = 0
    entry = 0
    volume = 0.1
    last_candle = []
    last_candle_eu = []
    last_candle_gu = []
    old_last_bearish_candle = []
    old_last_bullish_candle = []
    structure = []
    last_closed_candle = []
    today = datetime.datetime.today()
    timeframe = mt5.TIMEFRAME_M5
    late_a = ""
    entered_london = False
    entered_ny = False
    s = osession.Session()
    p = oprice.Price()
    t = otrade.Trade()
    c = ocandles.Candles()
    b = obuy.Buy()
    s1 = osell.Sell()
    if not mt5.initialize():
        print("Initialize failed")
        mt5.shutdown()

    execution_time = datetime.datetime.now().time().minute
    # getting actual session
    session = s.get_trading_session()

    def start(self, bot, message):
        while not self.entered_ny and not self.entered_london:
            print("**Current Session**: {}".format(self.session))
            if self.session == "":
                return True
            while self.session == "Tokyo Session":
                next_session_time = datetime.datetime.now().replace(hour=8, minute=2, second=0)
                now = datetime.datetime.now()
                a = next_session_time - now
                bot.reply_to(message, "Actual session is tokyo, sleeping for " + str(
                    a.total_seconds()) + " seconds until opening next session")
                time.sleep(a.total_seconds())
                self.session = self.s.get_trading_session()
            bot.reply_to(message, "Actual session: " + self.session)
            highest_price_eu, lowest_price_eu = self.s.get_high_low_old_session(self.session, "EURUSD", self.timeframe)
            highest_price_gu, lowest_price_gu = self.s.get_high_low_old_session(self.session, "GBPUSD", self.timeframe)
            is_entered = False
            bot.reply_to(message, "Checking for liquidity Sweep")
            z = ""
            liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = False, False, False, False
            if self.session == self.s.get_trading_session():
                if self.execution_time % 5 != 0:
                    bot.reply_to(message, "checking passed candles if the price got swept or not")
                    # searching in both eu and gu
                    late_a_eu, self.last_candle_eu = self.p.late_enter(highest_price_eu, lowest_price_eu,
                                                                       self.s.candles_actual_session(mt5.TIMEFRAME_M1,
                                                                                                     self.session,
                                                                                                     "EURUSD"))
                    time.sleep(3)
                    late_a_gu, self.last_candle_gu = self.p.late_enter(highest_price_gu, lowest_price_gu,
                                                                       self.s.candles_actual_session(mt5.TIMEFRAME_M1,
                                                                                                     self.session,
                                                                                                     "GBPUSD"))
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
                        liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = self.p.get_liquidity(
                            highest_price_eu, lowest_price_eu, highest_price_gu, lowest_price_gu)
                        print("im here1")
                else:
                    liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = self.p.get_liquidity(
                        highest_price_eu,
                        lowest_price_eu,
                        highest_price_gu,
                        lowest_price_gu)
                    print("im here2")
                a = 0
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

            # buy phase
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

            # sell phase
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

            is_entered_second = False
            bot.reply_to(message,
                         "now checking for second entry, it'l do it automatically once the price gets into half sl")
            if self.buy:
                tick = mt5.symbol_info_tick(symbol)
                while self.tp >= tick.bid or self.tp >= tick.ask or self.sl <= tick.bid or self.sl <= tick.ask:
                    e = self.b.second_entry(self.session, symbol, self.volume, bot, message)
                    if e:
                        bot.reply_to(message, "The bot has entered second entry")
                        break
                    else:
                        bot.reply_to(message, "there is no second entry, starting to check for ", self.session)
                        break
            if self.sell:
                tick = mt5.symbol_info_tick(symbol)
                while self.tp >= tick.bid or self.tp >= tick.ask or self.sl >= tick.bid or self.sl >= tick.ask:
                    e = self.s1.second_entry(self.session, symbol, self.volume, bot, message)
                    if e:
                        bot.reply_to(message, "The bot has entered second entry")
                        break
                    else:
                        bot.reply_to(message, "there is no second entry, starting to check for ", self.session)
                        break
            time.sleep(10)
            if self.session == "London Session":
                bot.reply_to(message, "enjoy now the bot is going to sleep until NY session")
                next_session_time = datetime.datetime.now().replace(hour=12, minute=5, second=0)
                now = datetime.datetime.now()
                a = next_session_time - now
                time.sleep(a.total_seconds())
            else:
                return True
