from flask import Blueprint,render_template,url_for,request,abort,redirect,flash,jsonify
from flask_login import login_required,current_user
from main_app.models import User,Link
from cryptography.fernet import Fernet
from main_app.ext import db
from main_app import app
import qrcode
from io import BytesIO
import base64

routes_bp = Blueprint("routes_bp",__name__)

@routes_bp.route("/")
def index():
    return render_template("home.html")


@routes_bp.route("/<string:username>")
@login_required
def account(username):
    user = User.query.filter_by(username = username).first()
    if user:
        page=request.args.get("page",1,type=int)
        len_links = [len(Link.query.filter_by(owner=user,link_type="normal").all()),
                    len(Link.query.filter_by(owner=user,link_type="protected").all()),
                    len(Link.query.filter_by(owner=user,link_type="youtube").all()),]
        links = Link.query.filter_by(owner=user,link_type="normal").order_by(Link.id.desc()).paginate(page=page,per_page=6)
    else:
        abort(404)
    if user==current_user:
        return render_template("account.html",links=links,len_links=len_links)

    elif user != current_user:
        return "wait for your turn asshole"


def getlinkData(link_type=None,page=1):
    if not link_type:
	    raise ValueError("Specify The Link Type")
    elif link_type in ("normal","youtube","protected"):
	    if link_type != "protected":
		    links = Link.query.filter_by(owner=current_user,link_type=link_type).order_by(Link.id.desc()).paginate(page=page,per_page=6)
		    links = links.items
	    else:
		    links = Link.query.filter_by(owner=current_user,link_type="protected").order_by(Link.id.desc()).paginate(page=page,per_page=6)
		    f=Fernet(app.config["ENCRYPTION_KEY"])
		    links,length = links.items , len(links.items)
		    for i in range(length):
			    element=links[i].user_link
			    links[i].user_link = f.decrypt(element.encode())
	    return links
    else:
	    raise ValueError("Not known")

@routes_bp.route("/data/<string:v>",methods=["POST"])
@login_required
def sendData(v):
    if v in ("youtube","protected","normal"):
        links=getlinkData(link_type=v)
        ids=[link.id for link in links]
        url=[link.user_link for link in links]
        titles=[link.title for link in links]
        desc=[link.description for link in links]
        return jsonify(
				{
				   "id":ids,
				   "urls":url,
				   "titles":titles,
				   "descriptions":desc
				}
		)
    else:
        abort(404)



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




@routes_bp.route("/<int:linkID>/delete",methods=('GET','POST'))
@login_required
def delete_link(linkID):
    link=Link.query.get(linkID)
    if link.owner==current_user:
        db.session.delete(link)
        db.session.commit()
        return redirect(url_for('routes_bp.account',username=current_user.username))
    else:
        abort(403)


@routes_bp.route("/<string:title>/qr")
@routes_bp.route("/<int:linkID>/qr")
@login_required
def generate_qr(linkID="",title=""):
    if title:
        link=Link.query.filter_by(owner=current_user,title=title).first()
    elif linkID:
        link=Link.query.get(linkID)
    if link:
        f=Fernet(app.config["ENCRYPTION_KEY"])
        if link.link_type != "protected":
            user_link = link.user_link
        elif link.link_type == "protected":
            user_link = f.decrypt(link.user_link.encode())
        img=qrcode.make(user_link)
        byte_for_img=BytesIO()
        img.save(byte_for_img,format="png")
        b_img=base64.b64encode(byte_for_img.getvalue()).decode('utf-8')
        return render_template("qr.html",b_img=b_img)
    else:
        abort(404)



@routes_bp.route("/<string:title>/yt")
@routes_bp.route("/<int:linkID>/yt")
@login_required
def yt_player(linkID="",title=""):
    if title:
        link=Link.query.filter_by(owner=current_user,title=title).first()
    elif linkID:
        link=Link.query.get(linkID)
    if link:
        if link.link_type == "youtube":
            user_link = link.user_link
        else:
            flash("Unsuccessful Launch.Not a Youtube type link")
            return redirect(url_for("routes_bp.account",username=current_user.username))
        link_id = user_link.split("v=")[1]
        if "#t" in user_link:
            link_time = user_link.split("#t")[1]
            embed = f"https://www.youtube.com/embed/{link_id}#t={link_time}"
        else:
            embed =f"https://www.youtube.com/embed/{link_id}"
        return render_template("yt.html",embed=embed)
    else:
        abort(404)



@app.context_processor
def data_template():
	return dict(getlinkData=getlinkData)
