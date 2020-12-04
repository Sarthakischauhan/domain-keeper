from flask import Blueprint,render_template,url_for
from flask_login import login_required,current_user


routes_bp = Blueprint("routes_bp",__name__)

@routes_bp.route("/")
def index():
    return render_template("home.html")


@routes_bp.route("/<string:username>")
@login_required
def account(username):
    return f"welcome {username}"



