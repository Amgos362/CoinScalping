import time
import pyupbit
import pandas as pd

access = "access"
secret = "secret"
coins = ["KRW-ETH", "KRW-ETC"]
lower30 = []
higher65 = []

for i in range(len(coins)):
    lower30.append(False)
    higher65.append(False)

upbit = pyupbit.Upbit(access, secret) # 로그인
print("scalping start")

def rsi(ohlc: pd.DataFrame, period: int = 14):
    delta = ohlc['close'].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    au = ups.ewm(com = period-1, min_periods = period).mean()
    ad = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = au/ad
    RSI = pd.Series(100 - (100/(1+RS)), name = "RSI(14)")
    return RSI


def buy(coin):
    krw = upbit.get_balance("KRW")
    coin_bought = len(upbit.get_balances())
    if krw > 5000:
            upbit.buy_market_order(coin, krw * 0.9995 / (len(coins) - coin_bought + 1))
    return

def sell(coin):
    scam = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)
    total = scam * cur_price
    if total > 5000:
        upbit.sell_market_order(coin, scam)
    return

def get_ma_min30(ticker, n):
    df = pyupbit.get_ohlcv(ticker=ticker, interval="minute30", count=n)
    ma = df['close'].rolling(n).mean().iloc[-1]
    return ma

def get_ma_day(ticker):
    df = pyupbit.get_ohlcv(ticker=ticker, interval="day", count=10)
    ma = df['close'].rolling(10).mean().iloc[-1]
    return ma

while True:


    for i in range(len(coins)):
        df = pyupbit.get_ohlcv(ticker=coins[i], interval="minute1")    # RSI(N) 계산 / 데이터 200개 조회
        now_rsi = rsi(df, 14).iloc[-1]
        cur_price = pyupbit.get_current_price(coins[i])

        if get_ma_min30(coins[i], 60) < cur_price:
            if now_rsi < 28:
                lower30[i] = True
            elif now_rsi > 33 and lower30[i] == True:
                buy(coins[i])
                lower30[i] = False
            elif now_rsi > 72:
                higher65[i] = True
            elif now_rsi < 66 and higher65[i] == True:
                sell(coins[i])
                higher65[i] = False

        else:
            if now_rsi < 23:
                lower30[i] = True
            elif now_rsi > 29 and lower30[i] == True:
                buy(coins[i])
                lower30[i] = False
            elif now_rsi > 67:
                higher65[i] = True
            elif now_rsi < 62 and higher65[i] == True:
                sell(coins[i])
                higher65[i] = False

        if upbit.get_avg_buy_price(coins[i]) > 0:
            if cur_price / upbit.get_avg_buy_price(coins[i]) < 0.995:
                sell(coins[i])

    time.sleep(0.5)


