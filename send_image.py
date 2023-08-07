import time
import pyupbit
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os

TARGET_URL = 'url'
MESSAGE_TOKEN = "token"

coins = ["KRW-BTC", "KRW-ETH"]
intervals = ["minute60", "minute240"]

def show_indicator():
    image_paths_with_coin = []
    coins = ["KRW-BTC", "KRW-ETH"]
    intervals = ["minute60", "minute240"]
    for i in range(len(coins)):

        output_dir = "/home/ubuntu/graphs/"
        os.makedirs(output_dir, exist_ok=True)  # 디렉토리가 없으면 생성

        df = pyupbit.get_ohlcv(ticker=coins[i], interval=intervals[i], count=1000)

        df['original'] = (((df['high'] - df['low']) / df['volume']) / df['close']).rolling(window=10).mean()
        low = df['original'].rolling(window=20).min()
        high = df['original'].rolling(window=20).max()
        df['indicator'] = ((high - df['original']) / (high - low)) * 100
        df['indicator'] = df['indicator'].rolling(window=10).mean()

        df = df.dropna()

        fig, ax1 = plt.subplots(figsize=(20, 5))

        # indicator 그래프 그리기
        ax1.plot(df.index, df['indicator'] * 10000, color='tab:blue')
        ax1.set_ylabel('Indicator', color='tab:blue')  # y축 레이블 설정
        ax1.tick_params(axis='y', labelcolor='tab:blue')  # y축 레이블 색상 설정
        ax1.axhline(y=100000, color='black', linestyle='--')  # indicator 10 위치에 선 추가
        ax1.axhline(y=900000, color='black', linestyle='--')  # indicator 90 위치에 선 추가

        ax2 = ax1.twinx()  # x축을 공유하는 두번째 축 생성

        # close 그래프 그리기
        ax2.plot(df.index, df['close'], color='tab:green')
        ax2.set_ylabel('Close', color='tab:green')  # y축 레이블 설정
        ax2.tick_params(axis='y', labelcolor='tab:green')  # y축 레이블 색상 설정

        red_marker = False
        blue_marker = False
        for index in range(len(df.index) - 1):
            if df['indicator'][index] > 10 and df['indicator'][index + 1] < 10 and red_marker == False:
                ax2.plot(df.index[index + 1], df['close'][index + 1], 'r^')
                red_marker = True
                blue_marker = False
            if df['indicator'][index] < 90 and df['indicator'][index + 1] > 90 and blue_marker == False:
                ax2.plot(df.index[index + 1], df['close'][index + 1], 'bv')
                blue_marker = True
                red_marker = False

        # ax3 = ax1.twinx()  # x축을 공유하는 두번째 축 생성

        fig.tight_layout()  # 그래프의 레이아웃을 조정
        VVR = df['indicator'][-1].round(1)
        ax1.text(df.index[-1], df['indicator'][-1] * 10000, f"VVR = {VVR}", color='blue')

        image_path = f"{coins[i]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        plt.savefig(image_path)
        image_paths_with_coin.append((image_path, coins[i]))

    plt.close()  # 창을 닫지 않으면 리소스가 소비될 수 있음
    return image_paths_with_coin

def send_image(image_path, coin, token=None):
    """LINE Notify를 사용한 이미지 전송"""
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                TARGET_URL,
                headers={
                    'Authorization': 'Bearer ' + token
                },
                files={
                    'imageFile': image_file
                },
                data={
                    'message': f'{coin[4:]} Graph'
                }
            )
        status = response.json()['status']
        if status != 200:
            raise Exception('Fail need to check. Status is %s' % status)

    except Exception as e:
        raise Exception(e)



last_sent_time = None

while True:
    now = datetime.now()
    if last_sent_time is None or (now - last_sent_time).total_seconds() >= 4 * 60 * 60:
        image_paths_with_coin = show_indicator()
        for image_path, coin in image_paths_with_coin:
            send_image(image_path, coin, MESSAGE_TOKEN)

        last_sent_time = now

    time.sleep(1)


