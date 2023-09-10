from app.extensions import db
from datetime import datetime
from marshmallow import Schema, fields

collect_book_table = db.Table(
    "collect_book",
    db.Column("collect_id", db.Integer, db.ForeignKey("collect.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("content", db.Text, nullable=True, comment="图书评价"),
    db.Column("created_at", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间"),
    db.Column("updated_at", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
)

class Collect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), comment="书单名")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"),comment="外键, 作者Id")
    content = db.Column(db.Text, comment="书单简介")
    like_count = db.Column(db.Integer, default=0, comment="点赞数量")
    visit_count = db.Column(db.Integer, default=0, comment="浏览量")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # books = db.relationship("Book", secondary="collect_book")

class CollectShema(Schema):
    id = fields.Int()
    name = fields.Str()
    author_id = fields.Int()
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

# class BookCollect(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     collect_id = db.Column(db.Ineteger, db.ForeignKey("collect.id"), comment="外键，书单Id")
#     book_id = db.Column(db.Integer, db.ForeignKey("book.id"), comment="外键，图书Id")
#     content = db.Column(db.Text, nullable=True, comment="图书评价")
#     created_at = db.Column(db.Datetime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间")
#     updated_at = db.Column(db.Datetime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
