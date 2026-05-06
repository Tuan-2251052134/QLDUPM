from configs import stripe_config


def create_session(appointment_id):
    return stripe_config.create_session(10000, appointment_id)
