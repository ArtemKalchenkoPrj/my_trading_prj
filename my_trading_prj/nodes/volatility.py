import pandas as pd

from ta.volatility import BollingerBands, KeltnerChannel

from my_trading_prj.state import GraphState, IndicatorSignal
from my_trading_prj.nodes.trend import fetch_ohlcv

def compute_keltner(df: pd.DataFrame, window):
    kc = KeltnerChannel(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=window,
        window_atr=window,
        original_version=False
    )

    upper = kc.keltner_channel_hband()[-10:].values
    lower = kc.keltner_channel_lband()[-10:].values
    middle = kc.keltner_channel_mband()[-10:].values
    width = upper - lower

    return {'width': width, 'upper': upper, 'lower': lower, 'middle': middle}

def compute_bollinger(df: pd.DataFrame, window):

    bb = BollingerBands(
        close=df["close"],
        window=window
    )

    upper = bb.bollinger_hband()[-10:].values
    lower = bb.bollinger_lband()[-10:].values
    middle = bb.bollinger_mavg()[-10:].values
    width = bb.bollinger_wband()[-10:].values

    return {'width': width, 'upper': upper, 'lower': lower, 'middle': middle}

def calculate_volatility(state: GraphState):
    coin = state['coin']
    window = state['window']

    df = fetch_ohlcv(coin=coin)

    bollinger = compute_bollinger(df, window)
    keltner = compute_keltner(df, window)

    last_price = df['close'].iloc[-10:]

    bollinger_upper = IndicatorSignal(name='BollingerUpper',window=window, value=bollinger['upper'])
    bollinger_lower = IndicatorSignal(name='BollingerLower', window=window, value=bollinger['lower'])
    bollinger_middle = IndicatorSignal(name='BollingerMiddle', window=window, value=bollinger['middle'])
    bollinger_width = IndicatorSignal(name='BollingerWidth', window=window, value=bollinger['width'])

    keltner_upper = IndicatorSignal(name='KeltnerUpper',window=window, value=keltner['upper'])
    keltner_lower = IndicatorSignal(name='KeltnerLower', window=window, value=keltner['lower'])
    keltner_middle = IndicatorSignal(name='KeltnerMiddle', window=window, value=keltner['middle'])
    keltner_width = IndicatorSignal(name='KeltnerWidth', window=window, value=keltner['width'])

    last_price_indicator = IndicatorSignal(name='LastPrice', window=window, value=last_price)

    if indicators := state.get('indicators'):
        indicators.append(bollinger_upper)
        indicators.append(bollinger_lower)
        indicators.append(bollinger_middle)
        indicators.append(bollinger_width)

        indicators.append(keltner_upper)
        indicators.append(keltner_lower)
        indicators.append(keltner_middle)
        indicators.append(keltner_width)
    else:
        indicators = [bollinger_upper, bollinger_lower,bollinger_middle,bollinger_width,
                      keltner_upper, keltner_lower, keltner_middle, keltner_width]

    return {'indicators': indicators, 'last_price':last_price_indicator}


if __name__ == "__main__":
    df = fetch_ohlcv(coin='BTC-USD')
    res = compute_bollinger(df,10)
    print("")