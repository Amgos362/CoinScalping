import pyupbit
import matplotlib.pyplot as plt

coins = ["KRW-BTC", "KRW-ETH"]
intervals = ["minute60", "minute240"]
for i in range(len(coins)):

    df = pyupbit.get_ohlcv(ticker=coins[i], interval=intervals[i], count=1000)

    df['original'] = (((df['high'] - df['low'])/df['volume'])/df['close']).rolling(window=10).mean()
    low = df['original'].rolling(window=20).min()
    high = df['original'].rolling(window=20).max()
    df['indicator'] = ((high - df['original']) / (high - low)) * 100
    df['indicator'] = df['indicator'].rolling(window=10).mean()

    df = df.dropna()

    fig, ax1 = plt.subplots(figsize=(20,5))

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
    for i in range(len(df.index) - 1):
        if df['indicator'][i] > 10 and df['indicator'][i+1] < 10 and red_marker == False:
            ax2.plot(df.index[i+1], df['close'][i+1], 'r^')
            red_marker = True
            blue_marker = False
        if df['indicator'][i] < 90 and df['indicator'][i+1] > 90 and blue_marker == False:
            ax2.plot(df.index[i+1], df['close'][i+1], 'bv')
            blue_marker = True
            red_marker = False

    # ax3 = ax1.twinx()  # x축을 공유하는 두번째 축 생성

    fig.tight_layout()  # 그래프의 레이아웃을 조정
    VVR = df['indicator'][-1].round(1)
    ax1.text(df.index[-1], df['indicator'][-1] * 10000, f"VVR = {VVR}", color='blue')
    plt.show()
