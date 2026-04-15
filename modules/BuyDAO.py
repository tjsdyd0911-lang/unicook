from modules.DBManager import DBManager
from modules.BuyVO     import BuyVO

class BuyDAO :

    def GetList(self, id, period, page, per_page) :
        """
        특정 사용자의 구매 내역 목록 조회 (상품 정보 포함)
        """
        offset = (page - 1) * per_page
        buy_list = []
        # buy 테이블(b)과 item 테이블(i)을 code 기준으로 조인
        sql  = "select b.*, i.item_name, i.price, i.image, i.category_id "
        sql += "from buy b "
        sql += "join item i on b.code = i.code "
        sql += f"where b.id = '{id}' "
        if   period == "1m" :
            sql += "and b.btime >= date_sub(now(), interval 1 month) "
        elif period == "3m" :
            sql += "and b.btime >= date_sub(now(), interval 3 month) "
        sql += "order by b.btime desc " # 최근 구매순
        sql += f"limit {offset}, {per_page}"
        
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
    def GetCount(self, id, period):
        """
        특정 사용자의 전체 구매 건수를 조회
        """
        sql = f"select count(*) as cnt from buy where id = '{id}' "
        if period == "1m":
            sql += "and btime >= date_sub(now(), interval 1 month) "
        elif period == "3m":
            sql += "and btime >= date_sub(now(), interval 3 month) "
        with DBManager() as db :
            count = db.Select(sql)
            if count > 0:
                return db.GetValue(0, 'cnt')
            return 0
        
    def GetChartData(self, id) :
        """
        구매 횟수 및 구매 수량 목록 조회 (상품 정보 포함)
        """
        items = []
        with DBManager() as db :
            # buy 테이블(b)과 item 테이블(i)을 code 기준으로 조인
            # 상품이름, 구매 횟수, 구매량 구하는 구문
            sql  = "select i.item_name as item_name, "
            sql += "count(*) as freq, sum(b.qty) as qty "
            sql += "from buy b "
            sql += "join item i on b.code = i.code "
            sql += "join score s on b.code = s.code "
            sql += f"where b.id = '{id}' "
            sql += "and s.algo_type = 'best' "
            sql += "group by i.item_name "
            sql += "order by freq desc, qty desc "  
            sql += "limit 4 "
            
            list = db.Select(sql)
            for n in range(list) :
                vo = BuyVO()
                vo.item_name   = db.GetValue(n, "item_name")
                vo.count       = db.GetValue(n, "freq")
                vo.qty         = db.GetValue(n, "qty")
                
                items.append(vo)
                
        return items






















