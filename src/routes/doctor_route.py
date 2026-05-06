from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from services import user_service, specialty_service, certification_service
from configs.security_config import login_manager
from filters.auth_filter import is_doctor

blueprint = Blueprint('doctor', __name__)


@blueprint.route('/doctor/profile', methods=['GET'])
@is_doctor
def get_doctor_page():
    user = user_service.get_doctor_detail(current_user.id)
    return render_template('doctor/profile.html', user=user)


@blueprint.route('/doctor/update-profile', methods=['GET', "POST"])
@is_doctor
def get_doctor_update_page():
    if request.method == 'POST':
        user_service.update_user(request=request)
    user = user_service.get_doctor_detail(current_user.id)
    specialties = specialty_service.get_specialties()
    cert_count = int(request.args.get(
        "certCount", len(user.doctor_info.certifications)))
    return render_template('doctor/update_profile.html', user=user, specialties=specialties, certCount=cert_count)


@blueprint.route('/doctor/delete-cert/<id>', methods=["GET"])
@is_doctor
def delete_cert(id):
    certification = certification_service.get_certifcation_by_id(id)
    if certification.doctor_info_id != current_user.id:
        return redirect("/home")

    certification_service.delete_cert(certfication=certification)
    return redirect("/doctor/update-profile")

