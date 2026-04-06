"""
회원정보(user) 테이블용 vo
"""
class UserVO :
    def __init__(self) :
        self.id     = "" # 아이디
        self.pw     = "" # 비밀번호
        self.name   = "" # 이름
        self.age    = 0  # 나이
        self.gender = "" # 성별