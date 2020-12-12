from flask import Flask
import os

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')

elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")


from main_app.routes import routes_bp
from main_app.auth import auth_bp

app.register_blueprint(routes_bp)
app.register_blueprint(auth_bp)


