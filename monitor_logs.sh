#!/bin/bash

while true; do
    # 로그 파일에 변경이 감지되면 Python 스크립트 실행
    inotifywait -e modify /path/to/output.log
    python3 /path/to/send_to_line.py
done
