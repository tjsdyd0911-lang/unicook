import pandas as pd
import random
from datetime import datetime, timedelta
import io

# 1. 데이터 로드 (제공해주신 텍스트 데이터 기반)
user_csv = """id,pw,name,age,gender
user_001,pass001!,이이선,20,여자
user_002,pass002!,진지수,38,여자
... (중략) ...
user_100,pass100!,양도윤,27,남자"""

# 실제 환경에서는 파일을 읽으므로 아래와 같이 처리합니다.
item_df = pd.read_csv('상품컬럼추가.csv')
user_df = pd.read_csv('회원정보.csv')

# 예시용 유저 ID 리스트 (제공된 100명 데이터 기반)
user_ids = [ userid for userid in user_df["id"] ]


# 예시용 상품 코드 리스트 (제공된 CSV에서 추출한 실제 코드들)
item_codes = [ item_code for item_code in item_df["상품코드"] ]


# 2. 랜덤 날짜 생성 함수 (최근 1년 내)
def get_random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

# 3. 데이터 생성 설정
total_records = 100000
batch_size = 1000  # 1000개씩 묶어서 INSERT 구문 생성 (성능 최적화)

with open('buy_data_insert.sql', 'w', encoding='utf-8') as f:
    f.write("-- 구매내역 더미 데이터 10만건 생성\n")
    
    values = []
    for i in range(1, total_records + 1):
        user_id = random.choice(user_ids)
        item_code = random.choice(item_codes)
        qty = random.randint(1, 5)
        btime = get_random_date()
         
        values = f"'{user_id}', {item_code}, {qty}, '{btime}'"
        sql = f"INSERT INTO buy (id, code, qty, btime) VALUES ({values}) ;\n"
        f.write(sql)
        
        # SQL 구문 형태로 변환
        """
        values.append(f"('{user_id}', {item_code}, {qty}, '{btime}')")
        
        # 배치 사이즈마다 파일에 쓰기        
        if i % batch_size == 0:
            sql = f"INSERT INTO buy (id, code, qty, btime) VALUES\n" + ",\n".join(values) + ";\n\n"
            f.write(sql)
            values = []
        """

print(f"완료! 'buy_data_insert.sql' 파일이 생성되었습니다. (총 {total_records}건)")
