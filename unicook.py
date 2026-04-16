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
from modules.RecommendDAO import RecommendDAO

app = Flask(__name__)

app.secret_key = "unicook"

@app.before_request 
def add_header():
    response = make_response("Custom Response Body")
    # 브라우저에게 응답 내용을 캐시(저장)하지 말라고 지시
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

@app.route("/")
def main() :
    
    login_info = session.get("login")
    id = login_info.get("id") if login_info else None
    
    time_dao  = RecommendDAO()
    time_data, slot, slot_range = time_dao.GetAiRecommend(id)
    
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
                                        end_page     = end_page,
                                        time_data    = time_data,
                                        slot         = slot,
                                        slot_range   = slot_range
                                        )

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
    
# 검색/카테고리 (/navi)
@app.route("/navi.do")
def navi() :
    current_page = request.args.get('page', 1, type=int)
    category = request.args.get("category", "0")
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
    
    cart_dao = CartDAO()
    cart_list = cart_dao.GetList(id) if id else []
    
    
    return render_template("cart.html", cart_list=cart_list)

# 장바구니 추가
@app.route("/cartadd.do")
def cartadd() :
    try :
        login_info = session.get("login")
        if not login_info :
            return jsonify({"result": "login", "message": "로그인이 필요합니다."})
        id   = login_info.get("id")
        code = request.args.get("code")
        qty  = request.args.get("qty")
    
        dao = CartDAO()
        
        existing_items = dao.GetList(id)
        
        already_cart = any(int(item.code) == int(code) for item in existing_items)
        
        if already_cart :
            return jsonify({"result": "duplicate", "message": "이미 장바구니에 담긴 상품입니다."})
        
        dao.CartAdd(id, int(code), int(qty))
        
        # 최신 데이터 가져오기
        cart_data = dao.GetList(id) if id else []
        new_count = len(cart_data)
        
        return jsonify({"result": "success", "new_count": new_count})   # 저장 성공
    except Exception as e :
        print(f"Error: {e}")
        return jsonify({"result": "fail"}) # 저장 실패

# 장바구니 상품 수량변경
@app.route("/update_cart_qty.do", methods=["POST"])
def update_cart_qty() :
    cno = request.form.get("cno")
    qty = request.form.get("qty")
    
    dao = CartDAO()
    
    dao.CartQtyUdate(cno, qty)
    
    return "success"
    
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
   
    # 로그인 여부 확인
    if "login" not in session or session["login"] is None:
        return redirect("/login.do") # 슬래시(/)를 붙이는 것이 더 안전합니다.
    
    
    period = request.args.get("period","all")   
    current_page = request.args.get('page', 1, type=int)
    
    # 세션에서 아이디 가져오기 (따옴표 "id" 확인!)
    user_id = session["login"]["id"] 
    
    per_page = 5
    
    dao   = BuyDAO()
    total = dao.GetCount(user_id, period)    
    buys  = dao.GetList(user_id, period, current_page, per_page)
    

    dao = RecommendDAO()
    reco_items = dao.RecommendItem(user_id, "best")

    maxpage = (total - 1) // per_page + 1 if total > 0 else 1
    
    # 5개씩 슬라이싱
    start_page = (current_page -1) * per_page;
    end_page = start_page + per_page
    
    # 페이지 블록
    block_size = 5
    start_page = ((current_page - 1) // block_size) * block_size + 1
    end_page = start_page + block_size - 1
      
    if end_page > maxpage :
       end_page = maxpage
    
    return render_template("purchase.html", 
                           buys=buys, # 잘려진 구매 내역
                           period = period,
                           maxpage=maxpage, 
                           current_page=current_page,
                           start_page=start_page, 
                           end_page=end_page,
                           reco_items=reco_items
                           )

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
def bunsuk(target = None) :
    
    login_info = session.get("login")
    id = login_info.get("id") if login_info else None
    check_id = True if id else False
    
    if not target :
        target = request.args.get("target","main")
    
    if target == "main" :
        time_dao  = RecommendDAO()
        time_data, slot, slot_range = time_dao.GetAiRecommend(id)
        return render_template("bunsuk_main.html", 
                               target     = target,
                               check_id   = check_id,
                               time_data  = time_data,
                               slot       = slot,
                               slot_range = slot_range
                               )
    if target == "cart" :
        re_dao = RecommendDAO()
        re_dao.CartAiRecommend(id, algo_type = "cart")
        total, items = re_dao.GetByUserFrequency(id, n=4, algo_type = "cart")
        if int(total) > 0 :
            return render_template("bunsuk_cart.html",
                                   target = target,
                                   total  = total,
                                   items  = items
                                   )
    
    if target == "purchase" :
        buy_dao = RecommendDAO()
        buy_dao.MakePersonalBestRecommendations(id, algo_type = "best")
        total,items = buy_dao.GetByUserFrequency(id, n=4, algo_type = "best")
        if int(total) > 0 :
            return render_template("/bunsuk_purchase.html",
                                   target = target,
                                   total  = total,
                                   items  = items
                                   )
    
    #return render_template(f"bunsuk_{target}.html",target = target)

# 분석한 추천 상품
@app.route("/recommend.do")
def recommend() :
    # 로그인 여부 확인
    if "login" not in session or session["login"] is None:
        return redirect("/login.do")
    
    id = session["login"]["id"]
    
    target = request.args.get("target", "main")
    print(target)
    dao = RecommendDAO()
    if target == "purchase" :
        reco_items = dao.RecommendItem(id, "best")
        reco_dict = [
            {
                "code": vo.code, 
                "image": vo.image, 
                "item_name": vo.item_name, 
                "price": vo.price
            } for vo in reco_items
        ]
        return jsonify(reco_dict)
        
    if target == "cart" :
        reco_items = dao.RecommendItem(id, "cart")
        reco_dict = [
            {
                "code": vo.code, 
                "image": vo.image, 
                "item_name": vo.item_name, 
                "price": vo.price
            } for vo in reco_items
        ]
        return jsonify(reco_dict)
    
    return jsonify(reco_dict)

    

# 구매내역 분석 시각화
@app.route("/mixed.do")
def mixed() :
    id = session["login"]["id"] 
    
    dao = RecommendDAO()
    items = dao.GetChartData(id)
    dict_list = [
        {
            "item_name": vo.item_name, 
            "freq": vo.count, 
            "qty": vo.qty
        } for vo in items
    ]
    
    return jsonify(dict_list)

# 로그인 시 장바구니에 담긴 상품 갯수 조회를 헤더에 항상 표시하기 위한 함수
# @app.context_processor -> 공통 데이터 담당 (항상 표시해야될 데이터에 사용)
@app.context_processor
def info() :
    login_info = session.get("login")
    id = login_info.get("id") if login_info else None
    
    cart_dao = CartDAO()
    cart_data = cart_dao.GetList(id) if id else []
    
    return dict(cart={'cnt': len(cart_data)})
    
# main 함수
if __name__ == "__main__" :
    app.run(port=8000)