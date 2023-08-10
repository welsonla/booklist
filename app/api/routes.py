from app.api import bp
from flask import Flask, jsonify, request
from app.extensions import db
from app.models.user import User, UserSchema
from app.models.access_token import AccessToken
from app.extensions import result, sqlalchemy_to_json
import uuid

@bp.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    username = params["username"]
    password = params['password']
    u = User.query.filter_by(name=username).first()
    if u != None:
        if u.valid_password(password):
            access_token = AccessToken()
            access_token.userid = u.id
            access_token.token = str(uuid.uuid4())
            db.session.add(access_token)
            db.session.commit()

            schema = UserSchema()
            dict = schema.dump(u)
            return result(1000, "登录成功", dict)
        else:
            return result(1002, "密码验证失败")
    else:
        return result(1003, "用户不存在")
    return result(1004, "登录失败")

@bp.route("/register", methods=["POST"])
def register():
    params = request.get_json()
    # print("data")
    username = params["username"]
    u = User.query.filter_by(name=username).first()
    if u != None:
        return result(code=1001, message="用户名已经存在")
    else:
        user = User()
        user.name = username
        user.role = 3
        user.email = 'wyc.jar@gmail.com'
        user.nickname = 'ssssyyyy'
        user.password_hash = user.encode_password('111111')
        db.session.add(user)
        db.session.commit()
    return f"{params['username']}"


@bp.route('/logout', methods=['POST'])
def logout():
    return ""


@bp.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
    return ""


@bp.route('/book/comment', methods=['POST'])
def comment():
    return ""
