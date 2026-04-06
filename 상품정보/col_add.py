import pandas as pd
import random

# 원본 csv 파일 불러오기
item_file = "easyfood.csv"

# csv=> 데이터프레임
items = pd.read_csv(item_file, encoding="utf-8")
print(items)

# 가격컬럼 문자->숫자형 변환 전처리
items['가격'] = items['가격'].replace('[^0-9]', '', regex=True).astype(int)
print(items['가격'])
"""
prices = items["가격"]
prices_num = []
for price in prices :
    num = price.replace(",","")
    prices_num.append(num)
print(prices_num)
"""

# 조회수, 재고 데이터 생성
view = [random.randint(0, 1000) for _ in range(484)]
print(view)

stock = [random.randint(0, 500) for _ in range(484)]
print(stock)

# 데이터 결합
dic_data = {
        "조회수" : view,
        "재고"   : stock
    }

# 데이터프레임 생성
df = pd.DataFrame(dic_data)
print(df)

# 데이터프레임 결합
df_items = pd.concat([items, df], axis=1)
print(df_items)

df_items.to_csv("상품컬럼추가.csv", index=False ,encoding="utf-8-sig")