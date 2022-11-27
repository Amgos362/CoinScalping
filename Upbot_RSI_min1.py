import time
import pyupbit
import pandas as pd

access = "access"
secret = "secret"
coinlist = ["KRW-BTC", "KRW-ETH", "KRW-ETC"]
lower30 = []
higher65 = []

for i in range(len(coinlist)):
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

def get_balance(ticker):
    balances = upbit.get_balances() #잔고 조회
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def buy(coin):
    krw = get_balance("KRW")
    if krw > 5000:
        upbit.buy_market_order(coin, krw * 0.9995)
    return

def sell(coin):
    scam = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)
    total = scam * cur_price
    if total > 5000:
        upbit.sell_market_order(coin, scam * 0.9995)
    return



while True:
    for i in range(len(coinlist)):
        df = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute1")    # RSI(N) 계산 / 데이터 200개 조회
        now_rsi = rsi(df, 14).iloc[-1]
 
        if now_rsi < 28:
            lower30[i] = True
        elif now_rsi > 33 and lower30[i] == True:
            buy(coinlist[i])
            lower30[i] = False
        elif now_rsi > 68:
            higher65[i] = True
        elif now_rsi < 62 and higher65[i] == True:
            sell(coinlist[i])
            higher65[i] = False
    
    time.sleep(0.5)



