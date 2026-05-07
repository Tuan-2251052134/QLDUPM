from flask import Blueprint, render_template, request, redirect
from services import appointment_service
from datetime import datetime
from exceptions import CreateAppointmentException
from filters.auth_filter import is_doctor, is_patient
from flask_login import current_user


blueprint = Blueprint('appointment', __name__)


@blueprint.route('/appointment/doctor', methods=['GET', 'POST'])
@is_doctor
def get_appointment_page():
    error = None
    if request.method == 'POST':
        datetimes = request.form.getlist('datetimes')
        try:
            appointment_service.create_appointments(
                datetimes=datetimes, start_date=request.args.get("startDate"), user_id=current_user.id)
        except CreateAppointmentException:
            error = "đã có lỗi khi tạo cuộc hẹn"
        return redirect(f'/appointment/doctor?startDate={request.args.get('startDate')}')

    days_of_week, registered_appointment_map, start_date_previous_week, start_date_next_week, show_warning = appointment_service.get_appointments_by_doctor(
        start_date=request.args.get("startDate"), user_id=current_user.id)
    return render_template('doctor/appointments.html',
                           daysOfWeek=days_of_week,
                           registeredAppointmentMap=registered_appointment_map,
                           error=error,
                           startDatePreviousWeek=start_date_previous_week,
                           startDateNextWeek=start_date_next_week,
                           showWarning=show_warning)


@blueprint.route('/appointment/doctor/<id>', methods=['GET', 'POST'])
@is_doctor
def get_appointment_detail_page(id):
    appointment = appointment_service.get_appointment_by_id_width_patient(id)
    return render_template('doctor/detail_appointment.html',
                           appointment=appointment)


@blueprint.route('/appointment/patient', methods=['POST'])
@is_patient
def update_appointment():
    appointment_id = request.form.get("appointmentId")
    patient_id = current_user.id
    symptom = request.form.get("symptom")
    doctor_id = request.form.get("doctorId")
    session = appointment_service.apply_appointment(
        appointment_id, patient_id, symptom)
    return redirect(f"/find-doctor/{doctor_id}?sessionId={session.id}")


@blueprint.route('/appointment/patient/timetable', methods=['GET'])
@is_patient
def get_patient_appointments():
    start_date = request.args.get(
        "startDate", datetime.now().strftime("%d/%m/%Y"))
    days_of_week, registered_appointment_map, start_date_previous_week, start_date_next_week = appointment_service.get_appointments_by_patient(start_date=start_date,
                                                                                                                                               user_id=current_user.id)
    return render_template('patient/timetable.html',
                           registeredAppointmentMap=registered_appointment_map,
                           daysOfWeek=days_of_week,
                           startDatePreviousWeek=start_date_previous_week,
                           startDateNextWeek=start_date_next_week)
