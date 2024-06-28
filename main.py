import secrets
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, request, render_template, url_for, redirect, flash


# __init__
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請登入成為鱷魚的一份子'

users = {'Me': {'password': ''}}


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(使用者):
    # 1. Fetch against the database a user by `id`
    if 使用者 not in users:
        return  render_template("wrong.html")

    # 2. Create a new object of `User` class and return it.
    user = User()
    user.id = 使用者
    return user

# 檢查是否是正確的使用者與密碼?
@login_manager.request_loader
def request_loader(request):
    使用者 = request.form.get('user_id')
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[使用者]['password']

    return user

@app.route('/')
def Home():
    return render_template("Login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("Login.html")

    key_id = request.form['user_id']
    if (key_id in users) and (request.form['password'] == users[key_id]['password']):
        user = User()
        user.id = key_id
        login_user(user)
        flash(f'{key_id}！歡迎加入鱷魚的一份子！')
        return redirect(url_for('from_start'))

    flash('登入失敗了...')
    return render_template('Login.html')

@app.route('/logout')
def logout():
    使用者 = current_user.get_id()
    logout_user()
    flash(f'{使用者}！歡迎下次再來！')
    return render_template('login.html')

@app.route('/from_start', methods=['GET', 'POST'])
@login_required
def from_start():
    return render_template('welcome.html')

@app.route("/show_records")
@login_required
def show_records():
    return render_template("Member.html")

if __name__ == '__main__':
    app.run()

