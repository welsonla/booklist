from flask.cli import AppGroup
import click
from app.extensions import db
from app.models.user import User

user_cli = AppGroup("user")

@user_cli.command("create")
@click.argument("name")
def create_user(name):
    print(f"name:{name}")

@user_cli.command("dashboard")
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