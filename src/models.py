from configs.db_config import db
from sqlalchemy import UniqueConstraint
from __init__ import app
from flask_login import UserMixin
from enums.user_role import UserRole
from enums.user_gender import UserGender
from enums.appointment_status import AppointmentStatus
from datetime import time


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dob = db.Column(db.Date, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    avatar = db.Column(db.String(200))
    gender = db.Column(db.Enum(UserGender), nullable=False)
    id_card = db.Column(db.String(12), nullable=False,  unique=True)
    address = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class DoctorInfo(db.Model):
    id = db.Column(db.Integer,
                   db.ForeignKey("user.id"),
                   primary_key=True,
                   autoincrement=True)
    specialty_id = db.Column(
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
        db.ForeignKey("user.id"))
    symptom = db.Column(db.String(20))
    status = db.Column(db.Enum(AppointmentStatus), nullable=False)

    __table_args__ = (
        UniqueConstraint('date', 'appointment_time_id', 'doctor_id', 'patient_id',
                         name='unique_date_appointment_time_id_doctor_id_patient_id'),
    )


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
        times = [
            AppointmentTime(start_time=time(7, 0), end_time=time(8, 0)),
            AppointmentTime(start_time=time(8, 0), end_time=time(9, 0)),
            AppointmentTime(start_time=time(9, 0), end_time=time(10, 0)),
            AppointmentTime(start_time=time(10, 0), end_time=time(11, 0)),
            AppointmentTime(start_time=time(11, 0), end_time=time(12, 0)),
            AppointmentTime(start_time=time(12, 0), end_time=time(13, 0)),
            AppointmentTime(start_time=time(13, 0), end_time=time(14, 0)),
            AppointmentTime(start_time=time(14, 0), end_time=time(15, 0)),
            AppointmentTime(start_time=time(15, 0), end_time=time(16, 0)),
            AppointmentTime(start_time=time(17, 0), end_time=time(18, 0)),
        ]
        db.session.add_all(times)
        db.session.commit()
