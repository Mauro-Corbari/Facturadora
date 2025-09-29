from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.usr_model import User
from config import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth", methods=["GET", "POST"])
def auth():
    tab = request.args.get("tab", "login")

    if request.method == "POST":
        if "login" in request.form:
            email = request.form["mail"]
            password = request.form["password"]

            user = User.query.filter_by(mail=email).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.usrID
                session["user_name"] = user.name
                flash(f"Bienvenido, {user.name}!", "success")
                return redirect(url_for("index"))
            else:
                flash("Credenciales incorrectas", "danger")
                tab = "login"

        elif "register" in request.form:
            name = request.form["name"]
            email = request.form["mail"]
            password = request.form["password"]
            role = request.form.get("role", "user")

            if User.query.filter_by(mail=email).first():
                flash("Este correo ya está registrado", "danger")
                tab = "register"
            else:
                hashed_password = generate_password_hash(password)
                new_user = User(name=name, mail=email, password=hashed_password, role=role)
                db.session.add(new_user)
                db.session.commit()

                flash("Registro exitoso. Ya podés iniciar sesión.", "success")
                tab = "login"

    return render_template("auth.html", tab=tab)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.auth"))
