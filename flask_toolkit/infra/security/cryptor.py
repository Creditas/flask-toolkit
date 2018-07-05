from aead import AEAD
from flask_toolkit.settings import CRYPTOR_PASSWORD_SECRET_KEY


class Cryptor:
    def __init__(self):
        self.__cryptor = AEAD(CRYPTOR_PASSWORD_SECRET_KEY)

    def encrypt(self, data, relative_data):
        return self.__cryptor.encrypt(
            data.encode(), relative_data.encode()
        ).decode()

    def decrypt(self, encrypted_data, relative_data):
        return self.__cryptor.decrypt(
            encrypted_data.encode(), relative_data.encode()
        ).decode()
