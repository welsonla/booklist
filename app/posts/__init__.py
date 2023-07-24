from flask import Blueprint

bp = Blueprint('post', __name__)

from app.posts import routes
