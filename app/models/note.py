from app.extensions import db
from sqlalchemy import ForeignKey
from app.models.book import Book
from app.models.user import User
import datetime

class Note(db.Model):
    """读书笔记"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), comment='标题')
    content = db.Column(db.Text, comment='内容')
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment='书籍id')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='用户Id')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')