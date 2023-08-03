import time
import pyupbit

access = "access"
secret = "secret"

upbit = pyupbit.Upbit(access, secret)  # 로그인
print("Trading start")

coins = ["KRW-BTC", "KRW-ETH"]
intervals = ["minute60", "minute240"]

def calculate_indicator(df):
    df['original'] = (((df['high'] - df['low']) / df['volume']) / df['close']).rolling(window=10).mean()
    low = df['original'].rolling(window=20).min()
    high = df['original'].rolling(window=20).max()
    df['indicator'] = ((high - df['original']) / (high - low)) * 100
    df['indicator'] = df['indicator'].rolling(window=10).mean()
    return df['indicator'].iloc[-1]  # return the latest indicator

def buy(coin, portion):
    krw = upbit.get_balance("KRW")
    if krw > 5000:
        upbit.buy_market_order(coin, krw * 0.9995 * portion)
    return

def sell(coin):
    coin_amount = upbit.get_balance(coin[4:])  # 수정: coin에서 'KRW-' 제거
    if coin_amount is not None:  # 보유량 확인
        upbit.sell_market_order(coin, coin_amount)
    return

while True:
    for i, coin in enumerate(coins):
        df = pyupbit.get_ohlcv(ticker=coin, interval=intervals[i])
        now_indicator = calculate_indicator(df)

        if now_indicator <= 10:  # indicator가 10 이하일 때 매수
            portion = 1/3 if coin == "KRW-BTC" else 2/3
            buy(coin, portion)
        elif now_indicator >= 90:  # indicator가 90 이상일 때 매도
            sell(coin)

        time.sleep(0.5)
