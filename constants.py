# 상품
products = {
    # 금 : 순도 99.5% 이상으로 정제된 Bar 형태의 100 Troy Ounce 금을 기초자산으로 하는 선물계약
    "GC": {
        "exchange": "CME",
        "contract_size": 100,  # Troy Ounce
        "note": "USD",
        "tick_size": 0.1,
        "tick_value": 10,
    },
    # 원유 : 미국 서부 텍사스 지역에서 생산되는 중질유 (WTI - Western Texas Intermediate)를 기초자산으로 하는 선물계약
    "CL": {
        "exchange": "CME",
        "contract_size": 1000,  # Barrels
        "note": "USD",
        "tick_size": 0.01,
        "tick_value": 10,
    },
}
