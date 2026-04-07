"""
장바구니(cart) C/R/U/D 처리 클래스
"""

from modules.DBManager import DBManager
from modules.CartVO    import CartVO

class CartDAO :
    def GetList(self, id) :
        cart = []
        if not id :  # ID가 없으면 빈 리스트 반환 (비로그인 시)
            return cart
        with DBManager() as db :
            sql  = "select c.*, i.image, "
            sql += "i.item_name, i.price from cart c "
            sql += "inner join item i on i.code = c.code "
            sql += f"where id = '{id}'"
            total = db.Select(sql)
            
            for n in range(total) :
                vo = CartVO()
                vo.cno        = db.GetValue(n, "cno")
                vo.id         = db.GetValue(n, "id")
                vo.code       = db.GetValue(n, "code")
                vo.qty        = db.GetValue(n, "qty")
                vo.ctime      = db.GetValue(n, "ctime")
                vo.item_name  = db.GetValue(n, "item_name")
                vo.image      = db.GetValue(n, "image")
                vo.price      = f"{db.GetValue(n, 'price'):,}원"
                vo.price_num  = db.GetValue(n, 'price')
                vo.cnt        = total
                cart.append(vo)
        return cart

    def CartAdd(self, id, code, qty) :
        with DBManager() as db :
            sql  = "insert into cart (id, code, qty, ctime) "
            sql += f"values('{id}', {code}, {qty}, now())"
            return db.RunSQL(sql)
    
    def CartDelete(self, cnos) :
        with DBManager() as db :
            placeholders = ', '.join(['%s'] * len(cnos))
            sql = f"DELETE FROM cart WHERE cno IN ({placeholders})"
            
            cursor = db.con.cursor()
            try:
                cursor.execute(sql, tuple(cnos))
                db.con.commit()
            except Exception as e :
                print(f"삭제 중 에러 발생: {e}")
                db.con.rollback()
            finally :
                cursor.close()