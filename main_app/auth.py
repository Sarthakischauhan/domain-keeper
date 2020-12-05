from flask import Blueprint,render_template,url_for,flash,request,redirect
from main_app.forms import SignupForm,LoginForm
from main_app.models import User
from main_app.ext import (db , bcrypt)
from flask_login import login_user,current_user,logout_user


auth_bp = Blueprint("auth_bp",__name__)


@auth_bp.route("/auth/")
def sample_auth():
    return "This is a sample auth endpoint"


@auth_bp.route("/signup",methods=["GET","POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("routes_bp.account",username = current_user.username))
    form = SignupForm()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data , email=form.email.data , password=pass_hash , name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash("Your Account Has Been Successfully Created")
        return redirect(url_for("routes_bp.index"))

    return render_template("signup.html",form=form)



@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes_bp.account",username = current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Welcome.Login Successful")
            return redirect(url_for("routes_bp.account",username=current_user.username)) if next_page else redirect(url_for("routes_bp.index"))
        else :
            flash("Login Unsuccessfull")

    return render_template("login.html",form=form)



@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logout Successful")
    return redirect(url_for("routes_bp.index"))


