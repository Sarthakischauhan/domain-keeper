from flask import Blueprint,render_template,url_for

routes_bp = Blueprint("routes",__name__)

@routes_bp.route("/")
def index():
    return render_template("layout.html")


