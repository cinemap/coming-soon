from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserManager, SQLAlchemyAdapter
from flask.ext.babel import Babel
from flask.ext.mail import Mail
# from flask_debugtoolbar import DebugToolbarExtension
# from flask.ext.admin import Admin

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
db = SQLAlchemy(app)
babel = Babel(app)
mail = Mail(app)

# toolbar = DebugToolbarExtension(app)
# admin = Admin(app)

import views
import models
from models import User
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)
