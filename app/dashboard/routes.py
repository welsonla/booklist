from app.dashboard import bp
from flask import render_template, render_template_string

@bp.route('/')
def index():
    return render_template('dashboard/index.html')