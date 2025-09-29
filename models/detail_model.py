from config import db
from models.product_model import Product
from models.ticket_model import Ticket

class Detail(db.Model):
    __tablename__ = "detalle_facturas"
    detailID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    prodID = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    ticketID = db.Column(db.Integer, db.ForeignKey("facturas.ticketID"), nullable=False)
    quant = db.Column(db.Integer, nullable = False)
    unit_price = db.Column(db.Integer, nullable = False)
    subtotal = db.Column(db.Integer, nullable = False)
    
    product = db.relationship("Product", backref="detalles")
    ticket = db.relationship("Ticket", backref="detalles")