from flask import Blueprint, render_template, request, redirect
from services.appointment_service import get_appointments, get_days_of_week, create_appointments
from exceptions import CreateAppointmentException
from filters.auth_filter import is_doctor


blueprint = Blueprint('appointment', __name__)


@blueprint.route('/user/doctor/appointment', methods=['GET', 'POST'])
@is_doctor
def get_appointment_page():
    start_date_previous_week, days_of_week, start_date_next_week, show_warning = get_days_of_week(
        request)
    error = None
    if request.method == 'POST':
        datetimes = request.form.getlist('datetimes')
        try:
            create_appointments(datetimes=datetimes, days_of_week=days_of_week)
        except CreateAppointmentException:
            error = "đã có lỗi khi tạo cuộc hẹn"
        return redirect(f'/user/doctor/appointment?startDate={request.args.get('startDate')}')

    registered_appointment_map = get_appointments(days_of_week=days_of_week)
    return render_template('doctor/appointments.html',
                           daysOfWeek=days_of_week,
                           registeredAppointmentMap=registered_appointment_map,
                           error=error,
                           startDatePreviousWeek=start_date_previous_week,
                           startDateNextWeek=start_date_next_week,
                           showWarning=show_warning)
