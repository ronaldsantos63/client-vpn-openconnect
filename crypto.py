from cryptography.fernet import Fernet

from PyQt5.QtCore import QSettings


class Crypto:
    settings: QSettings
    fernet: Fernet

    def __init__(self, settings: QSettings) -> None:
        self.settings = settings
        key = settings.value('key', Fernet.generate_key(), bytes)
        self.fernet = Fernet(key)
        settings.setValue('key', key)

    def encrypt(self, value: str) -> bytes:
        if not value:
            return b''
        return self.fernet.encrypt(value.encode())

    def decrypt(self, value: bytes) -> str:
        if not value:
            return ""
        return self.fernet.decrypt(value).decode()
