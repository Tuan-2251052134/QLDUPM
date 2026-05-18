from models import Specialty
from services import hospital_service


def get_specialties():
    return Specialty.query.all()


def get_specialties_with_hospitals():
    return get_specialties(), hospital_service.get_hospital()


def get_current_specialties():
    return Specialty.query.limit(4).all()
