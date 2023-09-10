from app.extensions import db
from datetime import datetime
from marshmallow import Schema, fields

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), comment="书单名")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"),comment="外键, 作者Id")
    type = db.Column(db.Integer, comment="类型Id")
    item_id = db.Column(db.Integer, default=0, comment="类目Id")
    state = db.Column(db.Integer, default=0, comment="状态")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")