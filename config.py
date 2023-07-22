import os
basedir = os.path.abspath(os.path.dirname(__file__))

# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess pass'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'booklist.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# flask shell
# from app.extensions import  db
# from app.models import Book
# print(db)
# db.create_all()