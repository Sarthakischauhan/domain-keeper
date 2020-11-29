from main_app.ext import (db,login_manager)
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return User.query.get(int(user_id))
    else :
        return None

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(120),nullable=False,unique=True)
    email=db.Column(db.String(60),nullable=False,unique=True)
    name=db.Column(db.String(20),nullable=False)
    links = db.relationship("Link",backref="owner",lazy=True)

    def __repr__(self):
        return f"User({self.username},{self.email},{self.name})"


class Link(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_link = db.Column(db.String(240),nullable=False)
    title =  db.Column(db.String(30),nullable=False)
    link_type =  db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Link({self.title})"

