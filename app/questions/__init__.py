from flask import Blueprint
from app.extensions import db

bp = Blueprint('questions',__name__)

from app.questions import routes