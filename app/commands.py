from flask.cli import AppGroup
import click
from app.extensions import db
from app.models.user import User
from app.models.review import Review
from app.models.collect import Collect,CollectBooks

user_cli = AppGroup("user")


# flask user create welsonla
@user_cli.command("create")
@click.argument("name")
def create_user(name):
    """测试Command"""
    print(f"name:{name}")


# flask user dbcreate
@user_cli.command("dbcreate")
def db_create():
    """创建Model表"""
    db.create_all()


@user_cli.command("dashboard")
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create Admin User"""
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