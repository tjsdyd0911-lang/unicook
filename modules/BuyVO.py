class BuyVO :
    def __init__(self) :
        # buy 테이블 컬럼
        self.bno       = 0      # 구매번호
        self.id        = ""     # 아이디
        self.code      = 0      # 상품코드
        self.qty       = 0      # 수량
        self.btime     = ""     # 구매일시
        
        # item 테이블과 조인해서 가져올 추가 정보
        self.item_name   = ""   # 상품명
        self.price       = 0    # 가격
        self.image       = ""   # 상품 이미지
        self.category_id = 0    # 카테고리 ID (분석용)
        
        # chart data 가져올 추가 정보
        self.count = 0  # 구매횟수