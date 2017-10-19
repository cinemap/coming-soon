from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

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


@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

