import time
import MetaTrader5 as mt5
import ozo.candles as ocandles
import ozo.trade as otrades
import ozo.session as oSession


# def get_structure(last_ten_candles, last_closed_candle):
#     #A candle is defined by it's highest and lowest right,
#     # so if the last closed candle for example is still inside the structre it wont do anything
#     # if the last closed candle close upper than the highest so there we would count a new structure
#
class Buy:
    # buy phase:
    entry = 0
    tp = 0
    sl = 0
    c = ocandles.Candles()
    t = otrades.Trade()
    s = oSession.Session()
    def buy_structure(self, highest_last_bullish_candle, symbol, timeframe, volume, bot, message):
        bearish_count = 0
        entered = False
        highest_last_bullish_price = highest_last_bullish_candle[2]
        time.sleep(2)
        last_closed_candle = self.c.get_last_closed_candle(symbol, timeframe)[0]
        while not entered:
            changed = False
            a = self.c.get_last_closed_candle(symbol, timeframe)
            print(a)
            if a[0] != last_closed_candle:
                last_closed_candle = a[0]  # here function of retrieving last candle
                time.sleep(5)
                if last_closed_candle[4] > last_closed_candle[1] and last_closed_candle[4] > highest_last_bullish_price:
                    bot.reply_to(message, "breakout, entered")
                    tick = mt5.symbol_info_tick(symbol)
                    lowest_candle = self.c.get_lowest_low(self.c.get_last_10_closed_candles1(symbol, timeframe))
                    self.tp = tick.bid + (tick.bid - lowest_candle)
                    self.sl = lowest_candle
                    self.entry = tick.bid
                    msg = "symbol: " + str(symbol) + " volume: " + str(volume) +  " sl: " + str(self.sl) +  " tp: " + str(self.tp)
                    bot.reply_to(message, msg)
                    self.t.enter_buy_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                    return True
                elif last_closed_candle[4] < last_closed_candle[1]:
                    bearish_count += 1
                    str1 = "bearish count: " + str(bearish_count)
                    bot.reply_to(message, str1)
                    time.sleep(280)
                elif last_closed_candle[4] > last_closed_candle[1] and bearish_count >= 2:
                    while not changed:
                        new = self.c.get_last_closed_candle(symbol, timeframe)[0]
                        if new[1] > new[4]:
                            bot.reply_to(message, "new structure:")
                            bot.reply_to(message, "old: " + str(highest_last_bullish_candle))
                            bot.reply_to(message, "new: " + str(last_closed_candle))
                            highest_last_bullish_candle = last_closed_candle
                            highest_last_bullish_price = highest_last_bullish_candle[3]
                            bearish_count = 0
                            changed = True
                            time.sleep(280)
                        elif new[4] > highest_last_bullish_price:
                            bot.reply_to(message, "breakout, entered")
                            tick = mt5.symbol_info_tick(symbol)
                            lowest_candle = self.c.get_lowest_low(
                                self.c.get_last_10_closed_candles1(symbol, timeframe))
                            self.tp = tick.bid + (tick.bid - lowest_candle)
                            self.sl = lowest_candle
                            msg = "symbol: " + str(symbol) + " volume: " + str(volume) + " sl: " + str(
                                self.sl) + " tp: " + str(self.tp)
                            bot.reply_to(message, msg)
                            self.t.enter_buy_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                            return True
                        elif new[1] < new[4]:
                            last_closed_candle = new
                            bot.reply_to(message, "changed last bullish, waiting for breakout or new structure")
                            time.sleep(280)
                else:
                    bot.reply_to(message, "bullish, waiting for breakout")
                    time.sleep(280)
            else:
                time.sleep(10)

    def second_entry(self, session, symbol, volume, bot, message):

        while self.s.get_trading_session() == session:
            tick = mt5.symbol_info_tick(symbol)
            if tick.bid < self.entry or tick.ask < self.entry:
                if (self.sl + ((self.entry - self.sl) / 2)) > tick.bid or (self.sl + ((self.entry - self.sl) / 2)) > tick.ask:
                    self.t.enter_buy_trade(symbol, volume=volume, sl=self.sl, tp=self.tp)
                    bot.reply_to(message, "the bot has entered the second entry")
                    return True
        return False
