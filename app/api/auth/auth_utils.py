from cryptography.fernet import Fernet

from app.constants import Auth


async def encrypt_string(value: str):
    cryp = Fernet(key=Auth.SECRET_KEY)
    encrypted_user_id = cryp.encrypt(value.encode())
    return encrypted_user_id


async def decrypt_string(encrypted_value: str):
    cryp = Fernet(key=Auth.SECRET_KEY)
    encrypted_value = encrypted_value.encode()
    print(encrypted_value)
    decrypted_value = cryp.decrypt(encrypted_value)
    return decrypted_value
