import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.main import bp as main_bp

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", instance_relative_config=True)

    app.config.from_mapping(
        SECRECT_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
    )

    app.config.from_object(config_class)

    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///booklist.db"

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # 初始化数据库链接
    db.init_app(app)

    print("db.init_app")
    # 创建所有表
    with app.app_context():
        print("create all tables")
        db.create_all()


    # 注册Main Blueprint
    app.register_blueprint(main_bp)

    @app.route('/index', methods=['GET'])
    def index():
        return render_template('hello.html')
    
    return app