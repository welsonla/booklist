from app.extensions import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from marshmallow import Schema, fields


class User(db.Model, UserMixin):
    """用户表"""
    __excluede__ = ['password_hash']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), comment="用户名, 登录用的")
    nickname = db.Column(db.String(50), nullable=True, comment="昵称")
    bio = db.Column(db.Text, nullable=True, comment="签名")
    password_hash = db.Column(db.String(128), nullable=False, comment="密码,加密后的")
    email = db.Column(db.String(50), comment="邮箱")
    role = db.Column(db.Integer, comment="用户角色")
    state = db.Column(db.Integer, default=0, comment="0:正常，1:冻结")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quotes = db.relationship('Quote', backref='user')

    reviews = db.relationship('Review', back_populates='author')

    def encode_password(self, password):
        """将密码进行散列加密"""
        pwd = self.password_hash = generate_password_hash(password)
        print("加密后的密码")
        return pwd

    def valid_password(self, password):
        """检查密码"""
        rslt = check_password_hash(self.password_hash, password)
        return rslt

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class Role(db.Model):
    """用户角色表"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), comment="角色名称")
    level = db.Column(db.Integer, comment="角色Id")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=datetime.utcnow)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    nickname = fields.Str()
    password_hash = fields.Str()
    bio = fields.Str()
    role = fields.Int()
    state = fields.Int()
    email = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
