from flask import Flask, render_template
from routes import user_route

app = Flask(__name__)
app.register_blueprint(user_route.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
