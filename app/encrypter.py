import base64
import binascii
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class StringEncryptor:
    def __init__(self, password):
        self.password = password.encode()
        self.salt = os.urandom(16)
        self.key = self._derive_key(self.password, self.salt)
        self.cipher = Fernet(self.key)

    def _derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, plaintext):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        encrypted_text = self.cipher.encrypt(plaintext)
        combined = self.salt + encrypted_text
        return binascii.hexlify(combined).decode()

    def decrypt(self, hex_encrypted_text, ttl=None):
        combined = binascii.unhexlify(hex_encrypted_text)
        salt = combined[:16]
        encrypted_text = combined[16:]
        key = self._derive_key(self.password, salt)
        cipher = Fernet(key)
        try:
            if ttl:
                decrypted_text = cipher.decrypt(encrypted_text, ttl=int(ttl))
            else:
                decrypted_text = cipher.decrypt(encrypted_text)
            return decrypted_text.decode()
        except InvalidToken:
            return "Invalid or expired token"


string_encryptor = StringEncryptor(os.environ.get("SECRET", "StrongPassword"))
