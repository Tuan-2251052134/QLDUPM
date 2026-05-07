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

    doctor_info = db.relationship(
        "DoctorInfo",
        uselist=False,
        lazy="select"
    )


class DoctorInfo(db.Model):
    id = db.Column(db.Integer,
                   db.ForeignKey("user.id"),
                   primary_key=True)
    specialty_id = db.Column(
        db.Integer,
        db.ForeignKey("specialty.id"),
        nullable=False)
    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospital.id"),
        nullable=False)
    certifications = db.relationship(
        "Certification",
        lazy="select"
    )
    specialty = db.relationship("Specialty", lazy="select")
    hospital = db.relationship("Hospital", lazy="select")


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    url = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    doctor_info_id = db.Column(
        db.Integer,
        db.ForeignKey("doctor_info.id"),  # 👈 FK ở đây
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
    patient = db.relationship("User", foreign_keys=[patient_id], lazy="select")

    __table_args__ = (
        UniqueConstraint('date', 'appointment_time_id', 'doctor_id', 'patient_id',
                         name='unique_date_appointment_time_id_doctor_id_patient_id'),
    )


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(150))


class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    image = db.Column(db.String(255))


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    address = db.Column(db.String(90))
    bank_account_number = db.Column(db.String(20))


class PaymentInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.String(255), nullable=False, unique=True)
    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointment.id"),
        nullable=False
    )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        hospitals = [
            Hospital(name="BV Bạch Mai", address="Hà Nội",
                     bank_account_number="100001"),
            Hospital(name="BV Chợ Rẫy", address="TP.HCM",
                     bank_account_number="100002"),
            Hospital(name="BV 108", address="Hà Nội",
                     bank_account_number="100003"),
            Hospital(name="BV Việt Đức", address="Hà Nội",
                     bank_account_number="100004"),
            Hospital(name="BV Đại học Y Hà Nội", address="Hà Nội",
                     bank_account_number="100005"),
            Hospital(name="BV Nhi Trung Ương", address="Hà Nội",
                     bank_account_number="100006"),
            Hospital(name="BV Phụ sản Trung Ương", address="Hà Nội",
                     bank_account_number="100007"),
            Hospital(name="BV K Trung Ương", address="Hà Nội",
                     bank_account_number="100008"),
            Hospital(name="BV E", address="Hà Nội",
                     bank_account_number="100009"),
            Hospital(name="BV Thanh Nhàn", address="Hà Nội",
                     bank_account_number="100010"),

            Hospital(name="BV Nhân Dân 115", address="TP.HCM",
                     bank_account_number="100011"),
            Hospital(name="BV Đại học Y Dược TP.HCM",
                     address="TP.HCM", bank_account_number="100012"),
            Hospital(name="BV Từ Dũ", address="TP.HCM",
                     bank_account_number="100013"),
            Hospital(name="BV Nhi Đồng 1", address="TP.HCM",
                     bank_account_number="100014"),
            Hospital(name="BV Nhi Đồng 2", address="TP.HCM",
                     bank_account_number="100015"),
            Hospital(name="BV Ung Bướu TP.HCM", address="TP.HCM",
                     bank_account_number="100016"),
            Hospital(name="BV Gia Định", address="TP.HCM",
                     bank_account_number="100017"),
            Hospital(name="BV Quân y 175", address="TP.HCM",
                     bank_account_number="100018"),

            Hospital(name="BV Đa khoa Đà Nẵng", address="Đà Nẵng",
                     bank_account_number="100019"),
            Hospital(name="BV Trung ương Huế", address="Huế",
                     bank_account_number="100020"),
            Hospital(name="BV Cần Thơ", address="Cần Thơ",
                     bank_account_number="100021"),
            Hospital(name="BV Đa khoa Hải Phòng", address="Hải Phòng",
                     bank_account_number="100022"),
            Hospital(name="BV Đa khoa Quảng Ninh",
                     address="Quảng Ninh", bank_account_number="100023"),
            Hospital(name="BV Đa khoa Nghệ An", address="Nghệ An",
                     bank_account_number="100024"),
            Hospital(name="BV Đa khoa Thanh Hóa", address="Thanh Hóa",
                     bank_account_number="100025"),
            Hospital(name="BV Đa khoa Bình Dương",
                     address="Bình Dương", bank_account_number="100026"),
            Hospital(name="BV Đa khoa Đồng Nai", address="Đồng Nai",
                     bank_account_number="100027"),
            Hospital(name="BV Đa khoa Khánh Hòa", address="Khánh Hòa",
                     bank_account_number="100028"),
        ]
        data = [
            "Nội tổng quát",
            "Tim mạch",
            "Hô hấp",
            "Tiêu hóa",
            "Nội tiết",
            "Thần kinh",
            "Ngoại tổng quát",
            "Ngoại thần kinh",
            "Chấn thương chỉnh hình",
            "Ngoại tim mạch",
            "Ngoại tiết niệu",
            "Sản khoa",
            "Phụ khoa",
            "Nhi khoa",
            "Sơ sinh",
            "Tai Mũi Họng",
            "Mắt",
            "Da liễu",
            "Răng Hàm Mặt",
            "Ung bướu",
            "Phục hồi chức năng",
            "Y học cổ truyền",
            "Truyền nhiễm"
        ]
        symptoms = [
            Symptom(description="Sốt"),
            Symptom(description="Ho"),
            Symptom(description="Đau đầu"),
            Symptom(description="Đau họng"),
            Symptom(description="Mệt mỏi"),
            Symptom(description="Khó thở"),
            Symptom(description="Đau ngực"),
            Symptom(description="Chóng mặt"),
            Symptom(description="Buồn nôn"),
            Symptom(description="Nôn mửa"),
            Symptom(description="Tiêu chảy"),
            Symptom(description="Táo bón"),
            Symptom(description="Đau bụng"),
            Symptom(description="Mất ngủ"),
            Symptom(description="Đau cơ"),
            Symptom(description="Đau khớp"),
            Symptom(description="Sổ mũi"),
            Symptom(description="Nghẹt mũi"),
            Symptom(description="Ớn lạnh"),
            Symptom(description="Đổ mồ hôi nhiều"),
        ]

        specialties = [Specialty(name=s) for s in data]
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
        db.session.add_all(specialties)
        db.session.add_all(symptoms)
        db.session.add_all(hospitals)
        db.session.commit()
