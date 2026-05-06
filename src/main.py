from __init__ import app
from routes import user_route, appointment_route, doctor_route, payment_route

app.register_blueprint(user_route.blueprint)
app.register_blueprint(appointment_route.blueprint)
app.register_blueprint(doctor_route.blueprint)
app.register_blueprint(payment_route.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
