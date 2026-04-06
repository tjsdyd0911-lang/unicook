from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from modules.UserVO  import UserVO
from modules.UserDAO import UserDAO
from modules.ItemVO  import ItemVO
from modules.ItemDAO import ItemDAO

app = Flask(__name__)

app.secret_key = "unicook"

@app.route("/")
def main() :
    page = request.args.get("page", 1)
    category = request.args.get("category", "0")
    dao = ItemDAO()
    total, items = dao.GetList(page, category)
    return render_template("main.html", items = items)

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

#로그아웃 (/logout.do)
@app.route("/logout.do")
def logout() :
    session["login"] = None     
    return redirect("/")
@app.route("/view.do")
def view() :
    code = request.args.get("code","")
    if code == "":
        return redirect("/")
    dao = ItemDAO()
    item = dao.View(code,True)
    return render_template("view.html", item=item)

@app.route("/cart.do")
def cart() :
    return render_template("cart.html")

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