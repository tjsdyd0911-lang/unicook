"""
상품정보(item) C/R/U/D 처리 클래스
"""

from modules.DBManager import DBManager
from modules.ItemVO    import ItemVO

class ItemDAO :
    def GetList(self, page, category) :
        """
        게시물 목록
        category:category_id -> 
        샐러드/샌드위치 : 1, 분식 : 2, 밀키트 : 3, 
        도시락/밥류 : 4, 치킨/피자/핫도그/만두 : 5
        """
        offset = (int(page) - 1) * 10
        item = []
        with DBManager() as db :
            sql  = "select count(code) as total "
            sql += "from item "
            if category != "0" :
                sql += f"where category = '{ category }' "
            total = db.Select(sql)
            
            sql  = "select * from item "
            if category != "0" :
                sql += f"where category = '{ category }' "
            sql += "order by view desc "
            sql += f"limit { offset }, 16 "
            
            count = db.Select(sql)
            for n in range(count) :
                vo = ItemVO()
                vo.code        = db.GetValue(n, "code")
                vo.image       = db.GetValue(n, "image")
                vo.category_id = db.GetValue(n, "category_id")
                vo.category    = db.GetValue(n, "category")
                vo.item_name   = db.GetValue(n, "item_name")
                vo.price       = f"{db.GetValue(n, 'price'):,}원"
                vo.weight      = db.GetValue(n, "weight")
                vo.view        = db.GetValue(n, "view")
                vo.stock       = db.GetValue(n, "stock")
                item.append(vo)
        print(total)
        return total, item
    
    def View(self, code, hit_up=True) :
        """
        게시물 정보 조회 및 조회수 증가
        """
        with DBManager() as db :
            
            # 2. 조회수 증가(Update) 쿼리 실행
            if hit_up:
                sql_up = f"update item set view = view + 1 where code = {code}"
                db.RunSQL(sql_up) # 조회수 업데이트
            
            sql  = "select * from item "
            sql += f"where code = {code} "
            count = db.Select(sql)
            vo = ItemVO()
            if count > 0 :
                vo.code = db.GetValue(0, "code")
                vo.image       = db.GetValue(0, "image")
                vo.category_id = db.GetValue(0, "category_id")
                vo.category    = db.GetValue(0, "category")
                vo.item_name   = db.GetValue(0, "item_name")
                vo.price       = f"{db.GetValue(0, 'price'):,}원"
                vo.weight      = db.GetValue(0, "weight")
                vo.view        = db.GetValue(0, "view")
                vo.stock       = db.GetValue(0, "stock")
                
                return vo
            
                