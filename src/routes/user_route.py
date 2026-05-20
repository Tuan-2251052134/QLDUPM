from flask import Blueprint, render_template, request, redirect
from services import user_service, specialty_service
from models import User
from configs.security_config import login_manager
from exceptions import LoginException, CloudinaryException
from argon2.exceptions import InvalidHashError
from enums.user_role import UserRole
from argon2.exceptions import VerifyMismatchError
from filters.auth_filter import is_patient


blueprint = Blueprint('common', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == "POST":
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
            hospital_id = request.form.get("hospitalId")
            user = User(
                dob=dob,
                role=role,
                name=name,
                phone=phone,
                email=email,
                gender=gender,
                id_card=id_card,
                address=address,
                password=password)
            avatar_file = request.files.get('avatar')
            certification_name = request.form.get("certificationName")
            certification_file = request.files.get('certification')
            user_service.create_user(
                user, specialty_id, avatar_file, certification_name, certification_file, hospital_id)
            return redirect('/login')
        specialties, hospitals = specialty_service.get_specialties_with_hospitals()
        return render_template('/public/register.html', specialties=specialties, hospitals=hospitals)
    except CloudinaryException:
        error = "Có lỗi với cloudinary"
        return render_template('/public/register.html', error=error)
    except Exception:
        return render_template('/public/register.html')


@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == "GET":
            return render_template('/public/login.html')

        role = user_service.login(request=request)
        if role == UserRole.DOCTOR:
            return redirect('/doctor/profile')

        return redirect('home')
    except LoginException:
        return render_template('/public/login.html', showError=True)
    except VerifyMismatchError:
        return render_template('/public/login.html', showError=True)
    except InvalidHashError:
        return render_template('/public/login.html', showError=True)


@blueprint.route('/home', methods=['GET'])
def home():
    doctors, specialties = user_service.get_current_doctors()
    return render_template('/public/home.html', doctors=doctors, specialties=specialties)


@blueprint.route("/find-doctor", methods=['GET'])
def get_doctors():
    name = request.args.get('name', "")
    specialty_id = int(request.args.get('specialtyId', 0))
    offset = int(request.args.get('offset', 0))
    previous_offset = offset-1 if offset != 0 else 0
    next_offset = offset + 1
    found_users, specialties = user_service.get_doctors(
        name, specialty_id, offset=offset)
    return render_template('public/find_doctor.html',
                           foundUsers=found_users,
                           specialties=specialties,
                           previousOffset=previous_offset,
                           nextOffset=next_offset,
                           name=name,
                           specialtyId=specialty_id)


@blueprint.route("/find-doctor/<id>", methods=['GET'])
def get_doctor_detail_profile(id):
    user, dates, registered_appointment_map, symptoms = user_service.get_doctor_detail_with_worktime(
        id)
    session_id = request.args.get("sessionId")
    return render_template('/public/detail_doctor.html',
                           user=user,
                           daysOfWeek=dates,
                           registeredAppointmentMap=registered_appointment_map,
                           symptoms=symptoms,
                           sessionId=session_id)


@blueprint.route("/logout", methods=["GET"])
def logout():
    user_service.logout()
    return redirect(f"/login")
