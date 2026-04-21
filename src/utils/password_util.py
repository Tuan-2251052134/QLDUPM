from argon2 import PasswordHasher

ph = PasswordHasher()

def hash(raw_password):
    return ph.hash(raw_password)

def verify(password, raw_password):
    ph.verify(password, raw_password)