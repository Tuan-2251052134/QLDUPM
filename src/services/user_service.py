from models import User
from utils import password_util
from models import User, DoctorInfo
from flask_login import login_user
from exceptions.login_exception import LoginException
from utils import password_util
from configs.db_config import db
from enums.user_role import UserRole


def create_user(request):
    dob = request.form.get('dob')
    role = request.form.get('role')
    name = request.form.get('name')
    phone = request.form.get("phone")
    email = request.form.get("email")
    avatar = request.form.get('avatar')
    gender = request.form.get('gender')
    id_card = request.form.get('id_card')
    address = request.form.get('address')
    password = request.form.get('password')
    hash_password = password_util.hash(password)
    user = User(
        dob=dob,
        role=role,
        name=name,
        phone=phone,
        email=email,
        avatar=avatar,
        gender=gender,
        id_card=id_card,
        address=address,
        password=hash_password)
    specialty_id = request.form.get('specialty_id')
    try:
        db.session.add(user)
        db.session.flush()
        if user.role == UserRole.DOCTOR.value:
            doctorInfo = DoctorInfo(
                id=user.id, specialty_id=specialty_id)
            db.session.add(doctorInfo)
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
