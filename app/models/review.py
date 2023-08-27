from app.extensions import db, date_style
from marshmallow import Schema, fields, post_load
from datetime import datetime
from app.models.user import UserSchema
from app.models.book import BookSchema

class Review(db.Model):
    """书评"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment="图书id")
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment="作者id")
    rating = db.Column(db.Float, default=0.0, comment="评分")
    title = db.Column(db.String, default='', comment="标题")
    content = db.Column(db.Text, nullable=True, comment="书评内容")
    like_count = db.Column(db.Integer, default=0, comment="喜欢次数")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow)

    author = db.relationship('User', back_populates='reviews')
    book = db.relationship('Book', back_populates='reviews')

class ReviewShema(Schema):
    id = fields.Int()
    book_id = fields.Int()
    author_id = fields.Int()
    rating = fields.Float()
    title = fields.Str()
    content = fields.Str()
    like_count = fields.Int()
    created_at = fields.DateTime(date_style)
    updated_at = fields.DateTime(date_style)

    author = fields.Nested(UserSchema, only=("id", "name", "nickname", "state",))
    book = fields.Nested(BookSchema, only=("id","name", "image_url"))
    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)
