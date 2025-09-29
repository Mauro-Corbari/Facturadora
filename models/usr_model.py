from config import db

class User(db.Model):
    __tablename__ = "usuarios"
    usrID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(69), nullable = False)
    mail = db.Column(db.String(96), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(64), nullable = False)