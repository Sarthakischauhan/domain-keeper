from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")

elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")


from main_app.routes import routes_bp
from main_app.auth import auth_bp

app.register_blueprint(routes_bp)
app.register_blueprint(auth_bp)


