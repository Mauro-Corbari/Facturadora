from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_app(app):
    app.secret_key = "whythehelldoihavetodothisonethingforaloginsystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///facturadora.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app