class EncryptionDecryptionModule:

    def __init__(self, secret_key: str, iv_key: str) -> None:
        self.secret_key = secret_key
        self.iv_key = iv_key

    def encrypt(self, raw_data: object):
        pass

    def decrypt(self, encrypted_data: object):
        pass
