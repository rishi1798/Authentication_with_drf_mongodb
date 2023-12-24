import bcrypt
import uuid

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    # Ensure the plain password is in bytes
    if isinstance(password, str):
        password = password.encode('utf-8')

    # Check if the hashed password is already bytes, if not, encode it
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')

    return bcrypt.checkpw(password, hashed)


def generate_auth_token():
    return str(uuid.uuid4())
