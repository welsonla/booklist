from flask import Blueprint

bp = Blueprint('list',__name__)

from app.list import routes
