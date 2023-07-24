from app.api import bp


@bp.route('/login', methods=['POST'])
def login(username, password):
    return ""


@bp.route('/logout', methods=['POST'])
def logout():
    return ""


@bp.route('/book/<int:id>',methods=('GET', 'POST'))
def book(id):
    return ""


@bp.route('/book/comment', methods='POST')
def comment():
    return ""