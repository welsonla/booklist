from app.extensions import db
# from flask_sqlalchemy import Column,String,Integer,Text,Float,DateTime
import datetime

class Book(db.Model):
    __tablename__='book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), comment="书名")
    cover_url = db.Column(db.String(255), comment="封面")
    author = db.Column(db.String(50), comment="作者")
    price = db.Column(db.Float, default=0, comment="定价")
    desc = db.Column(db.Text, nullable=True, comment="简介")
    isbn = db.Column(db.String(50), nullable=True, comment="图书编号")
    rating = db.Column(db.Float, comment="用户评分")
    rating_count = db.Column(db.Integer, comment="评分人数")
    pages = db.Column(db.Integer, default=0, comment="总页数")
    publisher = db.Column(db.String(255), nullable=True, comment='出版社')
    publish_date = db.Column(db.String(50), comment="出版日期")
    douban_url = db.Column(db.String(255), nullable=True, comment="豆瓣图书主页")
    category = db.Column(db.String(255), nullable=True, comment="图书种类")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
