from configs import stripe_config
from configs.stripe_config import endpoint_secret
import stripe
from models import PaymentInfo
from configs.db_config import db
from services import appointment_service


def create_session(appointment_id):
    return stripe_config.create_session(11232, appointment_id)


def handle_webhook(payload, stripe_signature_header):
    event = stripe.Webhook.construct_event(
        payload,
        stripe_signature_header,
        endpoint_secret
    )
    event_type = event["type"]
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        payment_id = session.id
        appointment_id = session["metadata"]["appointment_id"]
        payment_info = PaymentInfo(
            payment_id=payment_id, appointment_id=appointment_id)
        db.session.add(payment_info)
        db.session.commit()

    elif event_type == "checkout.session.expired":
        session = event["data"]["object"]
        appointment_id = session["metadata"]["appointment_id"]
        appointment = appointment_service.get_appointment_by_id(appointment_id)
        db.session.remove(appointment)
        db.session.commit()

    elif event_type == "payment_intent.payment_failed":
        session = event["data"]["object"]
        appointment_id = session["metadata"]["appointment_id"]
        appointment = appointment_service.get_appointment_by_id(appointment_id)
        db.session.remove(appointment)
        db.session.commit()
