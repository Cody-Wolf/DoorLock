from flask import Flask, request, redirect, render_template, session
from datetime import timedelta
import user_db as db

app = Flask(__name__, static_url_path='')
app.secret_key = '1145141919810'  # 对用户信息加密

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)  # 生成过期日期


@app.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')
    name = request.form.get('user')
    pwd = request.form.get('pwd')
    is_login = request.form.get('login')
    print(name, pwd, is_login)
    if is_login is not None:
        if db.password_check(db.User(Name=name, Pwd=pwd)):
            session['username'] = name
            return redirect('/')
        else:
            return render_template('login.html', login_msg='用户名或密码输入错误')
    else:
        res = db.creat_user(db.User(Name=name, Pwd=pwd))
        if res:
            return render_template('login.html', sign_msg='注册成功！')
        else:
            return render_template('login.html', sign_msg='用户已被注册！')


@app.route('/new')
def newIndex():
    return render_template('index.html')


@app.route('/')
def index():
    username = session.get('username')
    if username:
        return render_template('index1.html', msg='你好! 用户：' + username)
    return render_template('index1.html', msg='你好路人！ 你还未登录！')


@app.route('/logout')
def LogOut():
    if session.get('username'):
        del session['username']
    return redirect('/')


@app.route('/loginError')
def loginError():
    return render_template('loginError.html', error=1)


@app.route('/deviceManage', methods=['GET', "POST"])
def deviceManage():
    username = session.get('username')
    if not username:
        return loginError()
    user = db.find_user(username)
    if request.method == 'POST':
        val = request.form.get('manage')
        if val:
            msg = "你选择了设备：" + str(val)

        val = request.form.get('delete')
        if val:
            res = db.del_device(user, db.Device(val))
            if res:
                msg = "成功删除设备：" + str(val)
            else:
                msg = "删除以下设备失败：" + str(val)

        val = request.form.get('new')
        if val:
            res = db.add_device(user, db.Device(val))
            if res:
                msg = "成功添加设备：" + str(val)
            else:
                msg = "添加以下设备失败：" + str(val)
    device = user.device_list
    device_count = len(device)
    return render_template('deviceManage.html', **locals())


@app.route('/userManage', methods=['GET', "POST"])
def userManage():
    username = session.get('username')
    if not username:
        return loginError()


if __name__ == "__main__":
    app.run("0.0.0.0", 80, threaded=True, debug=True)
