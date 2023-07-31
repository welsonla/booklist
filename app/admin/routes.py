from app.admin import bp
from flask import render_template, render_template_string

@bp.route('/')
def index():
    return render_template('admin/index.html')