from app.extensions import db, ma
from datetime import datetime
from marshmallow import Schema, fields
from app.models.user import User, UserSchema
from app.models.book import BookSchema

class Quote(db.Model):
    """图书摘录"""

    # 搜索字段
    __searchable__ = ['chapter', 'content', 'comment']

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment='图书id')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='作者id')
    chapter = db.Column(db.String, comment='章节')
    page = db.Column(db.Integer, default=0, comment='页码')
    content = db.Column(db.Text, comment='摘抄')
    comment = db.Column(db.Text, comment='点评')
    is_recommand = db.Column(db.Integer, nullable=False, default=0, comment="推荐状态")
    favorite_count = db.Column(db.Integer, nullable=True, default=0, comment="收藏数量")
    state = db.Column(db.Integer, default=1, comment='0删除,1正常')
    source = db.Column(db.Integer, default=0, comment="数据来源,0 手动录入 1 微信 2 kindle")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #  关联User
    user = db.relationship('User')
    book = db.relationship('Book', backref=db.backref("quotes", lazy='select')) # backref=db.backref("quotes", lazy="dynamic")

class QuoteShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quote
        include_fk = True

    created_at = fields.DateTime(('%Y-%m-%d %H:%M:%S'))
    updated_at = fields.DateTime(('%Y-%m-%d %H:%M:%S'))

    # 过滤字段
    user = fields.Nested(UserSchema, only=("id", "name", "nickname", "state"))
    book = fields.Nested(BookSchema, only=("id", "name", "cover_url", "author"))