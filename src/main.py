from __init__ import app
from routes import user_route

app.register_blueprint(user_route.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
