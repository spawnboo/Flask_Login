import secrets
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, request, render_template, url_for, redirect, flash,session

from RegisterEmail import Register_Function

# __init__
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.session_protection = "strong"
login_manager.login_view = 'login'      # 登入要轉至登入的路由
login_manager.login_message = '請登入成為鱷魚的一份子'


# 載入使用者資料庫 or 清單
users = {'Me': {'password': '123'}}


# 繼承 UserMinin 物件
class Member(UserMixin):
    pass

# 檢查是否是正確的使用者與密碼?  與request_loader 一起需要做
@login_manager.user_loader
def user_loader(使用者):
    # 1. Fetch against the database a user by `id`
    if 使用者 not in users:
        return  render_template("wrong.html")

    # 2. Create a new object of `User` class and return it.
    member = Member()
    member.id = 使用者

    return member

# # 檢查是否是正確的使用者與密碼? 與user_loader 一起需要做
# @login_manager.request_loader
# def request_loader(request):
#     使用者 = request.form.get('user_id')
#     if 使用者 not in users:
#         return
#
#     member = Member()
#     member.id = 使用者
#     member.is_authenticated = 使用者.form['password'] == users[使用者]['password']
#     print("B member.is_authenticated" + member.is_authenticated)
#     return member

@app.route('/')
def Home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 更新使用者的資料庫應該在這邊, 再user_loader or request_loader 方法裡,會浪費太多資源!

    if request.method == 'GET':
        return render_template("LoginPage.html")

    key_id = request.form['user_id']

    print(users)

    if (key_id in users) and (request.form['password'] == users[key_id]['password']):
        member = Member()
        member.id = key_id
        login_user(member)
        flash(f'{key_id}！歡迎加入鱷魚的一份子！')
        return redirect(url_for('from_start'))

    flash('登入失敗了...')
    return 'bad login'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        session['Register_user'] = ''
        session['Register_password']   = ''
        session['Register_email'] = ''
        return render_template("Register.html")


    key_id = request.form['user_id']
    if key_id in users:
        flash("使用者已經被使用,請更換使用者名稱!")
        error_text = "使用者已經被使用!"
        return render_template("Register.html", note_text=error_text)

    # 可以使用的帳號
    else:
        # users[key_id] = {'password':request.form['password']}

        session['Register_user'] = request.form['user_id']
        session['Register_password']   = request.form['password']
        session['Register_email'] = request.form['email']

        return redirect(url_for('register_verify'))

    flash('註冊發生錯誤...')
    return 'bad register...'

@app.route('/register_verify', methods=['GET', 'POST'])
def register_verify():
    if request.method == 'GET':
        session['varify_code'] = Register_Function(session['Register_email'])
        return render_template("RegisterCheck.html")

    key_varify = request.form['verify_code']
    if key_varify == session['varify_code']:
        users[session['Register_user']] = {'password':session['Register_password']}

        # flash("註冊成功! 請重新登入")
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    使用者 = current_user.get_id()
    logout_user()
    flash(f'{使用者}！歡迎下次再來！')
    return render_template('LoginPage.html')

@app.route('/from_start')
@login_required
def from_start():
    return render_template('welcome.html')

@app.route("/show_records")
@login_required
def show_records():
    return render_template("Member.html")

# ==============================================註冊頁面與相關辦法========================================================


if __name__ == '__main__':
    app.debug = True
    app.run()

