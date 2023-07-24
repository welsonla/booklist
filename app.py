from flask import Flask
from app import create_app, db

app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    """全局注册db变量"""
    return dict(db=db)
