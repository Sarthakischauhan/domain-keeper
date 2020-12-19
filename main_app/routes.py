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
        page=request.args.get("page",1,type=int)
        len_links = [ len(Link.query.filter_by(owner=user,link_type="normal").all()),
                    len(Link.query.filter_by(owner=user,link_type="protected").all()),
                    len(Link.query.filter_by(owner=user,link_type="youtube").all()),
                    ]
        links = Link.query.filter_by(owner=user,link_type="normal").order_by(Link.date_added.desc()).paginate(page=page,per_page=3)
    else :
        abort(404)

    if user==current_user:
        return render_template("account.html",links=links,len_links=len_links)

    elif user != current_user:
        return "wait for your turn asshole"



@routes_bp.route("/add",methods=("GET","POST"))
@login_required
def add_link():
    f=Fernet(app.config["ENCRYPTION_KEY"])
    if request.method == "POST":
        url= request.form["url"]
        title = request.form["title"].lower().strip().split()
        title = '-'.join(title)
        if request.form["type"]=="protected":
            url = f.encrypt(url.encode())

        link1=Link(user_link=url,
            title=title,
            link_type=request.form["type"],
            description=request.form["desc"],
            owner=current_user)

        db.session.add(link1)
        db.session.commit()
        flash(f"{link1.link_type.capitalize()} link successfully added")
        return redirect(url_for("routes_bp.account",username=current_user.username))

    return render_template("add-link.html")
