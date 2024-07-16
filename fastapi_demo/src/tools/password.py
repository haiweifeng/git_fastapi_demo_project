import hashlib
from binascii import b2a_hex, a2b_hex


# windows下导包  pip install pycryptodomex
import sys

from settings.setting import SELFKEY


if sys.platform.startswith('linux'):
    from Crypto.Cipher import AES
else:
    from Cryptodome.Cipher import AES
# linux下导包  pip install pycryptodome

# from Crypto.Cipher import AES


class SelfPassWord:
    def __init__(self):
        self.key = self.handle_length(SELFKEY)
        self.mode = AES.MODE_CBC

    def handle_length(self, text):
        count = len(text)
        if count > 16:
            text = text[:16]
        elif count < 16:
            add = 16 - len(text)
            text = text + ('\0' * add)
        return text.encode()

    def encrypt(self, text):
        text = self.handle_length(text)
        cryptor = AES.new(self.key, self.mode, self.key)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext).decode()

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode().rstrip('\0')


def md5_password(pwd):
    hash = hashlib.md5()
    hash.update(bytes(pwd, encoding='utf-8'))
    return hash.hexdigest()


if __name__ == '__main__':
    s = SelfPassWord()
    print(s.encrypt("Aa111111"))