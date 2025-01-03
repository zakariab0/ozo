Here’s a comprehensive `README.md` file for your Python trading library. It explains the purpose, functionality, and usage of each module and class in your project.

---

# Python Trading Automation Library

This Python library is designed to automate trading strategies using MetaTrader 5 (MT5). It provides tools for analyzing market data, executing trades, and managing trading sessions. The library is modular, making it easy to extend and customize for different trading strategies.

---

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Session Management](#session-management)
   - [Candle Analysis](#candle-analysis)
   - [Trade Execution](#trade-execution)
   - [Price Analysis](#price-analysis)
   - [News and Liquidity Analysis](#news-and-liquidity-analysis)
4. [Modules Overview](#modules-overview)
5. [Example Workflow](#example-workflow)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features
- **Session Management**: Automatically detect and manage trading sessions (Tokyo, London, New York).
- **Candle Analysis**: Fetch and analyze candle data to identify trends, structures, and breakouts.
- **Trade Execution**: Execute market and limit orders for buy and sell trades.
- **Price Analysis**: Detect liquidity sweeps and high/low price levels.
- **News Analysis**: Check for high-impact news events and bank holidays.

---

## Installation

1. **Install MetaTrader 5**:
   - Download and install MT5 from the official website: [MetaTrader 5](https://www.metatrader5.com/).

2. **Install Required Python Packages**:
   ```bash
   pip install MetaTrader5 pandas beautifulsoup4 selenium
   ```

3. **Clone the Repository**:
   ```bash
   git clone https://github.com/zakariab0/ozo.git
   cd ozo
   ```

4. **Initialize MetaTrader 5**:
   - Ensure MT5 is running and logged into your trading account.
   - Use the `mt5.initialize()` function in your Python script to connect to MT5.

---

## Usage

### Session Management
The `Session` class manages trading sessions and provides methods to:
- Detect the current trading session (Tokyo, London, New York).
- Fetch high and low prices for previous sessions.
- Retrieve candle data for the current session.

```python
from ozo.session import Session

session = Session()
current_session = session.get_trading_session()
print("Current Session:", current_session)

# Get high and low prices of the previous session
high, low = session.get_high_low_old_session(current_session, "EURUSD", mt5.TIMEFRAME_M5)
print("High:", high, "Low:", low)
```

---

### Candle Analysis
The `Candles` class provides methods to:
- Fetch the last 10 closed candles.
- Identify bullish and bearish candles.
- Calculate the highest high and lowest low of a set of candles.

```python
from ozo.candles import Candles

candles = Candles()
last_10_candles = candles.get_last_10_closed_candles1("EURUSD", mt5.TIMEFRAME_M5)
bullish_candle = candles.get_bullish_candle(last_10_candles)
print("Bullish Candle:", bullish_candle)
```

---

### Trade Execution
The `Trade` class handles trade execution, including:
- Market buy and sell orders.
- Buy and sell limit orders.
- Setting stop-loss and take-profit levels.

```python
from ozo.trade import Trade

trade = Trade()
# Execute a buy trade
trade.enter_buy_trade("EURUSD", 0.1, 1.1000, 1.1100)

# Place a sell limit trade
trade.enter_sell_limit_trade("EURUSD", 0.1, 1.1100, 1.1000, 1.1050)
```

---

### Price Analysis
The `Price` class detects liquidity sweeps and determines the direction of price movements.

```python
from ozo.price import Price

price = Price()
direction, last_structure = price.late_enter(highest_price, lowest_price, candles)
print("Direction:", direction)
print("Last Structure:", last_structure)
```

---

### News and Liquidity Analysis
The `News` class checks for high-impact news events and bank holidays.

```python
from ozo.news import News

news = News()
result = news.check_forex_day("https://www.forexfactory.com/calendar")
print("Trading Day Quality:", result)
```

---

## Modules Overview

### `ozo.session`
- **Purpose**: Manage trading sessions and fetch session-specific data.
- **Key Methods**:
  - `get_trading_session()`: Detect the current trading session.
  - `get_high_low()`: Fetch high and low prices for a given range.
  - `candles_actual_session()`: Retrieve candles for the current session.

### `ozo.candles`
- **Purpose**: Analyze candle data to identify trends and structures.
- **Key Methods**:
  - `get_last_10_closed_candles1()`: Fetch the last 10 closed candles.
  - `get_bullish_candle()`: Identify the latest bullish candle.
  - `get_highest_high()`: Calculate the highest high in a set of candles.

### `ozo.trade`
- **Purpose**: Execute trades and manage orders.
- **Key Methods**:
  - `enter_buy_trade()`: Execute a market buy trade.
  - `enter_sell_limit_trade()`: Place a sell limit order.

### `ozo.price`
- **Purpose**: Analyze price action and detect liquidity sweeps.
- **Key Methods**:
  - `late_enter()`: Detect liquidity sweeps and determine direction.

### `ozo.news`
- **Purpose**: Check for high-impact news events and bank holidays.
- **Key Methods**:
  - `check_forex_day()`: Analyze the forex calendar for trading conditions.

---

## Example Workflow

1. **Initialize MT5**:
   ```python
   import MetaTrader5 as mt5
   mt5.initialize()
   ```

2. **Detect Trading Session**:
   ```python
   from ozo.session import Session
   session = Session()
   current_session = session.get_trading_session()
   ```

3. **Fetch Candle Data**:
   ```python
   from ozo.candles import Candles
   candles = Candles()
   last_10_candles = candles.get_last_10_closed_candles1("EURUSD", mt5.TIMEFRAME_M5)
   ```

4. **Execute a Trade**:
   ```python
   from ozo.trade import Trade
   trade = Trade()
   trade.enter_buy_trade("EURUSD", 0.1, 1.1000, 1.1100)
   ```

5. **Shutdown MT5**:
   ```python
   mt5.shutdown()
   ```

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contact me on mail: zakariabounouu@gmail.com . Let me know if you need further assistance! 🚀