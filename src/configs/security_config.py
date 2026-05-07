from dotenv import load_dotenv
import os
load_dotenv()

from __init__ import app
from flask_login import LoginManager

app.secret_key = os.getenv("APP_SECRET_KEY")
login_manager = LoginManager(app)
