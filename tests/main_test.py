import pytest
from pytest_mock import MockerFixture

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

    def test_setup_ui(self, mocker: MockerFixture):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'setup_ui')

        window.setup_ui()
    
        assert spy.call_count == 1

    def test_setup_ui_settings(self, mocker: MockerFixture):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'setup_ui_settings')

        window.setup_ui_settings()
    
        assert spy.call_count == 1
        
    def test_connect_events(self, mocker: MockerFixture):
        mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        spy = mocker.spy(window, 'connect_events')

        window.connect_events()
    
        assert spy.call_count == 1

    def test_get_openconnect_args(self, mocker: MockerFixture):
        mocked_window = mocker.patch.object(main, 'MainWindow')
        window = main.MainWindow()
        mocker.patch('PyQt5.QtWidgets.QLineEdit.text', return_value='123')
        expected = ['--user=123', '--passwd-on-stdin', '--authgroup=123', '123']
        
        spy = mocker.spy(obj=main.MainWindow, name='get_openconnect_args')
        mocker.patch('main.MainWindow.get_openconnect_args', return_value=expected)
        
        # window.get_openconnect_args()
        mocked_window.open_connect_args()
        
        print(mocked_window.call_args)
        print(spy.return_value)
        
        assert mocked_window.call_args