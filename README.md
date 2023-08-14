# Upbit 코인 현물 자동매매시스템 Upbot

no(*추가)한국 기준으로 서버 시간 설정: sudo ln -sf /usr/share/zoneinfo/Asia/Seoul/etc/localtime
현재 경로 상세 출력: ls -al
경로 이동: cd 경로

vim 에디터로 파일 열기: vim bitcoinAutoTrade.py

vim 에디터 입력: i

vim 에디터 저장: :wq!

패키지 목록 업데이트: sudo apt update

pip3 설치: sudo apt install python3-pip

pip3로 pyupbit 설치: pip3 install pyupbit

백그라운드 실행: nohup python3 bitcoinAutoTrade.py > output.log &

실행되고 있는지 확인: ps ax | grep .py

프로세스 종료(PID는 ps ax | grep .py를 했을때 확인 가능): kill -9 PID

주소, 파일 삭제: rm -rf git주소 혹은 파일(CoinScalping)

깃허브 주소 가져오기: git clone git주소

파일 내 에러가 있을 때 nohup 실행되지 않음.

실행되지 않는 이유를 살펴보려면 output.log 살펴보면 됨. less output.log에서 확인.

백그라운드 실행 시 CoinScalping으로 경로 이동 후 nohup ~ 써야함.

cd CoinScalping

git status

git stash

git pull origin main

git fetch origin

git reset --hard origin/main

하면 해당 레퍼지토리 업데이트됨

이때 백그라운드 실행하고 있던 프로그램은 리셋되지 않고 초기 상태 유지

아예 수정하고 싶으면 kill -9 PID 후 업데이트 후 백그라운드 실행.

CoinScalping에서 다시 홈으로 이동 cd ~
