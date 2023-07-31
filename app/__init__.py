import os
from flask import Flask, render_template
from config import Config
from app.main import bp as main_bp
from app.posts import bp as post_bp
from app.questions import bp as question_bp
from app.extensions import db
from app.models.user import User
from app.models.book import Book
from flask_login import LoginManager
from app.commands import user_cli
from flask.cli import cli
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.admin import BaseModelView
from app.admin.model_view.user_view import UserView
from app.admin.model_view.book_view import BookView
from app.admin.model_view.dashboard_view import DashboardView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", instance_relative_config=True)
    app.config.from_object(config_class)

    login_manager = LoginManager(app)

    # 实例化拓展
    # login_manager.init_app(app)
    app.cli.add_command(user_cli)

    # 注册数据库管理类
    db.init_app(app)

    # AdminLTE
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='booklist', template_mode='bootstrap4')
    admin.add_view(UserView(User, db.session, category='User'))
    admin.add_view(BookView(Book, db.session, category='Book'))
    admin.add_view(DashboardView(name='Dashboard', endpoint='dashboard'))

    # AdminLTE fileupload
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='uploads'))

    # 注册Main Blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(question_bp, url_prefix='/questions')

    @app.route('/index', methods=['GET'])
    def index():
        return render_template('hello.html')

    @app.shell_context_processor
    def make_shell_context():
        """全局注册db变量"""
        return dict(db=db)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    @app.context_processor
    def inject_user():
        user = User.query.first()
        return dict(user=user)

    return app



