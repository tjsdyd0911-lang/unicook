import pandas as pd
import random
from datetime import datetime, timedelta

# 📂 파일 경로
user_file = "csv/users_100.csv"
product_file = "csv/easyfood.csv"

# 📥 데이터 불러오기
users = pd.read_csv(user_file,encoding="utf-8")
products = pd.read_csv(product_file,encoding="utf-8")

user_ids = users['user_id'].tolist()
product_ids = products['상품코드'].tolist()

# 📦 결과 저장 리스트
orders = []

order_id = 1

# 📅 날짜 범위 (최근 90일)
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

def random_date():
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return (start_date + timedelta(days=random_days,seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S")

"""
# 🔥 인기 상품 가중치 설정
# 상위 20개 상품은 5배 더 잘 팔리게 설정
weights = []
for pid in product_ids:
    if pid <= 20:
        weights.append(5)   # 인기 상품
    else:
        weights.append(1)   # 일반 상품
"""

# 🔥 구매 데이터 생성
for user_id in user_ids:
    for _ in range(100):  # 사용자당 100개 구매
        order_date = random_date()
        product_id = random.choices(product_ids, k=1)[0]
        quantity = random.randint(1, 3)
        

        orders.append([
            order_id,
            user_id,
            product_id,
            quantity,
            order_date
        ])

        order_id += 1

# 📊 DataFrame 생성
orders_df = pd.DataFrame(orders, columns=[
    "order_id", "user_id", "product_id", "수량", "주문일자"
])

# 💾 CSV 저장
orders_df.to_csv("order_list.csv", index=False, encoding="utf-8-sig")

print("✅ 인기 상품 편향 반영 주문 데이터 생성 완료")

