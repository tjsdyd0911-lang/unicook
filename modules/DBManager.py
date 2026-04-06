# DBManager

import pymysql

class DBManager :
    def __init__(self) :
        self.con = None
    
    # DB연결
    def __enter__(self) :
        try : 
            self.con = pymysql.connect(host="127.0.0.1",
                                       user="root",
                                       password="ezen",
                                       db="unicook",
                                       charset="utf8")
            return self
        except Exception as e :
            raise e
    
    # DB연결 종료
    def __exit__(self, exc_type, exc_value, traceback):
        if self.con :
            self.con.close()
            
    # INSERT, UPDATE, DELETE 실행
    def RunSQL(self, sql) :
        cursor = self.con.cursor()
        cursor.execute(sql)
        self.con.commit()
        cursor.close()
    
    # SELECT 실행
    def Select(self, sql) :
        cursor = self.con.cursor()
        total = cursor.execute(sql)
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
    