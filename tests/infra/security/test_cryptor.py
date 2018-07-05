from mock import patch
from flask_toolkit.infra.security.cryptor import Cryptor


class AEADMock:
    def encrypt(self, data, relative_data):
        return b'encrypted_data'

    def decrypt(self, encrypted_data, relative_data):
        return b'foo'


@patch('flask_toolkit.infra.security.cryptor.AEAD')
def test_cryptor(aead_mock):
    aead_mock.return_value = AEADMock()
    encrypt = Cryptor().encrypt(data='foo', relative_data='bar')

    decrypt = Cryptor().decrypt(encrypted_data=encrypt, relative_data='bar')

    assert decrypt == 'foo'
