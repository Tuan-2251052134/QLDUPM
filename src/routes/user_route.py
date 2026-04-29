from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from services import user_service, specialty_service, certification_service
from models import User
from configs.security_config import login_manager
from exceptions import LoginException, CloudinaryException
from argon2.exceptions import InvalidHashError
from enums.user_role import UserRole
from filters.auth_filter import is_doctor


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
    except CloudinaryException:
        error = "Có lỗi với cloudinary"
        return render_template('register.html', error=error)
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
    name = request.args.get('name')
    specialty_id = request.args.get('specialty_id')
    found_users = user_service.get_doctors(name, specialty_id)
    print(found_users)
    return render_template('find_doctor.html', foundUsers=found_users)


@blueprint.route("/user/find-doctor/<id>", methods=['GET'])
def get_doctor_detail_profile(id):
    user = user_service.get_doctor_detail(id)
    return render_template('/detail_doctor.html', user=user)


@blueprint.route('/user/doctor/profile', methods=['GET'])
@is_doctor
def get_doctor_page():
    user = user_service.get_doctor_detail(current_user.id)
    return render_template('doctor/profile.html', user=user)


@blueprint.route('/user/doctor/update-profile', methods=['GET', "POST"])
@is_doctor
def get_doctor_update_page():
    if request.method == 'POST':
        user_service.update_user(request=request)
    user = user_service.get_doctor_detail(current_user.id)
    specialties = specialty_service.get_specialties()
    cert_count = int(request.args.get(
        "certCount", len(user.doctor_info.certifications)))
    return render_template('doctor/update_profile.html', user=user, specialties=specialties, certCount=cert_count)


@blueprint.route('/user/doctor/delete-cert/<id>', methods=["GET"])
@is_doctor
def delete_cert(id):
    certification = certification_service.get_certifcation_by_id(id)
    if certification.doctor_info_id != current_user.id:
        return redirect("/user/home")   
    
    certification_service.delete_cert(certfication=certification)
    return redirect("/user/doctor/update-profile")

