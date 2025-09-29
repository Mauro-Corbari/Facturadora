from flask import Flask, render_template, session, redirect, url_for, g
from config import init_app, db

from controllers.kyaku_logic import kyaku_bp
from controllers.product_logic import product_bp
from controllers.ticket_logic import ticket_bp
from controllers.usr_logic import auth_bp

from models.kyaku_model import Okyaku
from models.product_model import Product
from models.ticket_model import Ticket
from models.usr_model import User

app = Flask(__name__)
init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(kyaku_bp)
app.register_blueprint(product_bp)
app.register_blueprint(ticket_bp)


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.auth"))
    return render_template("index.html")


@app.context_processor
def inject_user():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return dict(current_user=user)


if __name__ == "__main__":
    app.run(debug=True)
