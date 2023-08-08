from app.api import bp
from flask import Flask, jsonify, request
from app.extensions import db
from app.models.user import User
from app.extensions import result


@bp.route('/login', methods=['POST'])
def login(username, password):
    return ""

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
