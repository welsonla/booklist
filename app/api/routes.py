import re

from sqlalchemy import func

from app.api import bp
from flask import Flask, jsonify, request
from app.extensions import db
from app.models.access_token import AccessToken
from app.models.user import User, UserSchema
from app.extensions import result, search
from app.models.book import Book, BookSchema
from app.models.note import Note, NoteSchema
from app.models.quote import Quote, QuoteShema
from app.models.review import Review, ReviewShema
from app.models.collect import Collect, CollectShema, CollectBooks
from app.models.favorite import Favorite, FavoriteSchema
from app.functions import get_userid_by_sign
from sqlalchemy.exc import SQLAlchemyError
import math
import uuid
from lxml.html import fromstring


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
        user.email = params["email"]
        user.nickname = username
        user.password_hash = user.encode_password(params["password"])
        db.session.add(user)
        db.session.commit()
        return result(1000, '注册成功', {})


@bp.route('/home', methods=["post"])
def home():
    """获取首页数据"""
    hotbooks = Book.query.order_by(Book.like_count.desc(),Book.rating.desc()).limit(6).all()
    bookSchema = BookSchema(many=True)
    bookDict = bookSchema.dump(hotbooks)

    notes = Note.query.order_by(Note.id.desc()).limit(5).offset(0).all()
    noteSchema = NoteSchema(many=True)
    noteDict = noteSchema.dump(notes)

    reviews = Review.query.order_by(Review.id.desc()).limit(5).offset(0).all()
    reviewShema = ReviewShema(many=True)
    reviewDict = reviewShema.dump(reviews)

    collections = Collect.query.order_by(Collect.is_recommand.desc(), Collect.like_count.desc()).limit(8).all()
    collectShema = CollectShema(many=True)
    collectDict = collectShema.dump(collections)

    categories = db.session.query(Book.category, db.func.count(Book.category)).group_by(Book.category).all()
    categorie_dict = []

    for (category, count) in categories:
        categorie_dict.append({'title': category, 'count': count})

    params = {
        "hotbooks": bookDict,
        "collections": collectDict,
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
    for q in quotes:
        if q.comment is not None:
            q.comment = fromstring(q.comment).text_content()
    quoteShema = QuoteShema(many=True)
    quoteDict = quoteShema.dump(quotes)
    bookDict["quotes"] = quoteDict

    ### 查询书评
    reviews = Review.query.filter_by(book_id=book.id).limit(3).offset(0).all()
    for r in reviews:
        if r.content is not None:
            r.content = fromstring(r.content).text_content()
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
        book_id = params["bookid"]
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
        # print("未找到用户")
        return result(1003, '用户未登录')


@bp.route('/user/<int:id>', methods=('POST',))
def user(id):
    user = User.query.get(id)
    if user is not None:
        userShema = UserSchema()
        dict = userShema.dump(user)

        # 加载收藏
        favorite_count = Favorite.query.filter_by(author_id=id).count()
        dict["favorite_count"] = favorite_count

        # 加载用户笔记
        quotePage = Quote.query.filter_by(user_id=id).paginate(page=1, per_page=5)
        noteShema = QuoteShema(many=True)
        noteArray = noteShema.dump(quotePage.items)
        dict["notes"] = noteArray

        # 加载书单
        # collects = Collect.query.filter_by(author_id=id).limit(5).all()
        # collectShema = CollectShema(many=True)
        # collectArray = collectShema.dump(collects)
        reviews = Review.query.filter_by(author_id=id).limit(5).all()
        reviewShema = ReviewShema(many=True)
        reviewArray = reviewShema.dump(reviews)
        dict["reviews"] = reviewArray

        return result(1000, '', dict)
    return result(1005, '用户信息不存在', [])

@bp.route('/book/note/list', methods=['POST'])
def quote_list():
    """笔记列表"""
    jsonData = request.get_json()
    book_id = jsonData['bookid']
    user_id = jsonData['userid']
    page = jsonData["p"]
    print(f"bookid:${book_id} -- user_id:${user_id} --- ${page}")
    pageInfo = Quote.query.filter(Quote.book_id == book_id,Quote.user_id == user_id, Quote.content.isnot(None)).paginate(page=int(page), per_page=10)
    total = pageInfo.pages
    listArray = pageInfo.items

    user = User.query.filter_by(id=user_id).first()
    userShema = UserSchema()
    userDict = userShema.dump(user)

    shema = QuoteShema(many=True)
    dict = {}
    dict["total"] = total
    dict["page"] = page
    dict["total_items"] = pageInfo.total
    dict["list"] = shema.dump(listArray)
    dict["user"] = userDict


    return result(1000, '', dict)

@bp.route('/book/quote/<int:id>', methods=['POST'])
def quote_detail(id):
    quote = Quote.query.get(id)
    quoteSchema = QuoteShema()
    dict = quoteSchema.dump(quote)
    return result(1000, '', dict)


@bp.route('/book/note/wechat/import', methods=['POST'])
def note_wechat_import():
    """导入微信读书笔记"""
    jsonData = request.get_json()
    content = jsonData.get('content')
    book_id = jsonData.get('bookid')

    sign = request.headers.get('sign')
    author_id = get_userid_by_sign(sign)
    print(f"图书id:${book_id} --- 作者Id:${author_id}")
    try:
        # 按章节拆分数据
        chapters = content.split("◆")
        print(f"章节条数:${len(chapters)}")
        for chapter in chapters:
            # 拆分标注条目
            noteArray = chapter.split("\n")
            # 第一行数据为章节名称
            chapter_name = noteArray[0].replace("◆", "")
            print(f"章节名:${chapter_name}")
            # 解析标注条目
            for note in noteArray[1:]:
                # 检查标注中是否包含个人笔记
                lines = note.splitlines()
                print(f"笔记条数:${len(lines)}")
                if len(lines) > 0:
                    note = parse_note(lines, chapter_name, book_id, author_id, 1)
                    db.session.add(note)
            # 保存变更
        db.session.commit()
    except SQLAlchemyError as e:
        return result(1010, '数据库操作失败')
    return result(1000, '导入成功', [])


def parse_note(lines, chapter_name, book_id, author_id, source):
    print(f"lines:${lines} --- 章节:${chapter_name} --- 图书Id:${book_id} --- 作者Id:${author_id}")
    quote = Quote()
    for line in lines:
        quote.chapter = chapter_name
        quote.book_id = book_id
        quote.user_id = author_id
        quote.source = source
        if re.match(r"\d{4}/\d{1,2}/\d{1,2}", line):
            continue
        elif line.startswith(">>"):
            # 标注内容
            quote.content = line.replace(">>", "")
        else:
            # 个人笔记
            quote.comment = line
    return quote


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
    return result(1000, '', dict)


@bp.route('/book/review/<int:id>', methods=["POST"])
def review_detail(id):
    """获取书评"""
    review = Review.query.get(id)
    reviewShema = ReviewShema()
    dict = reviewShema.dump(review)
    return result(1000, '', dict)


@bp.route("/book/collect/create", methods=['POST'])
def collect_create():
    """创建书单"""
    # 获取请求中的json映射成实体
    sign = request.headers.get('sign')
    # print(f"sign:${sign}")
    author_id = get_userid_by_sign(sign)

    jsonData = request.get_json()

    books = jsonData.get("list")
    collectShema = CollectShema()
    # collect = collectShema.load(jsonData, many=False)

    collect = Collect()
    collect.name = jsonData["name"]
    collect.content = jsonData["content"]
    collect.author_id = author_id
    collect.cover_url = books[0]["image_url"]
    db.session.add(collect)
    db.session.commit()

    # 添加关联图书
    for book in books:
        bookItem = CollectBooks()
        bookItem.book_id = book["id"]
        bookItem.collect_id = collect.id
        bookItem.content = book["title"]
        db.session.add(bookItem)

    db.session.commit()
    # 返回创建成功的书单
    collectDict = collectShema.dump(collect)
    # print(f"collect:${result}")
    return result(1000, '书单创建成功', collectDict)

@bp.route('/collect/<int:id>', methods=['POST'])
def collect_detail(id):
    """获取书单详情"""
    collect = Collect.query.get(id)
    books = []
    if collect is not None:
        relations = CollectBooks.query.filter_by(collect_id=id).all()
        # print(f"relations:${len(relations)}")
        for r in relations:
            book = Book.query.filter_by(id=r.book_id).first()
            # print(f"book.name:${book.name}")
            books.append(book)

    collectShema = CollectShema()
    dict = collectShema.dump(collect)

    bookSchema = BookSchema(many=True)
    list = bookSchema.dump(books)

    dict["books"] = list
    # print(f"dict:${dict}")
    # print(f"books:${len(books)}")
    return result(1000, '', dict)

@bp.route('/logout', methods=['POST'])
def logout():
    """退出登录，清理本地用户信息"""
    return ""


@bp.route('/book/comment', methods=['POST'])
def comment():
    return ""

@bp.route('/favorite/get', methods = ['POST'])
def favorite_detail():
    """获取用户收藏"""
    # 获取请求中的json映射成实体
    sign = request.headers.get('sign')
    author_id = get_userid_by_sign(sign)
    jsonData = request.get_json()
    type_id = jsonData.get('type')
    item_id = jsonData.get('item_id')
    # print(f"type_id:${type_id} -- item_id:{item_id} -- author_id:${author_id}")
    favorite = Favorite.query.filter_by(type=type_id, item_id=int(item_id), author_id=author_id).first()
    if favorite is not None:
        favoriteShema = FavoriteSchema()
        dict = favoriteShema.dump(favorite)
        return result(1000, '收藏添加成功', dict)
    return result(1008, "收藏的内容不存在", None)

@bp.route('/favorite/add', methods=['POST'])
def favorite_add():
    """用户添加收藏"""
    # 获取请求中的json映射成实体
    sign = request.headers.get('sign')
    author_id = get_userid_by_sign(sign)
    jsonData = request.get_json()
    type_id = jsonData.get('type')
    item_id = jsonData.get('item_id')
    content =  checkContent(type_id, item_id)
    if content is not None:
        favorite = Favorite()
        favorite.type = type_id
        favorite.item_id = item_id
        favorite.author_id = author_id
        db.session.add(favorite)
        # 更新收藏次数
        if type_id == 1:
            content.like_count = content.like_count + 1
        elif type_id == 2:
            content.like_count = content.like_count + 1
        elif type_id == 3:
            content.like_count = content.like_count + 1
        elif type_id == 4:
            content.favorite_count = content.favorite_count + 1
        db.session.commit()
        favoriteShema = FavoriteSchema()
        dict = favoriteShema.dump(favorite)
        return result(1000, '收藏添加成功', dict)
    return result(1008, "收藏的内容不存在", None)

@bp.route('/favorite/del', methods = ['POST'])
def favorite_del():
    """创建书单"""
    # 获取请求中的json映射成实体
    sign = request.headers.get('sign')
    author_id = get_userid_by_sign(sign)
    jsonData = request.get_json()
    type_id = jsonData.get('type')
    item_id = jsonData.get('item_id')
    favorite = Favorite.query.filter_by(type=type_id, item_id=item_id, author_id=author_id).first()
    if favorite is not None:
        db.session.delete(favorite)
        content = checkContent(type_id, item_id)
        if type_id == 1:
            content.like_count = content.like_count - 1
        elif type_id == 2:
            content.like_count = content.like_count - 1
        elif type_id == 3:
            content.like_count = content.like_count - 1
        elif type_id == 4:
            content.favorite_count = content.favorite_count - 1
        db.session.commit()
        return result(1000, '取消收藏成功', [])
    return result(1020, '取消收藏失败', [])

@bp.route('/favorite/list', methods=['POST'])
def favorite_list():
    sign = request.headers.get('sign')
    author_id = get_userid_by_sign(sign)
    jsonData = request.get_json()
    type_id = jsonData.get('type_id')

    list_result = db.session.query(Favorite.type, func.count(Favorite.type).label('c')).filter(Favorite.author_id == author_id).group_by(Favorite.type).all()

    count_dict = []
    print(f"list_result:{list_result}")
    for item in list_result:
        count_dict.append({'type': item[0], 'count': item[1] })

    result_dict = {}
    item_array = []
    favorite_list = Favorite.query.with_entities(Favorite.item_id).filter_by(author_id=author_id, type=type_id).all()
    for fav in favorite_list:
        item_array.append(fav.item_id)
    print(f"favorite_list:{item_array}")
    if type_id == 1:
        books = Book.query.filter(Book.id.in_(item_array)).all()
        shema = BookSchema(many=True)
        dict = shema.dump(books)
        result_dict["list"] = dict
    elif type_id == 2:
        collects = Collect.query.filter(Collect.id.in_(item_array)).all()
        shema = CollectShema(many=True)
        dict = shema.dump(collects)
        result_dict["list"] = dict
    elif type_id == 3:
        reviews = Review.query.filter(Review.id.in_(item_array)).all()
        for r in reviews:
            r.content = fromstring(r.content).text_content()
        shema = ReviewShema(many=True)
        dict = shema.dump(reviews)
        result_dict["list"] = dict
    elif type_id == 4:
        notes = Quote.query.filter(Quote.id.in_(item_array)).all()
        # for r in notes:
        #     if r.comment is not None:
        #         r.comment = fromstring(r.comment).text_content()
        shema = ReviewShema(many=True)
        dict = shema.dump(notes)
        # print(f"dict:{dict}")
        result_dict["list"] = dict

    result_dict["counts"] = count_dict
    return result(1000, '', result_dict)
def checkContent(type_id, item_id):
    """检查收藏内容是否存在"""
    # print(f"type:id${type_id} -- item_id:${item_id}")
    if type_id == 1:
        # 图书
        return Book.query.get(item_id)
    elif type_id == 2:
        # 书单
        return Collect.query.get(item_id)
    elif type_id == 3:
        # 书评
        return Review.query.get(item_id)
    elif type_id ==4:
        # 笔记
        return Quote.query.get(item_id)

@bp.route('/collect/getList', methods=['POST'])
def getMineCollect():
    sign = request.headers.get('sign')
    # print(f"sign:${sign}")
    author_id = get_userid_by_sign(sign)
    collections = Collect.query.filter_by(author_id=author_id).all()
    collectShema = CollectShema(many=True)
    dict = collectShema.dump(collections)
    return result(1000, '获取书单成功', dict)

@bp.route('/search', methods=['POST'])
def full_text_search():
    """全文搜索"""
    keyword = request.get_json().get('q')
    page = request.get_json().get('p') or 1
    results = search.msearch(Book, query=keyword, fields=['name', 'isbn', 'author', "desc"])
    sourceArray = []
    for book in results:
        hitDict = {
            "title": book["name"],
            "author": book["author"],
            "id": book["id"],
            "content": book["desc"],
            "image_url": book["image_url"]
        }
        sourceArray.append(hitDict)
        # print(f"book.name:{book} --- {type(book)} --- {book.score} --- {book.rank} ")
    pagination = paginate(sourceArray, page=page, per_page=20)
    return result(1000, "", pagination)


def paginate(dataArray=[], page=1, per_page=20):
    # 总页数
    total = math.ceil(len(dataArray) / 20)
    # 起始索引
    offset = (page - 1) * per_page
    # 结束索引
    end = offset + per_page
    if len(dataArray) < end:
        end = offset + len(dataArray) % per_page
    # 当页数据
    list = dataArray[offset:end]
    return {
        "total_page": total,
        "total_count":len(dataArray),
        "start": offset,
        "end": end,
        "list": list
    }
