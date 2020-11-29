from flask import Blueprint,render_template,url_for,flash
from main_app.forms import SignupForm
from main_app.models import User
from main_app.ext import (db , bcrypt)


auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/auth/")
def sample_auth():
    return "This is a sample auth endpoint"


@auth_bp.route("/signup/",methods=["GET","POST"])
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



