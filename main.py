from flask import Flask, request, redirect, render_template, session
from datetime import timedelta
import user_db as db

app = Flask(__name__, static_url_path='')
app.secret_key = '1145141919810'  # 对用户信息加密

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)  # 生成过期日期


@app.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    islogin = request.form.get('login')
    print(user, pwd, islogin)
    if islogin is not None:
        if db.password_check(user, pwd):
            session['username'] = user
            return redirect('/')
        else:
            return render_template('login.html', login_msg='用户名或密码输入错误')
    else:
        res = db.creat_user(user, pwd)
        if res:
            return render_template('login.html', sign_msg='注册成功！')
        else:
            return render_template('login.html', sign_msg='用户已被注册！')


@app.route('/new', methods=['GET', "POST"])
def IndexNew():
    return render_template('index.html')


@app.route('/', methods=['GET', "POST"])
def Index():
    username = session.get('username')
    if username:
        return render_template('index1.html', msg='你好! 用户：' + username)
    return render_template('index1.html', msg='你好路人！ 你还未登录！')


@app.route('/logout')
def LogOut():
    if session.get('username'):
        del session['username']
    return redirect('/')


@app.route('/LoginError')
def LoginError():
    return render_template('LoginError.html', error=1)


@app.route('/test')
def Test():
    username = session.get('username')
    if not username:
        return LoginError()
    return render_template('temp.html', username = username)


if __name__ == "__main__":
    app.run("0.0.0.0", 80, threaded=True, debug=True)
