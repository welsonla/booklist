from app.api import bp
from flask import Flask, jsonify, request
from app.extensions import db
from app.models.access_token import AccessToken
from app.models.user import User, UserSchema
from app.extensions import result
from app.models.book import Book, BookSchema
from app.models.note import Note, NoteSchema
from app.models.quote import Quote, QuoteShema
from app.models.review import Review, ReviewShema
from app.functions import get_userid_by_sign

import uuid


@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    params = request.get_json()
    username = params["username"]
    password = params['password']
    user = User.query.filter_by(name=username).first()
    if user is not None:
        if user.valid_password(password):
            token = str(uuid.uuid4())
            access_token = AccessToken.query.filter_by(userid=user.id).first()
            if access_token is None:
                access_token = AccessToken()
            access_token.userid = user.id
            access_token.token = token
            db.session.add(access_token)
            db.session.commit()

            schema = UserSchema()
            dict = schema.dump(user)
            resp = {"user": dict, "sign": token}
            return result(1000, "登录成功", resp)
        else:
            return result(1002, "密码验证失败")
    else:
        return result(1003, "用户不存在")
    return result(1004, "登录失败")


@bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
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


@bp.route('/home', methods=["post"])
def home():
    """获取首页数据"""
    hotbooks = Book.query.order_by(Book.rating.desc()).limit(5).all()
    bookSchema = BookSchema(many=True)
    bookDict = bookSchema.dump(hotbooks)

    notes = Note.query.order_by(Note.id.desc()).limit(5).offset(0).all()
    noteSchema = NoteSchema(many=True)
    noteDict = noteSchema.dump(notes)

    reviews = Review.query.order_by(Review.id.desc()).limit(5).offset(0).all()
    reviewShema = ReviewShema(many=True)
    reviewDict = reviewShema.dump(reviews)

    categories = db.session.query(Book.category, db.func.count(Book.category)).group_by(Book.category).all()
    categorie_dict = []

    for (category, count) in categories:
        categorie_dict.append({'title': category, 'count': count})

    params = {
        "hotbooks": bookDict,
        "booklist": [],
        "notelist": noteDict,
        "reviews": reviewDict,
        "categories": categorie_dict
    }
    return result(1000, '', params)


@bp.route('/book/<int:id>', methods=['Post'])
def book(id):
    """获取图书详情"""
    book = Book.query.get(id)
    bookSchema = BookSchema(many=False)
    bookDict = bookSchema.dump(book)

    # 查询关联笔记
    quotes = Quote.query.filter_by(book_id=book.id).limit(3).offset(0).all()
    quoteShema = QuoteShema(many=True)
    quoteDict = quoteShema.dump(quotes)
    bookDict["quotes"] = quoteDict

    ### 查询书评
    reviews = Review.query.filter_by(book_id=book.id).limit(3).offset(0).all()
    revieShema = ReviewShema(many=True)
    reviewDict = revieShema.dump(reviews)
    bookDict["reviews"] = reviewDict

    return result(1000, '', bookDict)


@bp.route('/book/quote/create', methods=['POST'])
def quote_create():
    """发表摘抄与评论"""
    # 获取登录用户的cookie标识
    sign = request.headers.get('sign')
    # 查找登录用户信息
    token = AccessToken.query.filter_by(token=sign).first()
    if token is not None:
        params = request.get_json()
        book_id  = params["bookid"]
        chapter = params["chapter"]
        page = params["page"] or 0
        content = params["content"]
        comment = params["comment"] or ""

        quote = Quote()
        quote.book_id = book_id
        quote.chapter = chapter
        quote.page = page
        quote.content = content
        quote.comment = comment
        quote.user_id = token.userid
        db.session.add(quote)
        db.session.commit()

        quoteSchema = QuoteShema()
        dict = quoteSchema.dump(quote)
        return result(1000, '', dict)
    else:
        print("未找到用户")
        return result(1003, '用户未登录')


@bp.route('/user/<int:id>', methods=('POST',))
def user(id):
    user = User.query.get(id)
    userShema = UserSchema()
    dict = userShema.dump(user)

    notes = Quote.query.filter_by(user_id=id).limit(5).all()
    noteShema = QuoteShema(many=True)
    noteArray = noteShema.dump(notes)
    dict["notes"] = noteArray

    reviews = Review.query.filter_by(author_id=id).limit(5).all()
    reviewShema = ReviewShema(many=True)
    reviewArray = reviewShema.dump(reviews)
    dict["reviews"] = reviewArray

    return result(1000, '', dict)

@bp.route('/book/quote/<int:id>', methods=['POST'])
def quote_detail(id):
    quote = Quote.query.get(id)
    quoteSchema = QuoteShema()
    dict = quoteSchema.dump(quote)
    return result(1000, '', dict)


@bp.route('/book/review/create', methods=['POST'])
def review_ceate():
    """创建书评"""
    jsonBody = request.get_json()
    reviewShema = ReviewShema()
    data = reviewShema.load(jsonBody, many=False)
    data.author_id = 1
    db.session.add(data)
    db.session.commit()
    dict = reviewShema.dump(data)
    return result(1000, '', dict )

@bp.route('/book/review/<int:id>',methods=["POST"])
def review_detail(id):
    """获取书评"""
    review = Review.query.get(id)
    reviewShema = ReviewShema()
    dict = reviewShema.dump(review)
    return result(1000, '', dict)

@bp.route('/logout', methods=['POST'])
def logout():
    """退出登录，清理本地用户信息"""
    return ""


@bp.route('/book/comment', methods=['POST'])
def comment():
    return ""
