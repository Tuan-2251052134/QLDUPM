from flask_login import current_user
from enums.user_role import UserRole
from flask import redirect
from functools import wraps


def is_doctor(next):
    @wraps(next)
    def check():
        if not current_user.is_authenticated or current_user.role != UserRole.DOCTOR:
            return redirect('/user/login')
        return next()
    return check
