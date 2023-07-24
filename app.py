from flask import Flask
from app import create_app, db
from flask_login import LoginManager
from app.models.user import User
import click

app = create_app('development')

login_manager = LoginManager(app)

@app.shell_context_processor
def make_shell_context():
    """全局注册db变量"""
    return dict(db=db)

@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.name = username
        user.encode_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(name=username, email='wanyc@outlook.com')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')