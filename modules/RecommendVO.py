"""
AI추천(score) 테이블용 vo
"""

class RecommendVO :
    def __init__(self) :
        self.id        = ""   #상품코드
        self.code      = 0    #상품코드
        self.score     = 0    #유사도 점수
        self.algo_type = ""   #알고리즘 유형