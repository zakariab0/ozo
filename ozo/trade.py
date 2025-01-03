import MetaTrader5 as mt5
import datetime
import time

# Class for handling trade execution
class Trade:

    # Static method to enter a buy trade
    @staticmethod
    def enter_buy_trade(symbol, volume, sl, tp):
        """
        Executes a buy trade for the specified symbol.
        Args:
            symbol (str): The trading symbol (e.g., "EURUSD").
            volume (float): The trade volume.
            sl (float): The stop-loss level.
            tp (float): The take-profit level.
        """
        # Prepare the trade request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,  # Action to execute the trade
            "symbol": symbol,  # Trading symbol
            "volume": volume,  # Trade volume
            "type": mt5.ORDER_TYPE_BUY,  # Buy order type
            "price": mt5.symbol_info_tick(symbol).ask,  # Current ask price
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Buy trade"  # Comment for the trade
        }
        # Send the trade request
        result = mt5.order_send(request)
        # Check if the trade was executed successfully
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to execute buy trade. Error: {result.comment}")
        else:
            print("Buy trade executed successfully.")

    # Static method to enter a buy limit trade
    @staticmethod
    def enter_buy_limit_trade(symbol, volume, sl, tp, price):
        """
        Places a buy limit order for the specified symbol.
        Args:
            symbol (str): The trading symbol (e.g., "EURUSD").
            volume (float): The trade volume.
            sl (float): The stop-loss level.
            tp (float): The take-profit level.
            price (float): The price at which the limit order will be triggered.
        """
        # Prepare the trade request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,  # Action to execute the trade
            "symbol": symbol,  # Trading symbol
            "volume": volume,  # Trade volume
            "type": mt5.ORDER_TYPE_BUY,  # Buy order type
            "price": price,  # Limit price
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Buy limit trade"  # Comment for the trade
        }
        # Send the trade request
        result = mt5.order_send(request)
        # Check if the trade was executed successfully
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to set buy limit trade. Error: {result.comment}")
        else:
            print("Buy limit trade executed successfully.")

    # Static method to enter a sell trade
    @staticmethod
    def enter_sell_trade(symbol, volume, sl, tp):
        """
        Executes a sell trade for the specified symbol.
        Args:
            symbol (str): The trading symbol (e.g., "EURUSD").
            volume (float): The trade volume.
            sl (float): The stop-loss level.
            tp (float): The take-profit level.
        """
        # Prepare the trade request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,  # Action to execute the trade
            "symbol": symbol,  # Trading symbol
            "volume": volume,  # Trade volume
            "type": mt5.ORDER_TYPE_SELL,  # Sell order type
            "price": mt5.symbol_info_tick(symbol).bid,  # Current bid price
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Sell trade"  # Comment for the trade
        }
        # Send the trade request
        result = mt5.order_send(request)
        # Check if the trade was executed successfully
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to execute sell trade. Error: {result.comment}")
        else:
            print("Sell trade executed successfully.")

    # Static method to enter a sell limit trade
    @staticmethod
    def enter_sell_limit_trade(symbol, volume, sl, tp, price):
        """
        Places a sell limit order for the specified symbol.
        Args:
            symbol (str): The trading symbol (e.g., "EURUSD").
            volume (float): The trade volume.
            sl (float): The stop-loss level.
            tp (float): The take-profit level.
            price (float): The price at which the limit order will be triggered.
        """
        # Prepare the trade request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,  # Action to execute the trade
            "symbol": symbol,  # Trading symbol
            "volume": volume,  # Trade volume
            "type": mt5.ORDER_TYPE_SELL,  # Sell order type
            "price": price,  # Limit price
            "sl": sl,  # Stop Loss level
            "tp": tp,  # Take Profit level
            "magic": 234000,  # Magic number to identify the trade
            "comment": "Sell limit trade"  # Comment for the trade
        }
        # Send the trade request
        result = mt5.order_send(request)
        # Check if the trade was executed successfully
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to set sell limit trade. Error: {result.comment}")
        else:
            print("Sell limit trade executed successfully.")

    # Static method to get liquidity sweep (placeholder)
    @staticmethod
    def get_lq_sweep(session):
        """
        Placeholder method for liquidity sweep detection.
        Args:
            session (str): The trading session.
        Returns:
            None
        """
        return None