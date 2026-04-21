# DBManager

import pymysql
import pandas as pd

class DBManager :
    def __init__(self) :
        self.con = None
    
    # DB연결
    def __enter__(self) :
        try : 
            self.con = pymysql.connect(host="192.168.0.35",
                                       user="unicook",
                                       password="cook",
                                       db="unicook",
                                       charset="utf8")
            return self
        except Exception as e :
            print(e)
            raise e
    
    # DB연결 종료
    def __exit__(self, exc_type, exc_value, traceback):
        if self.con :
            self.con.close()
            
    # INSERT, UPDATE, DELETE 실행
    def RunSQL(self, sql) :
        print(sql)
        print("-" * 40)
        
        cursor = self.con.cursor()
        try :
            cursor.execute(sql)
            self.con.commit()
            cursor.close()
        except :
            print("excute error in sql")
            cursor.close()
            return
            
    
    # SELECT 실행
    def Select(self, sql, params=[]) :
        print(sql)
        print("-" * 40)
        cursor = self.con.cursor()
        total = cursor.execute(sql, params)
        if total > 0 :
            self.data = cursor.fetchall()
            self.desc = cursor.description
        
        cursor.close() 
        return total
    
    # 행 가져오기
    def GetRow(self, rowno):
        return self.data[rowno]
    
    # 값 가져오기
    def GetValue(self, rowno, colname) :
        #열이름 가져오기
        for idx, item in enumerate(self.desc) :
            if item[0] == colname :
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
        print(df.head())
        return df
    
    