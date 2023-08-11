import requests

def send_log_to_line():
    # LINE Notify 토큰
    LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN_HERE"

    # 로그 파일 경로
    FILE_PATHS = ["output.log", "output2.log"]

    # 메시지에 파일 내용 추가
    message = ""
    for file_path in FILE_PATHS:
        with open(file_path, 'r') as file:
            content = file.read()
            message += f"Content of {file_path}:\n{content}\n\n"

    # LINE Notify API URL
    url = "https://notify-api.line.me/api/notify"

    # 메시지 전송
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"message": message}
    response = requests.post(url, headers=headers, data=payload)

    return {
        'statusCode': response.status_code,
        'body': response.text
    }

send_log_to_line()

