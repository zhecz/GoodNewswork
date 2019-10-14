from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_principal import Principal, Permission, RoleNeed
from flask_principal import identity_loaded, RoleNeed, UserNeed


app = Flask(__name__)

app.config['SECRET_KEY'] = 'KdwslCx7DZ72Nk_IpvSA1M8IJC1Gk67J'
#app.config['SQLALCHEMY_DATABASE_URI'] = 
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://xxfdqbgu:0-u_otmPgc2alndmeH-6lFtMuln1dj8i@salt.db.elephantsql.com:5432/xxfdqbgu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hwhmmhsr:KdwslCx7DZ72Nk_IpvSA1M8IJC1Gk67J@salt.db.elephantsql.com:5432/hwhmmhsr'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# load the extension
principals = Principal(app)


from flaskDemo import routes
from flaskDemo import models

models.db.create_all()

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'roleID'):
        identity.provides.add(RoleNeed(current_user.roleID))

    