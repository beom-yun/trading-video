import csv
from datetime import datetime
from collections import deque


def print_trades():
    print("<< trades >>")
    for k in trades:
        print(f"[종목 : {k}]")
        for r in trades[k]:
            print(r)
    print()


# csv로부터 체결내역 가져오기(TR 3414)
csv_data = list()
with open("3414_해외_일자별_체결내역.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        for i in range(len(row)):
            row[i] = row[i].replace('"', "").replace("=", "").replace(",", "")
        csv_data.append(row)

# 비어있는 행 지우기, list -> dict 변환
data = deque()
for row_csv_data in csv_data[:0:-1]:
    if row_csv_data[0]:
        data.append({csv_data[0][i]: row_csv_data[i] for i in range(len(csv_data[0]))})

# 데이터 전처리
for i in range(len(data)):
    data[i] = {
        "일시": datetime.strptime(
            f"{data[i]['체결일자']} {data[i]['체결시간']}", "%Y/%m/%d %H:%M:%S"
        ),
        "종목": data[i]["종목"],
        "구분": data[i]["매매구분"],
        "가격": float(data[i]["체결가격"]),
        "수량": int(data[i]["체결수량"]),
        "금액": int(data[i]["체결금액"]),  # float으로 안 해도 괜찮으련지?
        "통화": data[i]["통화"],
    }

# trades : 종목별 청산내역 queue
trades = dict()
while data:
    new_trade = data.popleft()
    print(f"새로 들어온 : {new_trade}")

    # 종목 자체가 없으면 새로 만들기기
    if new_trade["종목"] not in trades:
        trades[new_trade["종목"]] = deque()

    # 종목 queue가 비어있다면 새로운 거래내역을 append
    if not trades[new_trade["종목"]]:
        trades[new_trade["종목"]].append(new_trade)
        print("매매 싸이클 시작")
        print_trades()
        continue

    # 종목 queue가 비어있지 않을 경우
    # queue의 최우선 거래내역의 매매구분과 새로운 거래내역의 매매구분을 비교
    x = trades[new_trade["종목"]].popleft()

    # 매매구분이 같을 경우 (매수 - 매수 / 매도 - 매도)
    if x["구분"] == new_trade["구분"]:
        trades[new_trade["종목"]].appendleft(x)
        trades[new_trade["종목"]].append(new_trade)
    # 매매구분이 다를 경우 (매수 - 매도 / 매도 - 매수)
    else:
        if x["수량"] == new_trade["수량"]:
            print("청산")
        elif x["수량"] > new_trade["수량"]:
            print(f"일부청산")
            x["금액"] = (x["금액"] // x["수량"]) * (x["수량"] - new_trade["수량"])
            x["수량"] = x["수량"] - new_trade["수량"]
            trades[new_trade["종목"]].appendleft(x)
        else:
            print("일부청산2")
            new_trade["금액"] = (new_trade["금액"] // new_trade["수량"]) * (
                new_trade["수량"] - x["수량"]
            )
            new_trade["수량"] = new_trade["수량"] - x["수량"]
            data.appendleft(new_trade)

    if not trades[new_trade["종목"]]:
        print("매매 싸이클 종료")

    print_trades()
