from app.extensions import db
from marshmallow import Schema, fields
from datetime import datetime


class Review(db.Model):
    """书评"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment="图书id")
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment="作者id")
    rating = db.Column(db.Float, default=0.0, comment="评分")
    content = db.Column(db.Text, nullable=True, comment="书评内容")
    like_count = db.Column(db.Integer, default=0, comment="喜欢次数")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow)


class ReviewShema(Schema):
    id = fields.Int()
    book_id = fields.Int()
    author_id = fields.Int()
    rating = fields.Float()
    content = fields.Str()
    like_count = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
