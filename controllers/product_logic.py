from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db
from models.product_model import Product

product_bp = Blueprint("product", __name__)

@product_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.auth"))

@product_bp.route("/products", methods=["GET"])
def product_list():
    products = Product.query.all()
    return render_template("product.html", products=products)

@product_bp.route("/products/create", methods=["POST"])
def create_product():
    data = request.form
    new_product = Product(
        name=data["name"],
        desc=data["desc"],
        price=int(data["price"]),
        stock=int(data["stock"])
    )
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for("product.product_list"))

@product_bp.route("/products/update/<int:id>", methods=["POST"])
def product_update(id):
    product = Product.query.get_or_404(id)
    data = request.form
    product.name = data["name"]
    product.desc = data["desc"]
    product.price = int(data["price"])
    product.stock = int(data["stock"])
    db.session.commit()
    return redirect(url_for("product.product_list"))

@product_bp.route("/products/delete/<int:id>", methods=["POST"])
def product_delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("product.product_list"))
