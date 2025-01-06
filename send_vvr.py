import time
import pyupbit
import requests

TARGET_URL = 'https://notify-api.line.me/api/notify'
TOKEN = "token"  # TOKEN 값을 여기에 넣으세요.

coins = ["KRW-CHZ", "KRW-KNC", "KRW-GRS", "KRW-HIVE"]
intervals = ["minute60", "minute60", "minute240", "minute240"]


def send_line_notification(message):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"message": message}
    response = requests.post(TARGET_URL, headers=headers, data=data)


def calculate_vvr(coin, interval):
    try:
        df = pyupbit.get_ohlcv(ticker=coin, interval=interval, count=100)

        df['original'] = (((df['high'] - df['low']) / df['volume']) / df['close']).rolling(window=10).mean()
        low = df['original'].rolling(window=20).min()
        high = df['original'].rolling(window=20).max()
        df['indicator'] = ((high - df['original']) / (high - low)) * 100
        df['indicator'] = df['indicator'].rolling(window=10).mean()

        df = df.dropna()
        vvr = df['indicator'][-1]
        vvr = vvr.round(1)

        return vvr
    except Exception as e:
        send_line_notification(f"Error calculating VVR for {coin} on {interval}: {str(e)}")
        return None


while True:
    for i, coin in enumerate(coins):
            vvr = calculate_vvr(coin, intervals[i])
            if vvr is not None:
                send_line_notification(f"VVR for {coin} : {vvr}")
    time.sleep(3600)  # 1시간마다 반복
