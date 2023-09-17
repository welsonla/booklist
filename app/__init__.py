import os
import os.path as op
from flask import Flask, render_template
from config import Config
from app.main import bp as main_bp
from app.posts import bp as post_bp
from app.questions import bp as question_bp
from app.api import bp as api_bp
from app.extensions import db
from flask_login import LoginManager
from app.commands import user_cli
from flask_admin import Admin
from app.dashboard import BaseModelView
from app.models.user import User
from app.models.book import Book
from app.models.quote import Quote
from app.models.collect import Collect
from app.models.review import Review
from app.dashboard.model_view.quote_view import QuoteView
from app.dashboard.model_view.user_view import UserView
from app.dashboard.model_view.book_view import BookView
from app.dashboard.model_view.dashboard_view import DashboardView
from app.dashboard.model_view.admin_view import AdminView
from app.dashboard.model_view.collect_view import CollectView
from app.dashboard.model_view.review_view import ReviewView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_cors import CORS
from flask_migrate import Migrate
from flask_babelex import Babel

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", instance_relative_config=True)
    app.config.from_object(config_class)

    login_manager = LoginManager(app)

    # 配置支持跨域
    CORS(app)

    # 实例化拓展
    # login_manager.init_app(app)
    app.cli.add_command(user_cli)

    # 注册数据库管理类
    db.init_app(app)

    # 中文本地化
    babel = Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    app.config["LANGUAGES"] = {"zh_CN":"Chinese"}
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

    migrate = Migrate(app, db)

    # AdminLTE
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

    admin = Admin(app, name='Dashboard', template_mode='bootstrap4', base_template='dashboard/layout.html') # index_view=DashboardView(name='Dashboard', url='/dashboard', endpoint='admin')
    # 注册自定义的 ModelView
    admin.add_view(UserView(User, db.session))
    admin.add_view(BookView(Book, db.session))
    admin.add_view(QuoteView(Quote, db.session))
    admin.add_view(CollectView(Collect, db.session))
    admin.add_view(ReviewView(Review, db.session))
    admin.add_view(DashboardView(name='Dashboard', endpoint='dashboard'))

    admin.add_view(DashboardView(name='Hello 1', endpoint='test1', category='Test'))
    admin.add_view(DashboardView(name='Hello 2', endpoint='test2', category='Test'))
    admin.add_view(DashboardView(name='Hello 3', endpoint='test3', category='Test'))

    # AdminLTE fileupload
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='uploads'))

    # 注册Main Blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
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

    @babel.localeselector
    def get_locale():
        return 'zh_Hans_CN'

    return app



