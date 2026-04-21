from configs.db_config import db
from main import app
from flask_login import UserMixin
from enums.user_role import UserRole
from enums.user_gender import UserGender
from enums.appointment_status import AppointmentStatus


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.Enum(UserRole), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    avatar = db.Column(db.String(200))
    gender = db.Column(db.Enum(UserGender), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class DoctorInfo(db.Model):
    id = db.Column(db.Integer,
                   db.ForeignKey("appointment_time.id"),
                   primary_key=True,
                   autoincrement=True)
    specialty = db.Column(
        db.Integer,
        db.ForeignKey("specialty.id"),
        nullable=False)


class Certication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),  # 👈 FK ở đây
        nullable=False
    )


class AppointmentTime(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    appointment_time_id = db.Column(
        db.Integer,
        db.ForeignKey("appointment_time.id"),
        nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),  # 👈 FK ở đây
        nullable=False)
    symptom = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), nullable=False)


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(150))


class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    image = db.Column(db.String(255))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
