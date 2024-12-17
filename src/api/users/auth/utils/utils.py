import base64
import json

import bcrypt
from cryptography.fernet import Fernet

from config.settings import settings

crypt = Fernet(settings.AUTH.SECRET_KEY)


def encrypt_data(data: dict):
    encrypted_data = crypt.encrypt(json.dumps(data, default=str).encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()


def decrypt_data(data: str):
    encrypted_data = base64.urlsafe_b64decode(data.encode())
    decrypted_data = crypt.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())


def make_hash(value: str) -> bytes:
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt())


def check_hash(value: str, hashed_value: str):
    return bcrypt.checkpw(value.encode(), hashed_value.encode())
