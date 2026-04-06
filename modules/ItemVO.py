"""
상품정보(item) 테이블용 vo
"""

class ItemVO :
    def __init__(self) :
        self.code         = 0   #상품코드
        self.image        = ""  #이미지
        self.category_id  = ""  #카테고리ID
        self.category     = ""  #카테고리
        self.item_name    = ""  #상품명
        self.price        = 0   #가격
        self.weight       = 0   #중량
        self.view         = 0   #조회수
        self.stock        = 0   #재고