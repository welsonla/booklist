from app.extensions import db
from datetime import datetime
from marshmallow import Schema, fields
from app.models.user import User, UserSchema
from app.models.book import BookSchema

class Quote(db.Model):
    """图书摘录"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment='图书id')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='作者id')
    chapter = db.Column(db.String, comment='章节')
    page = db.Column(db.Integer, default=0, comment='页码')
    content = db.Column(db.Text, comment='摘抄')
    comment = db.Column(db.Integer, comment='点评')
    state = db.Column(db.Integer, default=1, comment='0删除,1正常')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #  关联User
    # user = db.relationship('User')
    # book = db.relationship('Book', backref=db.backref("quotes", lazy='select')) # backref=db.backref("quotes", lazy="dynamic")

class QuoteShema(Schema):
    id = fields.Int()
    book_id = fields.Int()
    user_id = fields.Int()
    chapter = fields.Str()
    page = fields.Int()
    content = fields.Str()
    comment = fields.Str()
    state = fields.Int()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    # 过滤字段
    user = fields.Nested(UserSchema, only=("id", "name", "nickname", "state",))
    book = fields.Nested(BookSchema, only=("id", "name", "cover_url", "author"))