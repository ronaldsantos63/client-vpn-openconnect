import pytest
import PyQt5
from PyQt5.QtWidgets import QInputDialog
from unittest import mock
from pytest_mock import MockerFixture
from cryptography.fernet import Fernet

import main


@pytest.mark.smoke
class TestMainWindow:
    def test_get_executable(self):
        assert isinstance(main.get_executable(), list)

    def test_check_if_openconnect_is_installed(self, mocker: MockerFixture):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'check_if_openconnect_is_installed')

        window.check_if_openconnect_is_installed()

        assert spy.call_count == 1

    def test_set_masterkey(self, mocker: MockerFixture):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'set_masterkey')

        window.set_masterkey()
        
        assert spy.call_count == 1

    def test_setup_ui_settings(self, mocker: MockerFixture):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'setup_ui_settings')

        window.setup_ui_settings()
        
        assert spy.call_count == 1

    def test_check_user(self, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'check_user')

        window.check_user()
    
        assert spy.call_count == 1
