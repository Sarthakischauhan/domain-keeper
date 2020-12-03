from main_app import app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

#initializing the dependency
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)



@app.context_processor
def success_rate():
    def success_or_not(messages):
        if "Unsuccessfull" in messages[0]:
            return False
        else :
            return True
    return dict(success_or_not=success_or_not)
