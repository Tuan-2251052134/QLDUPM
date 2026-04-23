from __init__ import app
from flask_login import LoginManager

app.secret_key = "cb019579-6271-4875-a751-37d239e51119"
login_manager = LoginManager(app)
