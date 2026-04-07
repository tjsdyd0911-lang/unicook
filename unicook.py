import math
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import session
from flask import jsonify
from flask import url_for
from modules.UserDAO import UserDAO
from modules.ItemDAO import ItemDAO
from modules.CartDAO import CartDAO
from modules.BuyDAO  import BuyDAO

app = Flask(__name__)

app.secret_key = "unicook"

@app.before_request 
def add_header():
    print("add head...")
    response = make_response("Custom Response Body")
    # 브라우저에게 응답 내용을 캐시(저장)하지 말라고 지시
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

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
    session.clear()
    return redirect(url_for('main'))

# 로그인 체크(/loginCheck.do)
@app.route("/loginCheck.do")
def login_check() : 
    if session.get('login') :
        return jsonify({"login" : True})
    else :
        return jsonify({"login" : False})
    
# 검색 (/search)
@app.route("/search.do")
def search() :
    current_page = request.args.get('page', 1, type=int)
    category = "0"
    keyword = request.args.get('keyword')
    dao = ItemDAO()
    total, items = dao.GetList(current_page, category, keyword)
    
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

# 구매 완료 처리
@app.route("/purchase.do", methods=["POST"])
def purchaseadd():
    data  = request.get_json()
    items = data.get("items")
    login_info = session.get("login")
    id = login_info.get("id")
    
    if not login_info :
        return jsonify({"result": "fail", "message": "로그인이 필요합니다."})
    
    buy_dao  = BuyDAO()
    cart_dao = CartDAO()
    
    cno_list = []
    for item in items :
        cno  = item["cno"]
        code = item["code"]
        qty  = item["qty"]
        
        buy_dao.Insert(id, code, qty)
        
        cno_list.append(cno)
    
    if cno_list:
        cart_dao.CartDelete(cno_list)
        
    return "success"

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