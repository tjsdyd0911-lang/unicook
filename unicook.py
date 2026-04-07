from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session, jsonify
from modules.UserVO  import UserVO
from modules.UserDAO import UserDAO
from modules.ItemVO  import ItemVO
from modules.ItemDAO import ItemDAO

from modules.CartVO  import CartVO
from modules.CartDAO import CartDAO
import math

from modules.BuyVO  import BuyVO
from modules.BuyDAO  import BuyDAO


app = Flask(__name__)

app.secret_key = "unicook"

@app.route("/")
def main() :
    current_page = request.args.get('page', 1, type=int)
    category = request.args.get("category", "0")
    dao = ItemDAO()
    total, items = dao.GetList(current_page, category)
    
    # 페이지 5개씩 구현
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

# 로그인 체크(/loginCheck.do)
@app.route("/loginCheck.do")
def login_check() : 
    if session.get('login') :
        return jsonify({"login" : True})
    else :
        return jsonify({"login" : False})

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
def purchase():
   
    # 1. 로그인 여부 확인
    if "login" not in session or session["login"] is None:
        return redirect("/login.do") # 슬래시(/)를 붙이는 것이 더 안전합니다.
    
    # 2. 세션에서 아이디 가져오기 (따옴표 "id" 확인!)
    user_id = session["login"]["id"] 
    
    dao = BuyDAO()
    buys = dao.GetList(user_id)

    # 4. HTML에 전달
    return render_template("purchase.html", buys=buys)

@app.route("/bunsuk.do")
def bunsuk_main() :
    target = request.args.get("target","main")
    return render_template("bunsuk.html",target = target)
    #return render_template(f"bunsuk_{target}.html",target = target)
    

# main 함수
if __name__ == "__main__" :
    app.run(port=8000)