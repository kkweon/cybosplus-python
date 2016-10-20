# cybosplus-python
CybosPlus Python Wrapper (+ flask API server)

## Requirements
0. python2 (*32bit*)
1. flask
2. flask-restful
3. flask-cors
4. pywin32
5. pywinauto

## Configuration (config.py)
1. DEBUG = False
    True => Cybos 시작안함.
2. CYBOS_TRADING_PASSWORD = "0302"
    Cybos 거래용 비밀번호 4자리
    
## How to Run
1. Windows CMD *관리자 권한* 실행
```cmd
python app.py
```
2. [http://localhost](http://localhost)

## API 설명
1. /info (*GET*)
    - 연결 정보
    - 시장 오픈/종료 시간
    
2. /portfolio (*GET*)
    - 계좌 포트폴리오 정보

3. /stock
    - /stock/buy (*POST*)
        - 매수/매도
    - /stock/info (*POST*)
        - 복수 종목의 현재가 정보
    - /stock/info/<string:stock_code> (*POST*)
        - 단일 종목의 정보
        
 

