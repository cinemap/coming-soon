from app import app
from auth import *
from models import *
from views import *


def setup_db():
    db.create_all()


if __name__ == '__main__':
    setup_db()
    app.run()