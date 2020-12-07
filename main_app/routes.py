from flask import Blueprint,render_template,url_for,request,abort
from flask_login import login_required,current_user
from main_app.models import User,Link

routes_bp = Blueprint("routes_bp",__name__)

@routes_bp.route("/")
def index():
    return render_template("home.html")


@routes_bp.route("/<string:username>")
@login_required
def account(username):
    user = User.query.filter_by(username = username).first()
    secure_links = Link.query.filter_by(owner=current_user , link_type="protected")
    links = Link.query.filter_by(owner=current_user)
    if user and user==current_user:
        return render_template("account.html")

    elif user != current_user:
        return "wait for your turn asshole"

    else :
        abort(404)

