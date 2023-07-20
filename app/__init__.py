import os
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", instance_relative_config=True)

    app.config.from_mapping(
        SECRECT_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    @app.route('/index', methods=['GET'])
    def index():
        return render_template('hello.html')
    
    return app