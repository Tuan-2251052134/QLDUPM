from models import User
from utils import password_util
from models import User, DoctorInfo, Specialty
from flask_login import login_user, current_user
from exceptions import LoginException, CloudinaryException
from utils import password_util
from configs.db_config import db
from enums.user_role import UserRole
from enums.user_gender import UserGender
from cloudinary import uploader
from sqlalchemy.orm import joinedload
from services import certification_service


def create_user(request):
    dob = request.form.get('dob')
    role = request.form.get('role')
    name = request.form.get('name')
    phone = request.form.get("phone")
    email = request.form.get("email")
    gender = request.form.get('gender')
    id_card = request.form.get('id_card')
    address = request.form.get('address')
    password = request.form.get('password')
    specialty_id = request.form.get('specialtyId')
    hash_password = password_util.hash(password)

    try:
        avatar_file = request.files.get('avatar')
        result = uploader.upload(avatar_file)
        avatar_url = result.get('secure_url')
    except Exception as ex:
        raise CloudinaryException()

    user = User(
        dob=dob,
        role=role,
        name=name,
        phone=phone,
        email=email,
        avatar=avatar_url,
        gender=gender,
        id_card=id_card,
        address=address,
        password=hash_password)

    try:
        db.session.add(user)
        db.session.flush()
        if user.role == UserRole.DOCTOR.value:
            doctorInfo = DoctorInfo(
                id=user.id, specialty_id=specialty_id)
            db.session.add(doctorInfo)
            certification_service.create_cert(user, request)
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
    query = db.session.query(User.id, User.name, Specialty.name)
    query = query.join(DoctorInfo, DoctorInfo.id == User.id)
    query = query.join(Specialty, Specialty.id == DoctorInfo.specialty_id)

    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))

    if specialty_id:
        query = query.filter(DoctorInfo.specialty_id == specialty_id)

    query = query.filter(User.role == UserRole.DOCTOR)
    query = query.limit(limit=10).offset(offset=offset)

    return query.all()


def get_doctor_detail(id):
    query = User.query.filter_by(id=id).options(
        joinedload(User.doctor_info).joinedload(DoctorInfo.certifications),
        joinedload(User.doctor_info).joinedload(DoctorInfo.specialty)
    )
    return query.first()


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
        print(user.gender)
        db.session.add(user)
        certification_service.create_or_update_certs(request)
        db.session.commit()
    except Exception as ex:
        print(ex)
        db.session.rollback()
