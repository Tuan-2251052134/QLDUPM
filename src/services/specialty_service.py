from models import Specialty


def get_specialties():
    return Specialty.query.all()
