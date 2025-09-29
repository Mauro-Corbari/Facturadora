from config import db
from models.kyaku_model import Okyaku

class Ticket(db.Model):
    __tablename__ = "facturas"
    ticketID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date, nullable = False)
    total = db.Column(db.Integer, nullable = False)
    kyakuID = db.Column(db.Integer, db.ForeignKey("clientes.kyakuID"), nullable=False)

    cliente = db.relationship("Okyaku", back_populates="facturas")
    detalles = db.relationship("Detail", back_populates="factura", cascade="all, delete-orphan")
