from modules.DBManager import DBManager
from modules.BuyVO     import BuyVO

class BuyDAO :
    def GetList(self, id, period) :
        """
        특정 사용자의 구매 내역 목록 조회 (상품 정보 포함)
        """
        buy_list = []
        # buy 테이블(b)과 item 테이블(i)을 code 기준으로 조인
        sql  = "select b.*, i.item_name, i.price, i.image, i.category_id "
        sql += "from buy b "
        sql += "join item i on b.code = i.code "
        sql += f"where b.id = '{id}' "
        sql += "order by b.btime desc " # 최근 구매순
        sql += "limit 0,10"
        print(sql)
        
        with DBManager() as db :
            count = db.Select(sql)
            for n in range(count) :
                vo = BuyVO()
                # buy 테이블 데이터
                vo.bno     = db.GetValue(n, "bno")
                vo.id      = db.GetValue(n, "id")
                vo.code    = db.GetValue(n, "code")
                vo.qty     = db.GetValue(n, "qty")
                vo.btime   = db.GetValue(n, "btime")
                
                # 조인된 item 테이블 데이터
                vo.item_name   = db.GetValue(n, "item_name")
                vo.price       = db.GetValue(n, "price")
                vo.image       = db.GetValue(n, "image")
                vo.category_id = int(db.GetValue(n, "category_id"))
                
                buy_list.append(vo)
        
        return buy_list
    def Insert(self, id, code, qty) :
        with DBManager() as db :
            sql  = "insert into buy(id, code, qty, btime) "
            sql += f"values('{id}', {code}, {qty}, now())"
            return db.RunSQL(sql)