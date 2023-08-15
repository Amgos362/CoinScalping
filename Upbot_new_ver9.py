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

avg_buy_price = {}
balances = upbit.get_balances()
if not balances:
    print("Failed to fetch initial balances.")

for balance in balances:
    currency = balance['currency']
    coin_name = f"KRW-{currency}"

    if coin_name in coins:
        avg_buy_price[coin_name] = pyupbit.get_current_price(coin_name)
        if avg_buy_price[coin_name] is None:
            print(f"Failed to fetch price for {coin_name}")

def buy(coin, vvr):
    krw = upbit.get_balance("KRW")
    retry_count = 0

    while krw is None and retry_count < 5:
        print("Failed to fetch KRW balance, retrying...")
        time.sleep(1)
        krw = upbit.get_balance("KRW")
        retry_count += 1

    if krw is None:
        print("Failed to fetch KRW balance after retries.")
        return

    if not avg_buy_price:  # 첫 번째 매수
        investment = krw * 0.5 * 0.9995  # 현금의 절반
    else:  # 두 번째 매수
        investment = krw * 0.9995  # 남은 현금 전부

    if investment > 5000:
        upbit.buy_market_order(coin, investment)
        coin_amount = upbit.get_balance(coin[4:])
        if coin_amount is None:
            print(f"Failed to fetch balance for {coin}")
            return
        avg_buy_price[coin] = pyupbit.get_current_price(coin)
        if avg_buy_price[coin] is None:
            print(f"Failed to fetch price for {coin}")
            return
        buy_message = f"매수 {coin}: {coin_amount}개, 평단 {avg_buy_price[coin]}원, VVR = {vvr.round(1)}"
        send_message(buy_message, MESSAGE_TOKEN)


def sell(coin, vvr):
    coin_amount_before = upbit.get_balance(coin[4:])
    if coin_amount_before is None:
        print(f"Failed to fetch balance for {coin}")
        return

    coin_value_before = coin_amount_before * avg_buy_price.get(coin, 0)
    upbit.sell_market_order(coin, coin_amount_before)
    krw_after = upbit.get_balance("KRW")
    if krw_after is None:
        print("Failed to fetch KRW balance after selling.")
        return

    profit_loss = krw_after - coin_value_before * 2
    profit_loss_percent = (profit_loss / coin_value_before) * 100 if coin_value_before != 0 else 0
    sell_message = f"매도 {coin}: {coin_amount_before}개, 손익금 {profit_loss}원 ({profit_loss_percent}%), VVR = {vvr.round(1)}"
    send_message(sell_message, MESSAGE_TOKEN) 
    if coin in avg_buy_price:
        del avg_buy_price[coin]

def send_message(message, token=None):
    try:
        response = requests.post(
            TARGET_URL,
            headers={'Authorization': 'Bearer ' + token},
            data={'message': message}
        )
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred when sending message: {e}")

while True:
    for i, coin in enumerate(coins):
        df = pyupbit.get_ohlcv(ticker=coin, interval=intervals[i])
        if df is None:
            print(f"Nonetype {coin} occurred")
            time.sleep(1)
            continue
        now_indicator = calculate_indicator(df)

        if now_indicator <= 10 and coin not in avg_buy_price:
            buy(coin, now_indicator)
        elif now_indicator >= 90 and coin in avg_buy_price:
            sell(coin, now_indicator)

        time.sleep(0.5)
