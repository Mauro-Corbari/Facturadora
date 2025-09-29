from config import db

class Okyaku(db.Model):
    __tablename__ = "clientes"
    kyakuID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    namae = db.Column(db.String(69), nullable = False)
    meiru = db.Column(db.String(96), unique = True, nullable = False)
    denwa = db.Column(db.Integer, nullable = False)
    adoresu = db.Column(db.String(255), nullable = False)