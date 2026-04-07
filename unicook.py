from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import jsonify
from modules.UserDAO import UserDAO
from modules.ItemDAO import ItemDAO
from modules.CartDAO import CartDAO
import math

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
    
    login_info = session.get("login")
    id = login_info.get("id") if login_info else None
    
    dao = CartDAO()
    cart_list = dao.GetList(id) if id else []
    
    return render_template("cart.html", cart_list=cart_list)

# 장바구니 추가
@app.route("/cartadd.do")
def cartadd() :
    try :
        login_info = session.get("login")
        if not login_info :
            return jsonify({"result": "fail", "message": "로그인이 필요합니다."})
        id   = login_info.get("id")
        code = request.args.get("code")
        qty  = request.args.get("qty")
    
        dao = CartDAO()
        
        dao.CartAdd(id, int(code), int(qty))
        
        # 최신 데이터 가져오기
        cart_data = dao.GetList(id) if id else []
        new_count = len(cart_data)
        
        return jsonify({"result": "success", "new_count": new_count})   # 저장 성공
    except Exception as e :
        print(f"Error: {e}")
        return jsonify({"result": "fail"}) # 저장 실패

# 장바구니 삭제
@app.route("/cartdelete.do", methods=["POST"])
def cartdelete() :
    
    data = request.get_json()
    cnos = data.get("cnos")
    print(f"받은 cnos 데이터: {cnos}")
    if cnos :
        dao = CartDAO()
        dao.CartDelete(cnos)
        
        # 삭제 후 현재 세션 사용자의 최신 장바구니 개수를 다시 계산
        login_info = session.get("login")
        user_id = login_info.get("id") if login_info else None
        
        # 최신 데이터 가져오기
        cart_data = dao.GetList(user_id) if user_id else []
        new_count = len(cart_data)
        
        return jsonify({"result" : "success", "new_count": new_count})
    else :
        return jsonify({"result": "fail", "message": "No items selected"})
    

@app.route("/purchase.do")
def purchase() :
    return render_template("purchase.html")

@app.route("/bunsuk.do")
def bunsuk_main() :
    target = request.args.get("target","main")
    return render_template("bunsuk.html",target = target)
    #return render_template(f"bunsuk_{target}.html",target = target)

# 로그인 시 장바구니에 담긴 상품 갯수 조회를 헤더에 항상 표시하기 위한 함수
# @app.context_processor -> 공통 데이터 담당 (항상 표시해야될 데이터에 사용)
@app.context_processor
def cart_info() :
    login_info = session.get("login")
    id = login_info.get("id") if login_info else None
    
    cart_dao = CartDAO()
    cart_data = cart_dao.GetList(id) if id else []
    
    return dict(cart={'cnt': len(cart_data)})
    
# main 함수
if __name__ == "__main__" :
    app.run(port=8000)