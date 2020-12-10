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
    if user :
        links = Link.query.filter_by(owner=user).all()
        secured_links = list(filter(lambda lnk : True if lnk.link_type=="protected" else False ,links))
        ordinary_links = list(filter(lambda lnk : True if lnk.link_type!="protected" else False ,links))
    else :
        abort(404)

    if user==current_user:
        return render_template("account.html",links=links,secured_links=secured_links)

    elif user != current_user:
        return "wait for your turn asshole"



@routes_bp.route("/add",methods=("GET","POST"))
@login_required
def add_link():
    return render_template("add-link.html")
