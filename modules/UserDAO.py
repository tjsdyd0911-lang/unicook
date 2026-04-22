"""
회원정보 C/R/U/D 처리 클래스
"""
from modules.UserVO    import UserVO
from modules.DBManager import DBManager

class UserDAO :
    def Login(self, id, pw) :
        
        with DBManager() as db :
            vo = None
            
            sql  = "select * from user "
            sql += f"where id = '{id}' and pw = md5('{pw}')"
            
            total = db.Select(sql)
            if total >= 0 :
                vo = UserVO()
                vo.id = db.GetValue(0,"id")
                vo.name   = db.GetValue(0,"name")
            return vo
        
    def UserInfo(self, id) :
        with DBManager() as db :
            sql  = "select gender, age "
            sql += "from user "
            sql += f"where id = '{id}'"
            info = db.Select(sql)
            
            gender = ""
            age    = 0
            for _ in range(info) :
                gender = db.GetValue(0, "gender")
                age    = db.GetValue(0, "age")
            return gender, age
            
            
            