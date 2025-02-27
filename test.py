import csv
from datetime import datetime
from collections import deque


mock_fee = 14  # 모의계좌 수수료(USD)


def print_trades():
    print("<< trades >>")
    for k in trades:
        print(f"[종목 : {k}]")
        for r in trades[k]:
            print(r)
    print()


def print_tractions():
    print("<< transactions >>")
    for k in transactions:
        print(f"[종목 : {k}]")
        for r in transactions[k]:
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
# transactions : 매매 트랜잭션(싸이클 시작에서부터 종료까지)
trades = dict()
transactions = dict()

while data:
    new_trade = data.popleft()

    # 종목 자체가 없으면 새로 만들기
    if new_trade["종목"] not in trades:
        trades[new_trade["종목"]] = deque()
        transactions[new_trade["종목"]] = list()

    # 종목 queue가 비어있다면 새로운 거래내역을 append
    # 매매 싸이클 시작
    if not trades[new_trade["종목"]]:
        trades[new_trade["종목"]].append(new_trade)
        transactions[new_trade["종목"]].append(
            {
                "ticker": new_trade["종목"],
                "start_time": new_trade["일시"],
                "end_time": None,
                "type": new_trade["구분"],
                "pnl": 0,
                "fee": 0,
            }
        )
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
        tr_size = min(x["수량"], new_trade["수량"])

        if x["수량"] == new_trade["수량"]:
            if transactions[new_trade["종목"]][-1]["type"] == "매수":
                transactions[new_trade["종목"]][-1]["pnl"] += (
                    new_trade["금액"] - x["금액"]
                )
            else:
                transactions[new_trade["종목"]][-1]["pnl"] += (
                    x["금액"] - new_trade["금액"]
                )
        elif x["수량"] > new_trade["수량"]:
            if transactions[new_trade["종목"]][-1]["type"] == "매수":
                transactions[new_trade["종목"]][-1]["pnl"] += (
                    new_trade["금액"] - (x["금액"] // x["수량"]) * tr_size
                )
            else:
                transactions[new_trade["종목"]][-1]["pnl"] += (
                    x["금액"] // x["수량"]
                ) * tr_size - new_trade["금액"]
            x["금액"] = (x["금액"] // x["수량"]) * (x["수량"] - new_trade["수량"])
            x["수량"] = x["수량"] - new_trade["수량"]
            trades[new_trade["종목"]].appendleft(x)
        else:
            if transactions[new_trade["종목"]][-1]["type"] == "매수":
                transactions[new_trade["종목"]][-1]["pnl"] += (
                    new_trade["금액"] // new_trade["수량"]
                ) * tr_size - x["금액"]
            else:
                transactions[new_trade["종목"]][-1]["pnl"] += (
                    new_trade["금액"] // new_trade["수량"]
                ) * tr_size - x["금액"]
            new_trade["금액"] = (new_trade["금액"] // new_trade["수량"]) * (
                new_trade["수량"] - x["수량"]
            )
            new_trade["수량"] = new_trade["수량"] - x["수량"]
            data.appendleft(new_trade)
        transactions[new_trade["종목"]][-1]["fee"] += mock_fee * tr_size

    # 매매 싸이클 종료
    if not trades[new_trade["종목"]]:
        transactions[new_trade["종목"]][-1]["end_time"] = new_trade["일시"]

print_tractions()
