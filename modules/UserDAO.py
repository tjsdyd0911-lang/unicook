"""
회원정보 C/R/U/D 처리 클래스
"""
from modules.UserVO    import UserVO
from modules.DBManager import DBManager

class UserDAO :
    def Login(self, id, pw) :
        
        vo = None
        
        sql  = "select * from user "
        sql += f"where id = '{id}' and pw = md5('{pw}')"
        dbms = DBManager()
        dbms.DBOpen()
        total = dbms.Select(sql)
        if total >= 0 :
            vo = UserVO()
            vo.id = dbms.GetValue(0,"id")
            vo.name   = dbms.GetValue(0,"name")
        dbms.DBClose()
        return vo