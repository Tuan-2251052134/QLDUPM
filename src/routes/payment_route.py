from flask import Blueprint, render_template
from filters.auth_filter import is_patient

blueprint = Blueprint('payment', __name__)


@blueprint.route('/payment', methods=['GET'])
@is_patient
def get_payment_page():
    return render_template('patient/payment.html')



@blueprint.route('/payment/success', methods=['GET'])
@is_patient
def get_payment_success_page():
    return render_template('patient/payment_result.html')


@blueprint.route('/payment/fail', methods=['GET'])
@is_patient
def get_payment_fail_page():
    return render_template('patient/payment_result.html')
