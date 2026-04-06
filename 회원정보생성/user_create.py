# 회원정보 생성 프로그램

import random
import pandas as pd

# 사용자 아이디 : user_001~user_100
user_ids = []
for n in range(1, 101) :
    user_id = "user_%03d" % n
    user_ids.append(user_id)

# 사용자 비밀번호 : pass001!~pass100!    
user_pws = []
for n in range(1, 101) :
    user_pw = "pass%03d!" % n
    user_pws.append(user_pw)
    
# 성과 이름 리스트 정의
first_names = ["김", "이", "박", "최", "정", "강", "조", "백", "진", "차", "양"]
last_names = ["철수", "영희", "민수", "지영", "도윤", "서연", "자바", "이선", "지수"]

# 랜덤으로 이름 생성
def random_name():
    first = random.choice(first_names)
    last = random.choice(last_names)
    return first + last

user_names = []
for _ in range(100):
    user_names.append(random_name())

# 연령 20~65 세 랜덤 생성
user_ages = [random.randint(20, 65) for _ in range(100)]

# 성별 100명 랜덤 생성
user_genders = [random.choice(["남자", "여자"]) for _ in range(100)]

# 회원정보 리스트 생성
users = []
for user_id, user_pw, user_name, user_age, user_gender in zip(user_ids, user_pws, user_names, user_ages, user_genders) :
    row_data = [user_id, user_pw, user_name, user_age, user_gender]
    users.append(row_data)

col_name = ["id", "pw", "name", "age", "gender"]

# 데이터프레임 생성
users_df = pd.DataFrame(users, columns=col_name)

# csv 저장
users_df.to_csv("회원정보.csv", index=False, encoding="utf-8-sig")

print("회원정보 생성 완료!")