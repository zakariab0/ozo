import time
import MetaTrader5 as mt5
class Price:

    #this function returns two variables a, b;
    # a: if it's true then lq sweep from the highest, if it's false then lq sweep from the lowest
    # b: the last structure either it was ls from highest or lowest
    @staticmethod
    def late_enter(highest, lowest, candles):
        print(candles[0])
        print("highes: ", highest)
        print("lowest: ", lowest)
        a = candles[0]
        b = candles[0]
        position_b = 0
        position_a = 0
        for i, c in enumerate(candles):
            if a != b:
                if highest < c[2] < a[2] and c[0] < a[0]:
                    a = c
                    position_a = i
                if b[3] < c[3] < lowest and c[0] < b[0]:
                    b = c
                    position_b = i
            else:
                if highest < c[2]:
                    a = c
                    position_a = i
                if lowest > c[3]:
                    b = c
                    position_b = i

        if a[2] > highest and b[3] < lowest:
            print("a")
            if a[0] < b[0]:
                print("b")
                print("liquidity sweep from highest")
                print("get last bearish candle before ls")
                position_a -= 1
                while position_a >= 0:
                    if candles[position_a][1] > candles[position_a][4]:
                        print("Bullish candle that did lq sweep from highest in function: ", a)
                        a = candles[position_a]
                        print("bearish candle before lq sweep: ", a)
                        return "true", a
                    else:
                        position_a -= 1
                return -1
            elif b[0] < a[0]:
                print("c")
                print("liquidity sweep from lowest")
                print("get last bullish candle before ls")
                position_b -= 1
                while position_b >= 0:
                    if candles[position_b][1] < candles[position_b][4]:
                        print("bearish candle that did lq sweep from highes in function: ", b)
                        b = candles[position_b]
                        print("Bullish candle before lq sweep: ", b)
                        return "false", b
                    else:
                        position_b -= 1
        elif a[2] > highest:
            print("liquidity sweep from highest")
            print("get last bearish candle before ls")
            position_a -= 1
            print("positiona1: ", position_a)
            while position_a >= 0:
                if candles[position_a][1] > candles[position_a][4]:
                    print("Bullish candle that did lq sweep from highes in function: ", a)
                    a = candles[position_a]
                    print("bearish candle before lq sweep: ", a)
                    return "true", a
                else:
                    position_a -= 1
        elif b[3] < lowest:
            print("e")
            print("b: ", b[3])
            print("lowest: ", lowest)
            print("liquidity sweep from lowest")
            print("get last bullish candle before ls")
            position_b -= 1
            while position_b >= 0:
                if candles[position_b][1] < candles[position_b][4]:
                    print("Bearish candle that did lq sweep from highes in function: ", b)
                    b = candles[position_b]
                    print("Bullish candle before lq sweep: ", b)
                    return "false", b
                else:
                    position_b -= 1
        else:
            return -1, ()


    @staticmethod
    def get_liquidity(highest_price_eu, lowest_price_eu, highest_price_gu, lowest_price_gu):
        liquid_low_eu, liquid_high_eu, liquid_low_gu, liquid_high_gu = False, False, False, False
        symbol_eu = "EURUSD"
        symbol_gu = "GBPUSD"
        while not liquid_low_eu and not liquid_high_eu and not liquid_low_gu and not liquid_high_gu:
            tick_eu = mt5.symbol_info_tick(symbol_eu)
            tick_gu = mt5.symbol_info_tick(symbol_gu)
            time.sleep(3)
            # Accessing the bid and ask prices from the tick data
            actual_bid_price_eu = tick_eu.bid
            actual_ask_price_eu = tick_eu.ask
            actual_bid_price_gu = tick_gu.bid
            actual_ask_price_gu = tick_gu.ask
            print("Bid eu: ", actual_bid_price_eu, ", Ask eu: ", actual_ask_price_eu)
            print("Bid gu: ", actual_bid_price_gu, ", Ask gu: ", actual_ask_price_gu)
            # here we're waiting for liquidity sweep
            if actual_bid_price_eu < lowest_price_eu:
                print("Liquidity is swept from lowest of EU, searching for buy3")
                return True, False, False, False
            elif actual_ask_price_eu > highest_price_eu:
                print("Liquidity is swept from highest of EU, searching for sell3")
                return False, True, False, False
            elif actual_bid_price_gu < lowest_price_gu:
                print("Liquidity is swept from lowest of GU, searching for buy3")
                return False, False, True, False

            elif actual_ask_price_gu > highest_price_gu:
                print("Liquidity is swept from highest of GU, searching for sell3")
                return False, False, False, True

