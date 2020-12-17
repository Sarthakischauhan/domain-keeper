from main_app import app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate,MigrateCommand

#initializing the dependency
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)

login_manager.login_view = "auth_bp.login"

@app.context_processor
def push_to_templates():
    def success_or_not(messages):
        if "Unsuccessfull" in messages[0]:
            return False
        else :
            return True

    def title_unfold(title):
        title = title.strip().split("-")
        title = ' '.join(title)
        return title

    return dict(
            success_or_not = success_or_not,
            len = len,
            title_unfold = title_unfold,
            )
