from app.extensions import db

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
