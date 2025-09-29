from flask import Flask
from config import init_app, db
from models.kyaku_model import Okyaku
from models.product_model import Product
from models.ticket_model import Ticket
from models.detail_model import Detail
from models.usr_model import User

app = Flask(__name__)
init_app(app)

with app.app_context():
    db.create_all()
    print("Base de datos 'facturadora.db' creada correctamente.")
