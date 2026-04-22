# DBManager (mysqlclient 버전)
"""
pip install mysqlclient
"""
import MySQLdb  # pymysql 대신 MySQLdb를 사용합니다.
import pandas as pd
import json
import os

def LoadDbConfig() :
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.json")
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f :
        config = json.load(f)
    return config["database"]

class DBManager:
    def __init__(self):
        self.con = None
        self.data = None
        self.desc = None
    
    # DB연결
    def __enter__(self):
        try: 
            db_config = LoadDbConfig()
            # MySQLdb.connect를 사용하며, charset 옵션은 utf8mb4를 권장합니다.
            self.con = MySQLdb.connect(**db_config)
            return self

        except Exception as e:
            raise e
    
    # DB연결 종료
    def __exit__(self, exc_type, exc_value, traceback):
        if self.con:
            self.con.close()
            
    # INSERT, UPDATE, DELETE 실행
    def RunSQL(self, sql):
        cursor = self.con.cursor()
        try:
            cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            print(f"Execute error in sql: {e}")
            self.con.rollback() # 에러 발생 시 롤백 추가
        finally:
            cursor.close()
            
    # SELECT 실행
    def Select(self, sql, params=None):
        if params is None:
            params = []
            
        cursor = self.con.cursor()
        try:
            total = cursor.execute(sql, params)
            if total > 0:
                self.data = cursor.fetchall()
                self.desc = cursor.description
            else:
                self.data = []
                self.desc = []
            return total            
        finally:
            cursor.close() 
    
    # 행 가져오기
    def GetRow(self, rowno):
        if self.data and len(self.data) > rowno:
            return self.data[rowno]
        return None
    
    # 값 가져오기
    def GetValue(self, rowno, colname):
        if not self.desc or not self.data:
            return None
            
        # 열 이름으로 인덱스 찾기
        for idx, item in enumerate(self.desc):
            if item[0] == colname:
                return self.data[rowno][idx]
        return None
    
    # dataframe 가져오기
    def GetDataFrame(self,sql) :
        self.Select(sql)
        
        if not hasattr(self, "data") or not hasattr(self, "desc"):
            return pd.DataFrame() # 빈 데이터프레임 반환
            
        # 2. self.desc에서 컬럼명만 추출
        columns = [col[0] for col in self.desc]
        
        # 3. 데이터를 기반으로 DataFrame 생성
        df = pd.DataFrame(self.data, columns=columns)
        return df