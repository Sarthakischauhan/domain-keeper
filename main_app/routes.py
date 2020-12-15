from flask import Blueprint,render_template,url_for,request,abort,redirect,flash
from flask_login import login_required,current_user
from main_app.models import User,Link
from cryptography.fernet import Fernet
from main_app.ext import db
from main_app import app

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
        sec_links = list(filter(lambda lnk : True if lnk.link_type=="protected" else False ,links))
        yt_links = list(filter(lambda lnk : True if lnk.link_type=="youtube" else False ,links))
        links = list(filter(lambda lnk : True if lnk.link_type=="normal" else False ,links))
    else :
        abort(404)

    if user==current_user:
        return render_template("account.html",links=links,sec_links=sec_links,yt_links=yt_links)

    elif user != current_user:
        return "wait for your turn asshole"



@routes_bp.route("/add",methods=("GET","POST"))
@login_required
def add_link():
    f=Fernet(app.config["ENCRYPTION_KEY"])
    if request.method == "POST":
        url= request.form["url"]
        if request.form["type"]=="protected":
            url = f.encrypt(url.encode())
        link1=Link(user_link=url,
            title=request.form["title"],
            link_type=request.form["type"],
            description=request.form["desc"],
            owner=current_user)
        db.session.add(link1)
        db.session.commit()
        flash(f"{link1.link_type.capitalize()} link successfully added")
        return redirect(url_for("routes_bp.account",username=current_user.username))
    return render_template("add-link.html")
