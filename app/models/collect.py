from app.extensions import db, ma
from datetime import datetime
from marshmallow import Schema, fields, post_load
from app.models.user import UserSchema

# collect_book_table = db.Table(
#     "collect_book",
#     db.Column("collect_id", db.Integer, db.ForeignKey("collect.id"), primary_key=True),
#     db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
#     db.Column("content", db.Text, nullable=True, comment="图书评价"),
#     db.Column("created_at", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间"),
#     db.Column("updated_at", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
# )

class CollectBooks(db.Model):
    """书单与图书关联表"""
    id = db.Column(db.Integer, primary_key=True)
    collect_id = db.Column(db.Integer, comment="外键，书单Id")
    book_id = db.Column(db.Integer, comment="外键，图书Id")
    content = db.Column(db.Text, nullable=True, comment="图书评价")
    created_at =  db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

class Collect(db.Model):
    # 搜索字段
    __searchable__ = ['name', 'content']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), comment="书单名")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"),comment="外键, 作者Id")
    content = db.Column(db.Text, comment="书单简介")
    like_count = db.Column(db.Integer, default=0, comment="点赞数量")
    visit_count = db.Column(db.Integer, default=0, comment="浏览量")
    is_recommand = db.Column(db.Integer, nullable=False, default=0, comment="推荐状态")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # books = db.relationship("Book", secondary="collect_book")

    author = db.relationship('User', backref='collects')

class CollectShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Collect
        include_fk = True

    @post_load
    def make_review(self, data, **kwargs):
        return Collect(**data)

    author = fields.Nested(UserSchema, only=("id", "name", "nickname", "state"))