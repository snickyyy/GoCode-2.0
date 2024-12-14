import base64
import json

import bcrypt
from cryptography.fernet import Fernet

from config.settings import settings

crypt = Fernet(settings.SECRET_KEY)


def encrypt_data(data: dict):
    encrypted_data = crypt.encrypt(json.dumps(data, default=str).encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()


def decrypt_data(data: str):
    encrypted_data = base64.urlsafe_b64decode(data.encode())
    decrypted_data = crypt.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())


def make_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
