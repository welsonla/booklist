from app.extensions import db
import datetime


class Quote(db.Model):
    """图书摘录"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, comment='图书id')
    user_id = db.Column(db.Integer, comment='作者id')
    chapter = db.Column(db.String, comment='章节')
    page = db.Column(db.Integer, default=0, comment='页码')
    content = db.Column(db.Text, comment='摘抄')
    comment = db.Column(db.Integer, comment='点评')
    state = db.Column(db.Integer, default=1, comment='0删除,1正常')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)