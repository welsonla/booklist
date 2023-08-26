from app.models.access_token import AccessToken

def get_userid_by_sign(sign):
    """通过sign获取用户id"""
    token = AccessToken.query.filter_by(token=sign).first()
    return token.user_id