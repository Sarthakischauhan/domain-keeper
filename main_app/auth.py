from flask import Blueprint,render_template,url_for,flash,request
from main_app.forms import SignupForm,LoginForm
from main_app.models import User
from main_app.ext import (db , bcrypt)
from flask_login import login_user,current_user


auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/auth/")
def sample_auth():
    return "This is a sample auth endpoint"


@auth_bp.route("/signup",methods=["GET","POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data , email=form.password.data , password=pass_hash , name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash("Your Message Has Been Successfully Created")
        return redirect(url_for("routes_bp.index"))

    return render_template("signup.html",form=form)



@auth_bp.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        password_check = bcrypt.check_password_hash(User.query.password,form.password.data).first()
        if user and password_check:
            login_user(user)
            next_page = request.args.get("next") 
            return "Login Successful" if next_page else "catch me if you can"
        else :
            flash("Login Unsuccessfull")

    return render_template("login.html",form=form)
        



