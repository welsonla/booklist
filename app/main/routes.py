from app.main import bp
from app.models.user import User
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user
from app.extensions import db
@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # # 插入admin用户
    # user = User(name='welsonla', email='wanyc@outlook', bio='Done is better then perfect.')
    # user.encode_password('QWERTY!@#')
    # db.session.add(user)
    # db.session.commit()
    # print('插入用户"welsonla"')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('请输入正确的用户名和密码')
            print("请输入正确的用户名和密码")
            return redirect(url_for('main.login'))

        user = User.query.filter_by(name=username).first()
        print(f"user:{user.name}")
        if username == user.name and user.valid_password(password):
            login_user(user)
            flash('登录成功')
            print("登录成功")
            # return redirect(url_for('dashboard.index'))
            return redirect('admin')
        flash('用户名或密码错误')
        print("用户名或密码错误")
        return redirect(url_for('main.login'))
    else:
        # GET 方法直接返回模板页面
        return render_template('login.html')