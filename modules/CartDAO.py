"""
장바구니(cart) C/R/U/D 처리 클래스
"""

from modules.DBManager import DBManager
from modules.CartVO    import CartVO

class CartDAO :
    def GetList(self, qty) :
        cart = []
        with DBManager() as db :
            sql  = "select c.*, i.image, i.item_name, i.price from cart c "
            sql += "inner join item i i.code = c.code "
            sql += f"where id = {id}"
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
                cart.append(vo)
        return cart

    def CartAdd(self, id, code, qty) :
        with DBManager() as db :
            sql  = "insert into cart (id, code, qty, ctime) "
            sql += f"values('{id}', {code}, {qty}, now())"
            return db.RunSQL(sql)