from flask import render_template, redirect, url_for, Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from models.kyaku_model import Okyaku

API_URL = "http://localhost:5000/kyaku"

kyaku_bp = Blueprint("kyaku", __name__)

@kyaku_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.auth"))


@kyaku_bp.route("/kyaku/create", methods=["POST"])
def create_kyaku():
    data = request.form
    new_kyaku = Okyaku(
        namae=data["name"],
        meiru=data["email"],
        denwa=data["denwa"],
        adoresu=data["address"]
    )
    db.session.add(new_kyaku)
    db.session.commit()
    return redirect(url_for("kyaku.kyaku_list"))


@kyaku_bp.route("/kyaku", methods=["GET"])
def kyaku_list():
    kyaku_list = Okyaku.query.all()
    return render_template("kyaku.html", kyaku=[
        {
            "id": k.kyakuID,
            "name": k.namae,
            "email": k.meiru,
            "denwa": k.denwa,
            "address": k.adoresu
        }
        for k in kyaku_list
    ])


@kyaku_bp.route("/kyaku/update/<int:id>", methods=["POST"])
def kyaku_update(id):
    kyaku = Okyaku.query.get_or_404(id)

    if request.method == "POST":
        data = request.form
        kyaku.namae = data["name"]
        kyaku.meiru = data["email"]
        kyaku.denwa = data["denwa"]
        kyaku.adoresu = data["address"]

        db.session.commit()
        return redirect(url_for("kyaku.kyaku_list"))


@kyaku_bp.route("/kyaku/delete/<int:id>", methods=["POST"])
def kyaku_delete(id):
    kyaku = Okyaku.query.get_or_404(id)
    db.session.delete(kyaku)
    db.session.commit()
    return redirect(url_for("kyaku.kyaku_list"))
