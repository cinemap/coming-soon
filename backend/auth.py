from flask.ext.user import UserManager, SQLAlchemyAdapter

from app import app, db
from models import User

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)