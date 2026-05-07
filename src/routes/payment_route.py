from flask import Blueprint, render_template, request
from filters.auth_filter import is_patient
from services import payment_service

blueprint = Blueprint('payment', __name__)


@blueprint.route('/payment/success', methods=['GET'])
@is_patient
def get_payment_success_page():
    return render_template('patient/payment_result.html', isSuccess=True)


@blueprint.route('/payment/fail', methods=['GET'])
@is_patient
def get_payment_fail_page():
    return render_template('patient/payment_result.html', isSuccess=False)


@blueprint.route('/payment/webhook', methods=['POST'])
def call_back_from_bank():
    payload = request.data
    stripe_signature_header = request.headers.get("Stripe-Signature")
    try:
        payment_service.handle_webhook(payload, stripe_signature_header)
    except Exception as e:
        print(e)
        return "", 400
    return "", 200

