from app.extensions import db

class AccessToken(db.Model):
    """用户授权Token表"""
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    userid = db.Column(db.Integer, nullable=False, comment="用户id")
    token = db.Column(db.String, nullable=False, comment="登录授权Token")