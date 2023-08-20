from app.api import bp
from flask import Flask, jsonify, request
from app.extensions import db
from app.models.user import User, UserSchema
from app.models.access_token import AccessToken
from app.extensions import result, sqlalchemy_to_json
from app.models.book import Book, BookSchema
from app.models.note import Note, NoteSchema
from app.models.quote import Quote, QuoteShema
import uuid


@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    params = request.get_json()
    username = params["username"]
    password = params['password']
    u = User.query.filter_by(name=username).first()
    if u is not None:
        if u.valid_password(password):
            token = str(uuid.uuid4())
            access_token = AccessToken.query.filter_by(userid=u.id).first()
            if access_token is None:
                access_token = AccessToken()
            access_token.userid = u.id
            access_token.token = token
            db.session.add(access_token)
            db.session.commit()

            schema = UserSchema()
            dict = schema.dump(u)
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
    print(f"hotbooks.count{len(hotbooks)}")
    print(f"hotbooks:{dict}")

    notes = Note.query.order_by(Note.like_count.desc()).limit(5).all()
    noteSchema = NoteSchema(many=True)
    noteDict = noteSchema.dump(notes)
    print(f"notelist.count:{len(notes)}")

    categories = db.session.query(Book.category, db.func.count(Book.category)).group_by(Book.category).all()
    categorie_dict = []
    print(categories)
    for (category, count) in categories:
        print(f"{category}----{count}")
        categorie_dict.append({'title': category, 'count': count})
    print(categorie_dict)

    params = {
        "hotbooks": bookDict,
        "booklist": [],
        "notelist": noteDict,
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

    print(f"quotes.count:{len(quotes)}")
    print(f"book.dict:{bookDict}")
    print(f"book.notes:{book.quotes}")
    return result(1000, '', bookDict)


@bp.route('/book/quote/create', methods=['POST'])
def quote_create():
    """发表摘抄与评论"""
    # 获取登录用户的cookie标识
    sign = request.headers.get('sign')
    print(f"sign:{sign}")
    print(f"headers:{request.headers}")
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
        print(f"发表成功:{dict}")
        return result(1000, '', dict)
    else:
        print("未找到用户")
        return result(1003, '用户未登录')


@bp.route('/book/quote/<int:id>', methods=['POST'])
def quote_detail(id):
    quote = Quote.query.get(id)
    quoteSchema = QuoteShema()
    dict = quoteSchema.dump(quote)
    return result(1000, '', dict)


@bp.route('/logout', methods=['POST'])
def logout():
    """退出登录，清理本地用户信息"""
    return ""


@bp.route('/book/comment', methods=['POST'])
def comment():
    return ""
