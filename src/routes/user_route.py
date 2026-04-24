from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from services import user_service, specialty_service
from models import User
from configs.security_config import login_manager
from exceptions.login_exception import LoginException
from argon2.exceptions import InvalidHashError
from enums.user_role import UserRole


blueprint = Blueprint('user', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@blueprint.route('/user/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == "POST":
            user_service.create_user(request=request)
            return redirect('/user/login')
        specialties = specialty_service.get_specialties()
        return render_template('register.html', specialties=specialties)
    except Exception:
        return render_template('register.html')


@blueprint.route('/user/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == "GET":
            return render_template('login.html')

        role = user_service.login(request=request)
        if role == UserRole.DOCTOR:
            return redirect('/user/doctor/profile')

        return redirect('home')

    except LoginException:
        return render_template('login.html', showError=True)
    except InvalidHashError:
        return render_template('login.html', showError=True)


@blueprint.route('/user/home', methods=['GET'])
def home():
    specialties = specialty_service.get_specialties()
    return render_template('home.html', specialties=specialties)


@blueprint.route("/user/find-doctor", methods=['GET'])
def get_doctor_profile():
    return render_template('find_doctor.html')


@blueprint.route('/user/doctor/profile', methods=['GET'])
def get_doctor_page():
    if current_user and current_user.role != UserRole.DOCTOR:
        redirect('/user/home')
    return render_template('doctor/profile.html')
