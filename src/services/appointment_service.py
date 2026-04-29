from datetime import timedelta, datetime
from flask_login import current_user
from enums.user_role import UserRole
from enums.appointment_status import AppointmentStatus
from models import Appointment, AppointmentTime
from configs.db_config import db
from exceptions import CreateAppointmentException


def get_days_of_week(request):
    start_date = datetime.strptime(request.args.get(
        "startDate"), "%d/%m/%Y") if request.args.get("startDate") else datetime.now()
    start_of_week = start_date - timedelta(days=start_date.weekday())

    dates = [
        (start_of_week + timedelta(days=i)).strftime("%d/%m/%Y")
        for i in range(7)
    ]
    show_warning = (datetime.strptime(
        dates[6], "%d/%m/%Y") - timedelta(days=7) < datetime.now())
    start_date_previous_week = (
        start_of_week - timedelta(days=7)).strftime("%d/%m/%Y")
    start_date_next_week = (
        start_of_week + timedelta(days=7)).strftime("%d/%m/%Y")
    return start_date_previous_week, dates, start_date_next_week, show_warning


def get_appointments(days_of_week):
    registered_appointments = db.session.query(Appointment, AppointmentTime).filter(
        Appointment.doctor_id == current_user.id,
        Appointment.date >= datetime.strptime(
            days_of_week[0], "%d/%m/%Y").date(),
        Appointment.date <= datetime.strptime(
            days_of_week[6], "%d/%m/%Y").date()
    ).join(AppointmentTime, Appointment.appointment_time_id == AppointmentTime.id).all()

    registered_appointment_map = {}

    for registered_appointment in registered_appointments:
        registered_appointment_map[
            f"{registered_appointment[0].date.strftime("%d/%m/%Y")}-{registered_appointment[1].id}"] = True

    return registered_appointment_map


def create_appointments(datetimes, days_of_week):
    appointments = []

    for _datetime in datetimes:
        date_string, appointment_time_id = _datetime.split("-")
        date = datetime.strptime(date_string, "%d/%m/%Y")
        start_of_week = date - timedelta(days=date.weekday())
        if start_of_week < datetime.now():
            raise CreateAppointmentException

        appointment = Appointment(
            date=date,
            appointment_time_id=appointment_time_id,
            doctor_id=current_user.id,
            status=AppointmentStatus.AVAILABLE
        )
        appointments.append(appointment)

    try:
        Appointment.query.filter(
            Appointment.doctor_id == current_user.id,
            Appointment.date >= datetime.strptime(
                days_of_week[0], "%d/%m/%Y").date(),
            Appointment.date <= datetime.strptime(
                days_of_week[6], "%d/%m/%Y").date()).delete()
        db.session.add_all(appointments)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise CreateAppointmentException
