import time
import pyupbit

access = "access"
secret = "secret"
coin = "KRW-ETH"
# buy_signal = False
# sell_signal = False

upbit = pyupbit.Upbit(access, secret) # 로그인
print("Trading start")

def calculate_indicator(df):
    df['original'] = (((df['high'] - df['low'])/df['volume'])/df['close']).rolling(window=10).mean()
    low = df['original'].rolling(window=20).min()
    high = df['original'].rolling(window=20).max()
    df['indicator'] = ((high - df['original']) / (high - low)) * 100
    df['indicator'] = df['indicator'].rolling(window=10).mean()
    return df['indicator'].iloc[-1]  # return the latest indicator

def buy(coin):
    krw = upbit.get_balance("KRW")
    if krw > 5000:
        upbit.buy_market_order(coin, krw * 0.9995)
    return

def sell(coin):
    coin_amount = upbit.get_balance(coin[4:]) # 수정: coin에서 'KRW-' 제거
    if coin_amount is not None: # 보유량 확인
        upbit.sell_market_order(coin, coin_amount)
    return

while True:
    df = pyupbit.get_ohlcv(ticker=coin, interval="minute240", count=100)
    now_indicator = calculate_indicator(df)

    if now_indicator <= 5:  # indicator가 10 이하일 때 매수
        buy(coin)
    elif now_indicator >= 95:  # indicator가 90 이상일 때 매도
        sell(coin)

    time.sleep(0.5)

# while True:
#     df = pyupbit.get_ohlcv(ticker=coin, interval="minute60", count=100) 
#     now_indicator = calculate_indicator(df)

#     if now_indicator < 10:  
#         buy_signal = True
#     elif now_indicator > 10 and buy_signal:  # if not bought and buy_signal is true
#         buy(coin)
#         buy_signal = False

#     if now_indicator > 90:  
#         sell_signal = True
#     elif now_indicator < 90 and sell_signal:  # if bought and sell_signal is true
#         sell(coin)
#         sell_signal = False

#     time.sleep(0.5)
