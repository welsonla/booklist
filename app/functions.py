from app.models.access_token import AccessToken

def get_userid_by_sign(sign):
    """通过sign获取用户id"""
    # print(f"sign:${sign}")
    token = AccessToken.query.filter_by(token=sign).first()
    print(f"token:${token}")
    if token is not None:
        return token.userid
    return ""

def remove_lines_from_string(text, num_lines):
    lines = text.split('\n')
    new_lines = lines[num_lines:]
    return '\n'.join(new_lines)