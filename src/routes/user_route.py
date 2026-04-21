from flask import Blueprint, render_template

blueprint = Blueprint('user', __name__)

@blueprint.route('/users/login')
def get_users():
    return render_template('login.html')