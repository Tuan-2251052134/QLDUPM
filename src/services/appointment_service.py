from datetime import timedelta, datetime
from enums.appointment_status import AppointmentStatus
from models import Appointment, AppointmentTime
from configs.db_config import db
from exceptions import CreateAppointmentException
from services import payment_service


def get_days_of_week(start_date):
    start_date = datetime.strptime(
        start_date, "%d/%m/%Y") if start_date else datetime.now()
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


def get_appointments(days_of_week, user_id, key):
    registered_appointments = db.session.query(Appointment, AppointmentTime).filter(
        getattr(Appointment, key) == user_id,
        Appointment.date >= datetime.strptime(
            days_of_week[0], "%d/%m/%Y").date(),
        Appointment.date <= datetime.strptime(
            days_of_week[6], "%d/%m/%Y").date()
    ).join(AppointmentTime, Appointment.appointment_time_id == AppointmentTime.id).all()

    registered_appointment_map = {}

    for registered_appointment in registered_appointments:
        registered_appointment_map[
            f"{registered_appointment[0].date.strftime("%d/%m/%Y")}-{registered_appointment[1].id}"] = registered_appointment[0].id if registered_appointment[0].status != AppointmentStatus.BOOKED else ["x", registered_appointment[0].symptom, registered_appointment[0].doctor_id]

    return registered_appointment_map


def get_appointments_by_patient(start_date, user_id):
    start_date_previous_week, days_of_week, start_date_next_week, _ = get_days_of_week(
        start_date=start_date)
    return days_of_week, get_appointments(
        days_of_week=days_of_week, user_id=user_id, key="patient_id"), start_date_previous_week, start_date_next_week


def get_appointments_by_doctor(start_date, user_id):
    start_date_previous_week, days_of_week, start_date_next_week, show_warning = get_days_of_week(
        start_date=start_date)
    return days_of_week, get_appointments(days_of_week, user_id, "doctor_id"), start_date_previous_week, start_date_next_week, show_warning


def create_appointments(datetimes, start_date, user_id):
    _, days_of_week, _, _ = get_days_of_week(start_date=start_date)
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
            doctor_id=user_id,
            status=AppointmentStatus.AVAILABLE
        )
        appointments.append(appointment)

    try:
        Appointment.query.filter(
            Appointment.doctor_id == user_id,
            Appointment.date >= datetime.strptime(
                days_of_week[0], "%d/%m/%Y").date(),
            Appointment.date <= datetime.strptime(
                days_of_week[6], "%d/%m/%Y").date(),
            Appointment.status != AppointmentStatus.BOOKED).delete()
        db.session.add_all(appointments)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise CreateAppointmentException


def apply_appointment(id, patient_id, symptom):
    try:
        appointment = Appointment.query.filter_by(id=id).first()
        appointment.patient_id = patient_id
        appointment.symptom = symptom
        appointment.status = AppointmentStatus.BOOKED
        db.session.add(appointment)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        raise ex

    session = payment_service.create_session(appointment_id=appointment.id)
    return session


def get_appointment_by_id(id):
    return Appointment.query.filter_by(id=id).first()
