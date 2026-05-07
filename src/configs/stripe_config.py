import stripe
from dotenv import load_dotenv
import os
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


def create_session(amount, appointment_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "appointment_payment",
                },
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        metadata={
            "appointment_id": str(appointment_id)
        },
        success_url="http://localhost:5000/payment/success",
        cancel_url="http://localhost:5000/payment/fail",
    )
    return session
