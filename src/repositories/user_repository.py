from configs.db_config import db


def create_user(user):
    db.session.add(user)
    db.session.commit()
