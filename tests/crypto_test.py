import pytest
from crypto import Crypto

from PyQt5.QtCore import QSettings


@pytest.mark.smoke
class TestCrypto:
    
    @pytest.fixture
    def settings(self):
        return QSettings('settings_test.ini', QSettings.Format.IniFormat)
    
    def test_encrypt(self, mocker, settings):
        mocker.patch('PyQt5.QtCore.QSettings.value', return_value=b's0fGjTjqikbfoQBoLS_gHY3i8xoOMjchkeSREUsU750=')
        crypto = Crypto(settings)
        actual = crypto.encrypt('123')
        expected = b'gAAAAABiVLr-m8Vqo8h-ZUdzfIz0mSr4TFNO0zF7CNdi8WMwIQMlT_ySs5Z3Rl5UMdEUTxJ_fVljsxK17ZB7Of_GqQw36bAGzw=='
        
        assert expected, actual

    def test_decrypt(self, mocker, settings):
        mocker.patch('PyQt5.QtCore.QSettings.value', return_value=b's0fGjTjqikbfoQBoLS_gHY3i8xoOMjchkeSREUsU750=')
        crypto = Crypto(settings)
        actual = crypto.decrypt(b'gAAAAABiVLr-m8Vqo8h-ZUdzfIz0mSr4TFNO0zF7CNdi8WMwIQMlT_ySs5Z3Rl5UMdEUTxJ_fVljsxK17ZB7Of_GqQw36bAGzw==')
        expected = "123"
        
        assert expected, actual