from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager
from models import User
import os

app = Flask(__name__)
app.config.from_object(Config)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes.auth import auth
from routes.ads import ads
from routes.admin import admin

app.register_blueprint(auth)
app.register_blueprint(ads)
app.register_blueprint(admin)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
