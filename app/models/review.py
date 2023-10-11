from app.extensions import db, date_style, ma
from marshmallow import Schema, fields, post_load
from datetime import datetime
from app.models.user import UserSchema
from app.models.book import BookSchema

class Review(db.Model):
    """书评"""
    # 搜索字段
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), comment="图书id")
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment="作者id")
    rating = db.Column(db.Float, default=0.0, comment="评分")
    title = db.Column(db.String, default='', comment="标题")
    content = db.Column(db.Text, nullable=True, comment="书评内容")
    like_count = db.Column(db.Integer, default=0, comment="喜欢次数")
    is_recommand = db.Column(db.Integer, nullable=False, default=0, comment="推荐状态")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow)

    author = db.relationship('User', backref='reviews')
    book = db.relationship('Book', backref='reviews')

class ReviewShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True

    # 输出关联Model
    author = fields.Nested(UserSchema, only=("id", "name", "nickname", "state",))
    book = fields.Nested(BookSchema, only=("id","name", "image_url"))

    created_at = fields.DateTime(date_style)
    updated_at = fields.DateTime(date_style)

    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)
