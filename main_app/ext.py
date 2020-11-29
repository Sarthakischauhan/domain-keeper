from main_app import app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


#initializing the dependency
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
