import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.main import bp as main_bp
from app.posts import bp as post_bp
from app.questions import bp as question_bp
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)

    # 注册Main Blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(question_bp, url_prefix='/questions')

    @app.route('/index', methods=['GET'])
    def index():
        return render_template('hello.html')

    @app.route('/test/')
    def test_page():
        return  "<h1>Testing  the Flask Application Factory Pattern</h1>"

    return app