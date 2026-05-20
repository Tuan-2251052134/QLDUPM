from models import User
from utils import password_util
from models import User, DoctorInfo, Symptom
from flask_login import login_user, current_user, logout_user
from exceptions import LoginException, CloudinaryException
from utils import password_util
from configs.db_config import db
from enums.user_role import UserRole
from enums.user_gender import UserGender
from cloudinary import uploader
from sqlalchemy.orm import joinedload
from services import certification_service, appointment_service, specialty_service
from datetime import datetime, timedelta


def create_user(user, specialty_id, avatar_file, certification_name, certification_file, hospital_id):
    user.password = password_util.hash(user.password)

    try:
        result = uploader.upload(avatar_file)
        avatar_url = result.get('secure_url')
    except Exception as ex:
        raise CloudinaryException()

    user.avatar = avatar_url
    try:
        db.session.add(user)
        db.session.flush()
        if user.role == UserRole.DOCTOR.value:
            doctorInfo = DoctorInfo(
                id=user.id, specialty_id=specialty_id, hospital_id=hospital_id)
            db.session.add(doctorInfo)
            certification_service.create_cert(
                user, certification_name, certification_file)
        db.session.commit()
    except Exception as ex:
        print(ex)
        db.session.rollback()


def login(request):
    email = request.form.get('email')
    password = request.form.get('password')

    found_user = User.query.filter_by(email=email).first()
    if found_user == None:
        raise LoginException()

    password_util.verify(found_user.password, password)

    login_user(found_user)

    return found_user.role


def get_doctors(name, specialty_id, offset=0):
    query = User.query

    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))

    if specialty_id:
        query = query.join(DoctorInfo).filter(
            DoctorInfo.specialty_id == specialty_id)

    query = query.options(
        joinedload(User.doctor_info).joinedload(DoctorInfo.specialty)
    )

    query = query.filter(User.role == UserRole.DOCTOR)
    query = query.limit(limit=6).offset(offset=offset*6)
    specialties = specialty_service.get_specialties()
    return query.all(), specialties


def get_doctor_detail(id):
    query = User.query.filter_by(id=id).options(
        joinedload(User.doctor_info).joinedload(DoctorInfo.certifications),
        joinedload(User.doctor_info).joinedload(DoctorInfo.specialty),
        joinedload(User.doctor_info).joinedload(DoctorInfo.hospital)
    )

    return query.first()


def get_doctor_detail_with_worktime(id):
    days_of_week, registered_appointment_map, _, _, _ = appointment_service.get_appointments_by_doctor(
        start_date=(datetime.now() + timedelta(7)).strftime("%d/%m/%Y"), user_id=id)
    symptoms = Symptom.query.all()
    return get_doctor_detail(id), days_of_week, registered_appointment_map, symptoms


def update_user(request):
    user = User.query.filter_by(id=current_user.id).first()
    if request.form.get("name"):
        user.name = request.form.get("name")
    if request.form.get("email"):
        user.email = request.form.get("email")
    if request.form.get("phone"):
        user.phone = request.form.get("phone")
    if request.form.get("password"):
        hash_password = password_util.hash(request.form.get("password"))
        user.password = hash_password
    if request.form.get("dob"):
        user.dob = request.form.get("dob")
    if request.form.get('gender') != None:
        user.gender = UserGender(int(request.form.get("gender")))
    if request.form.get("idCard"):
        user.id_card = request.form.get("idCard")
    if request.form.get("address"):
        user.address = request.form.get("address")
    if request.form.get("specialtyId"):
        user.specialty_id = request.form.get("specialtyId")
    if request.files.get("avatar").filename:
        try:
            avatar_file = request.files.get('avatar')
            result = uploader.upload(avatar_file)
            avatar_url = result.get('secure_url')
            user.avatar = avatar_url
        except Exception as ex:
            raise CloudinaryException()

    try:
        db.session.add(user)
        certification_service.create_or_update_certs(request)
        db.session.commit()
    except Exception as ex:
        print(ex)
        db.session.rollback()


def get_current_doctors():
    return User.query.filter_by(role=UserRole.DOCTOR).options(
        joinedload(User.doctor_info).joinedload(DoctorInfo.specialty)
    ).limit(3).all(), specialty_service.get_current_specialties()


def logout():
    logout_user()
