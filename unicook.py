from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from modules.UserDAO import UserDAO
from modules.ItemDAO import ItemDAO
import math
from modules.CartDAO import CartDAO

app = Flask(__name__)

app.secret_key = "unicook"

@app.route("/")
def main() :
    current_page = request.args.get('page', 1, type=int)
    category = request.args.get("category", "0")
    dao = ItemDAO()
    total, items = dao.GetList(current_page, category)
    
    # 페이지 6개씩 구현
    total_pages = math.ceil(total / 16)
    block_size = 5
    start_page = ((current_page - 1) // block_size) * block_size + 1
    end_page = start_page + block_size
    
    if end_page > total_pages:
        end_page = total_pages
    return render_template("main.html", items        = items,
                                        total_pages  = total_pages,
                                        current_page = current_page,
                                        start_page   = start_page,
                                        end_page     = end_page)

@app.route("/login.do")
def login() :
    return render_template("login.html")

#로그인 완료 (/loginok.do)
@app.route("/loginok.do", methods=["POST"])
def loginok() :
    id = request.form["id"]
    pw = request.form["pw"]
    dao = UserDAO()
    vo = dao.Login(id,pw)
    if vo == None :
        return "ERROR";
    else :
        session["login"] = { "id" : vo.id, "name" : vo.name }
        return "OK";  

# 로그아웃 (/logout.do)
@app.route("/logout.do")
def logout() :
    session["login"] = None
    return redirect("/")

# 카테고리 (/category)
@app.route("/category.do")
def category() :
    current_page = request.args.get('page', 1, type=int)
    category = request.args.get("category", "0")
    dao = ItemDAO()
    total, items = dao.GetList(current_page, category)
    
    # 페이지 6개씩 구현
    total_pages = math.ceil(total / 16)
    block_size = 5
    start_page = ((current_page - 1) // block_size) * block_size + 1
    end_page = start_page + block_size
    
    if end_page > total_pages:
        end_page = total_pages
    return render_template("_category_partial.html", items        = items,
                                                     total_pages  = total_pages,
                                                     current_page = current_page,
                                                     start_page   = start_page,
                                                     end_page     = end_page)

# 상세페이지
@app.route("/view.do")
def view() :
    code = request.args.get("code","")
    if code == "":
        return redirect("/")
    dao = ItemDAO()
    item = dao.View(code)
    return render_template("view.html", item=item)

@app.route("/cart.do")
def cart() :
    return render_template("cart.html")

# 장바구니 추가
@app.route("/cartadd.do")
def cartadd() :
    try :
        login_info = session.get("login")
        id   = login_info.get("id")
        code = request.args.get("code")
        qty  = request.args.get("qty")
        
        
        code = int(code)
        qty  = int(qty)
    
        dao = CartDAO()
        
        dao.CartAdd(id, code, qty)
        return "OK"   # 저장 성공
    except :
        return "FAIL" # 저장 실패

@app.route("/purchase.do")
def purchase() :
    return render_template("purchase.html")

@app.route("/bunsuk.do")
def bunsuk_main() :
    target = request.args.get("target","main")
    return render_template("bunsuk.html",target = target)
    #return render_template(f"bunsuk_{target}.html",target = target)
    

# main 함수
if __name__ == "__main__" :
    app.run(port=8000)