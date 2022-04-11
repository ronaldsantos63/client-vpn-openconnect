import sys
import os
import subprocess
from typing import List

from cryptography.fernet import Fernet

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QCloseEvent


def get_executable():
    if hasattr(sys, 'frozen') or hasattr(sys, 'importers'):
        return [os.path.abspath(sys.executable)]

    if os.path.isabs(sys.argv[0]):
        path = sys.argv[0]
    else:
        path = os.path.abspath(sys.argv[0])

    return [sys.executable, path]


class MainWindow(QMainWindow):
    connect_btn: QPushButton
    disconnect_btn: QPushButton
    vpn_url_edit: QLineEdit
    user_edit: QLineEdit
    pass_edit: QLineEdit
    auth_group_edit: QLineEdit
    log: QPlainTextEdit
    process: QProcess
    sudo_passwd: str
    q_settings: QSettings
    fernet: Fernet

    def __init__(self) -> None:
        super().__init__()
        self.process = None  # Default empty value.
        self.q_settings = QSettings('settings.ini', QSettings.Format.IniFormat)
        self.check_if_openconnect_is_installed()
        self.check_user()
        self.set_masterkey()
        self.setup_ui()
        self.setup_ui_settings()
        self.connect_events()

    def check_if_openconnect_is_installed(self):
        try:
            subprocess.check_output('which openconnect', shell=True)
        except Exception:
            QMessageBox.critical(self, "Critical!", "You need to install openconnect to be able to use this software!")
            sys.exit(1)

    def set_masterkey(self):
        masterkey = self.q_settings.value("key", Fernet.generate_key(), bytes)
        self.q_settings.setValue("key", masterkey)
        self.fernet = Fernet(masterkey)

    def setup_ui_settings(self):
        self.vpn_url_edit.setText(self.decrypt(self.q_settings.value('vpn_url', None)))
        self.user_edit.setText(self.decrypt(self.q_settings.value('user', None)))
        self.pass_edit.setText(self.decrypt(self.q_settings.value('pass', None)))
        self.auth_group_edit.setText(self.decrypt(self.q_settings.value('auth_group', None)))

    def check_user(self):
        """ Checks if current user is root, otherwise, reopen with root
        """
        if os.environ.get("USER") != "root":
            pass_sudo = QInputDialog.getText(
                self,
                "Warning!",
                "Administrative access is required to run this software",
                QLineEdit.EchoMode.PasswordEchoOnEdit
            )
            executable = get_executable()
            # print(f"executable: {executable}")
            # print(f"pass sudo: {pass_sudo[0]}")
            subprocess.run(["sudo", "-S"] + executable, input=pass_sudo[0].encode())
            sys.exit(1)

    def decrypt(self, value: str) -> str:
        if not value:
            return ""
        return self.fernet.decrypt(value).decode()

    def encrypt(self, value: str) -> bytes:
        if not value:
            return b''
        return self.fernet.encrypt(value.encode())

    def setup_ui(self):
        """ Build screen with widgets"""
        self.setWindowTitle("VPN Client")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("./logo.jpg"))
        self.restoreGeometry(self.q_settings.value("geometry", QByteArray()))

        vpn_url_spacer = QSpacerItem(40, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        vpn_url_label = QLabel("Vpn url:")
        self.vpn_url_edit = QLineEdit()
        self.vpn_url_edit.setPlaceholderText("  Enter your vpn url")

        vpn_url_container = QHBoxLayout()
        vpn_url_container.addWidget(vpn_url_label)
        vpn_url_container.addSpacerItem(vpn_url_spacer)
        vpn_url_container.addWidget(self.vpn_url_edit)

        user_spacer = QSpacerItem(60, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        user_label = QLabel("User:")
        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("  Enter your vpn user")

        user_container = QHBoxLayout()
        user_container.addWidget(user_label)
        user_container.addSpacerItem(user_spacer)
        user_container.addWidget(self.user_edit)

        pass_spacer = QSpacerItem(23, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        pass_label = QLabel("Password:")
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.pass_edit.setPlaceholderText("  Enter your password vpn")

        pass_container = QHBoxLayout()
        pass_container.addWidget(pass_label)
        pass_container.addSpacerItem(pass_spacer)
        pass_container.addWidget(self.pass_edit)

        auth_group_spacer = QSpacerItem(10, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        auth_group_label = QLabel("Auth group:")
        self.auth_group_edit = QLineEdit()
        self.auth_group_edit.setPlaceholderText("  Enter your vpn auth group, keep it blank if you don't have it")

        auth_group_container = QHBoxLayout()
        auth_group_container.addWidget(auth_group_label)
        auth_group_container.addSpacerItem(auth_group_spacer)
        auth_group_container.addWidget(self.auth_group_edit)

        buttons_container = QHBoxLayout()

        self.connect_btn = QPushButton("Connect")

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setEnabled(False)

        buttons_container.addWidget(self.connect_btn)
        buttons_container.addWidget(self.disconnect_btn)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        container = QVBoxLayout()
        container.addLayout(vpn_url_container)
        container.addLayout(user_container)
        container.addLayout(pass_container)
        container.addLayout(auth_group_container)
        container.addLayout(buttons_container)
        container.addWidget(self.log)

        w = QWidget()
        w.setLayout(container)

        self.setCentralWidget(w)

    def connect_events(self):
        self.vpn_url_edit.returnPressed.connect(self.user_edit.setFocus)
        self.user_edit.returnPressed.connect(self.pass_edit.setFocus)
        self.pass_edit.returnPressed.connect(self.auth_group_edit.setFocus)

        self.vpn_url_edit.textChanged.connect(lambda x: self.q_settings.setValue('vpn_url', self.encrypt(x)))
        self.user_edit.textChanged.connect(lambda x: self.q_settings.setValue('user', self.encrypt(x)))
        self.pass_edit.textChanged.connect(lambda x: self.q_settings.setValue('pass', self.encrypt(x)))
        self.auth_group_edit.textChanged.connect(lambda x: self.q_settings.setValue('auth_group', self.encrypt(x)))

        self.connect_btn.pressed.connect(self.start_process)
        self.disconnect_btn.pressed.connect(self.stop_process)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.q_settings.setValue("geometry", self.saveGeometry())
        return super().closeEvent(a0)

    def update_text(self, message):
        self.log.appendPlainText(message)

    def start_process(self):
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)

        if self.process is None:
            self.update_text("Connecting...")
            self.process = QProcess()
            self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
            self.process.readyRead.connect(self.handle_read_ready)
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.stateChanged.connect(self.handle_state)
            self.process.finished.connect(self.process_finished)
            self.process.start("openconnect", self.get_openconnect_args())
            self.process.write(f"{self.pass_edit.text()}\n".encode())

    def get_openconnect_args(self) -> List[str]:
        if not self.vpn_url_edit.text():
            QMessageBox.warning(self, "Warning!", "You forgot to fill in the vpn url")
            return
        if not self.user_edit.text():
            QMessageBox.warning(self, "Warning!", "You forgot to fill in the vpn username")
            return
        if not self.pass_edit.text():
            QMessageBox.warning(self, "Warning!", "You forgot to fill in the vpn password")
            return
        ret = []
        ret.append(f"--user={self.user_edit.text()}")
        ret.append("--passwd-on-stdin")
        if self.auth_group_edit.text():
            ret.append(f"--authgroup={self.auth_group_edit.text()}")
        ret.append(self.vpn_url_edit.text())
        return ret

    def stop_process(self):
        self.update_text("Disconnecting...")
        self.process.kill()
        self.process.terminate()
        self.process.close()

    def handle_read_ready(self):
        print("read ready")
        data = str(self.process.readAll(), "utf-8")
        self.update_text(data)
        print(data)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf-8")
        self.update_text(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf-8")
        self.update_text(stderr)

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running'
        }
        state_name = states[state]
        print(f"State changed: {state_name}")

    def process_finished(self):
        self.update_text("Process finished")
        self.process = None
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)


if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    # os.environ["QT_DEBUG_PLUGINS"] = "1"
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
