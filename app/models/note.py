from app.extensions import db, ma
from sqlalchemy import ForeignKey
from app.models.book import Book
from app.models.user import User
from datetime import datetime
from marshmallow import Schema, fields


class Note(db.Model):
    """读书笔记"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), comment='标题')
    content = db.Column(db.Text, comment='内容')
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment='书籍id')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='用户Id')
    like_count = db.Column(db.Integer,  comment='点赞数量')
    visit_count = db.Column(db.Integer, comment='浏览量')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note