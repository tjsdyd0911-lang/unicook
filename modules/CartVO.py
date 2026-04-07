"""
장바구니(cart) 테이블용 vo
"""

class CartVO :
    def __init__(self) :
        self.cno       = 0   #장바구니 번호
        self.id        = ""  #구매자 아이디
        self.code      = ""  #상품명
        self.qty       = 0   #구매수량
        self.ctime     = ""  #장바구니 담은 날짜
        self.item_name = ""  #장바구니 담은 상품명 
        self.image     = ""  #장바구니 담은 상품 이미지
        self.price     = 0   #장바구니 담은 상품 가격
        self.price_num = 0   #장바구니 상품 가격 int
        self.count     = 0   #장바구니에 담긴 상품 갯수