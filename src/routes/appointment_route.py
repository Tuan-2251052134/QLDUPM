from flask import Blueprint, render_template, request, redirect
from services.appointment_service import get_appointments, get_days_of_week, create_appointments, apply_appointment
from exceptions import CreateAppointmentException
from filters.auth_filter import is_doctor, is_patient
from flask_login import current_user


blueprint = Blueprint('appointment', __name__)


@blueprint.route('/user/doctor/appointment', methods=['GET', 'POST'])
@is_doctor
def get_appointment_page():
    start_date_previous_week, days_of_week, start_date_next_week, show_warning = get_days_of_week(
        request.args.get("startDate"))
    error = None
    if request.method == 'POST':
        datetimes = request.form.getlist('datetimes')
        try:
            create_appointments(
                datetimes=datetimes, days_of_week=days_of_week, user_id=current_user.id)
        except CreateAppointmentException:
            error = "đã có lỗi khi tạo cuộc hẹn"
        return redirect(f'/user/doctor/appointment?startDate={request.args.get('startDate')}')

    registered_appointment_map = get_appointments(
        days_of_week=days_of_week, user_id=current_user.id)
    return render_template('doctor/appointments.html',
                           daysOfWeek=days_of_week,
                           registeredAppointmentMap=registered_appointment_map,
                           error=error,
                           startDatePreviousWeek=start_date_previous_week,
                           startDateNextWeek=start_date_next_week,
                           showWarning=show_warning)


@blueprint.route('/user/patient/appointment', methods=['POST'])
@is_patient
def update_appointment():
    appointment_id = request.form.get("appointmentId")
    patient_id = current_user.id
    symptom = request.form.get("symptom")
    doctor_id = request.form.get("doctorId")
    print(request.form)
    apply_appointment(appointment_id, patient_id, symptom)
    return redirect(f"/user/find-doctor/{doctor_id}")
