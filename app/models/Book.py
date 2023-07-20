from app import db
# from flask_sqlalchemy import Column,String,Integer,Text,Float,DateTime
import datetime
import flask_sqlalchemy as sa

class Book(db.Model):
    __tablename__='book'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), comment="书名")
    cover_url = sa.Column(sa.String(255), comment="封面")
    author = sa.Column(sa.String(50), comment="作者")
    price = sa.Column(sa.Float, default=0, comment="定价")
    desc = sa.Column(sa.Text, nullable=True, comment="简介")
    isbn = sa.Column(sa.String(50), nullable=True, comment="图书编号")
    rating = sa.Column(sa.Float, comment="用户评分")
    rating_count = sa.Column(sa.Integer, comment="评分人数")
    pages = sa.Column(sa.Integer, default=0, comment="总页数")
    publisher = sa.Column(sa.String(255), nullable=True, comment='出版社')
    publish_date = sa.Column(sa.String(50), comment="出版日期")
    douban_url = sa.Column(sa.String(255), nullable=True, comment="豆瓣图书主页")
    category = sa.Column(sa.String(255), nullable=True, comment="图书种类")
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
