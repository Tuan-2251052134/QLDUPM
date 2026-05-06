from models import Hospital

def get_hospital():
    return Hospital.query.all()