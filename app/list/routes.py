from flask import Flask, render_template, redirect, url_for
from app.list import bp


@bp.route('/')
def index():
    return "Hello"