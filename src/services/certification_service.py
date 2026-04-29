from models import Certification
from cloudinary import uploader
from flask_login import current_user
from exceptions import CloudinaryException
from configs.db_config import db


def get_certifcation_by_id(id):
    return Certification.query.filter_by(id=id).first()


def delete_cert(certfication):
    db.session.delete(certfication)
    db.session.commit()


def create_cert(user, request):
    certification_name = request.form.get("certificationName")
    try:
        certification_file = request.files.get('certification')
        result = uploader.upload(certification_file)
        url = result.get('secure_url')
        certification = Certification(
            url=url, doctor_info_id=user.id, name=certification_name)
        db.session.add(certification)
    except Exception as ex:
        raise CloudinaryException()


def create_or_update_certs(request):
    certifications_file = request.files.getlist("certificationsFile")
    certifications_id = request.form.getlist("certificationsId")
    certifications_name = request.form.getlist("certificationsName")

    certifications = []
    for index in range(len(certifications_name)):
        if certifications_file[index].filename:
            try:
                result = uploader.upload(certifications_file[index])
                url = result.get('secure_url')
                certifications.append(Certification(
                    id=(int(
                        certifications_id[index]) if certifications_id[index] != "" else None),
                    url=url,
                    name=certifications_name[index],
                    doctor_info_id=current_user.id))

            except Exception as ex:
                print(ex)
                raise CloudinaryException()
    db.session.add_all(certifications)
