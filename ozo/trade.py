import MetaTrader5 as mt5
import datetime
import time
class Trade:

    @staticmethod
    def enter_buy_trade(symbol, volume, sl, tp):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Buy trade"  # Comment for the trade
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to execute buy trade. Error: {result.comment}")
        else:
            print("Buy trade executed successfully.")

    @staticmethod
    def enter_buy_limit_trade(symbol, volume, sl, tp, price):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Buy limit trade"  # Comment for the trade
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to set buy limit trade. Error: {result.comment}")
        else:
            print("Buy trade executed successfully.")


    @staticmethod
    def enter_sell_trade(symbol, volume, sl, tp):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,  # Use bid price for sell trade
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Sell trade"  # Comment for the trade
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to execute sell trade. Error: {result.comment}")
        else:
            print("Sell trade executed successfully.")

    @staticmethod
    def enter_sell_limit_trade(symbol, volume, sl, tp, price):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,  # Use bid price for sell trade
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Sell limit trade"  # Comment for the trade
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to set sell trade. Error: {result.comment}")
        else:
            print("Sell trade executed successfully.")


    @staticmethod
    def get_lq_sweep(session):
        return None
