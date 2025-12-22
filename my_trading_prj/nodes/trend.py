import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from ta.trend import EMAIndicator, SMAIndicator

from my_trading_prj.state import GraphState, IndicatorSignal


def fetch_ohlcv(
    coin: str,
) -> pd.DataFrame:
    """
    symbol: 'BTC-USD', 'ETH-USD', 'AAPL'
    start/end: 'YYYY-MM-DD'
    interval: 1m, 5m, 15m, 1h, 1d
    """
    end = datetime.now()
    start = end - timedelta(hours=50)
    df = yf.download(
        tickers=coin,
        start=start,
        end=end,
        interval="1h",
        progress=False,
        auto_adjust=False
    )

    if df.empty:
        raise ValueError("No data returned from Yahoo Finance")

    df.reset_index(inplace=True)
    df.columns = [c.lower() for c,_ in df.columns]
    return df

def calculate_trend(state: GraphState):
    coin = state['coin']
    window = state['next_indicator']['window']

    df = fetch_ohlcv(coin=coin)

    ema = EMAIndicator(close=df["close"], window=window).ema_indicator().iloc[-10:].values
    sma = SMAIndicator(close=df["close"], window=window).sma_indicator().iloc[-10:].values
    last_price = df['close'].iloc[-10:]


    ema_indicator = IndicatorSignal(name='ExponentialMovingAverage',window=window, value=ema)
    sma_indicator = IndicatorSignal(name='SimpleMovingAverage', window=window, value=sma)
    last_price_indicator = IndicatorSignal(name='LastPrice', window=window, value=last_price)

    if indicators := state.get('indicators'):
        indicators.append(ema_indicator)
        indicators.append(sma_indicator)
    else:
        indicators = [ema_indicator, sma_indicator]

    return {'indicators': indicators, 'last_price':last_price_indicator}


if __name__ == "__main__":
    calculate_trend({'coin':'BTC-USD','timeframe':1, 'indicators':[], 'window':5})