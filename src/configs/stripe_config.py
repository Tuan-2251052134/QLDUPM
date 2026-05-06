import stripe

stripe.api_key

def create_session(amount, appointment_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": appointment_id,
                },
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:6000/success",
        cancel_url="http://localhost:6000/fail",
    )
    return session
