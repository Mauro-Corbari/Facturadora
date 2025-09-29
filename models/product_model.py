from config import db

class Product(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(69), nullable = False)
    desc = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    stock = db.Column(db.Integer, nullable = False)
    
    detalles = db.relationship("Detail", back_populates="product", cascade="all, delete-orphan")