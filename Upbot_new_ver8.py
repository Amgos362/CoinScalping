import time
import pyupbit
import requests

TARGET_URL = 'url'
access = "access"
secret = "secret"
MESSAGE_TOKEN = "token"

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
        coin_amount = upbit.get_balance(coin[4:])
        buy_message = f"Bought {coin}: {coin_amount} amount"
        send_message(buy_message, MESSAGE_TOKEN) # 이 부분 추가
    return

def sell(coin):
    coin_amount_before = upbit.get_balance(coin[4:])
    coin_value_before = coin_amount_before * pyupbit.get_current_price(coin)
    upbit.sell_market_order(coin, coin_amount_before)
    krw_after = upbit.get_balance("KRW")
    profit_loss = krw_after - coin_value_before
    if coin_value_before == 0:
        profit_loss_percent = 0  # 또는 적절한 다른 값을 할당
    else:
        profit_loss_percent = (profit_loss / coin_value_before) * 100
    sell_message = f"Sold {coin}: {coin_amount_before} amount, Profit/Loss: {profit_loss} KRW ({profit_loss_percent}%)"
    send_message(sell_message, MESSAGE_TOKEN) # 이 부분 추가
    return

def send_message(message, token=None):
    """LINE Notify를 사용한 메세지 보내기"""
    try:
        response = requests.post(
            TARGET_URL,
            headers={
                'Authorization': 'Bearer ' + token
            },
            data={
                'message': message
            }
        )
        status = response.json()['status']
        # 전송 실패 체크
        if status != 200:
            # 에러 발생 시에만 로깅
            raise Exception('Fail need to check. Status is %s' % status)

    except Exception as e:
        raise Exception(e)


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

