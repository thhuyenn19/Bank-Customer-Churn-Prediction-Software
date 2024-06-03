from Connectors.Connector import Connector
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtCore import QTimer
import random
import string

from UI.ForgotPassword import Ui_MainWindow


class ForgotPasswordEx(Ui_MainWindow):
    def __init__(self, connector=None):
        super().__init__()
        self.connector = Connector()
        self.reset_attempts = 0
        self.code_attempts = 0
        self.username = ""
        self.phone = ""
        self.reset_password_window = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButtonSendCode.clicked.connect(self.sendCode)
        self.pushButtonChange.clicked.connect(self.forgotPassword)
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.updateMessageBox)

    def connectDatabase(self):
        self.connector.server = "localhost"
        self.connector.port = 3306
        self.connector.database = "bankchurn"
        self.connector.username = "root"
        self.connector.password = "@Obama123"
        self.connector.connect()

    def show(self):
        self.MainWindow.show()

    def sendCode(self):
        self.username = self.lineEditUserName.text()
        self.phone = self.lineEditPhone.text()

        if not self.username or not self.phone:
            QMessageBox.warning(self.MainWindow, "Warning", "Both username and phone fields must be filled to reset password.")
            return

        self.connectDatabase()
        sql = 'SELECT user_name, phone FROM account'
        self.account = self.connector.queryDataset(sql)
        user_info = self.account.loc[(self.account['user_name'] == self.username) & (self.account['phone'] == self.phone)]

        if user_info.empty:
            self.reset_attempts += 1
            if self.reset_attempts >= 3:
                QMessageBox.critical(self.MainWindow, "Error", "Incorrect information entered more than 3 times. The application will exit.")
                self.MainWindow.close()
            else:
                QMessageBox.warning(self.MainWindow, "Warning", f"Incorrect username or phone. You have {3 - self.reset_attempts} attempts left.")
            return

        self.code = ''.join(random.choice(string.digits) for _ in range(6))

        self.seconds_left = 60
        self.message_box = QMessageBox(self.MainWindow)
        self.message_box.setWindowTitle("Confirmation Code")
        self.message_box.setText(
            f"<b>Mã code: {self.code}</b><br><br>Mã code có hiệu lực trong vòng 1 phút.<br><br>Thời gian còn lại: {self.seconds_left}s")
        self.message_box.show()

        self.timer.start(1000)

    def updateMessageBox(self):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            self.message_box.setText(
                f"<b>Mã code: {self.code}</b><br><br>Mã code có hiệu lực trong vòng 1 phút.<br><br>Thời gian còn lại: {self.seconds_left}s")
        else:
            self.message_box.close()
            self.timer.stop()

    def forgotPassword(self):
        confirmcode = self.lineEditConfirmCode.text()

        if confirmcode != self.code:
            self.code_attempts += 1
            if self.code_attempts >= 3:
                QMessageBox.critical(self.MainWindow, "Error", "Incorrect confirmation code entered more than 3 times. The application will exit.")
                self.MainWindow.close()
            else:
                QMessageBox.warning(self.MainWindow, "Warning", f"Incorrect confirmation code. You have {3 - self.code_attempts} attempts left.")
            return

        self.showReset()
        self.MainWindow.close()

    def showReset(self):
        from UI.ResetPasswordEx import ResetPasswordEx
        reset_password_window = QMainWindow()
        try:
            self.reset_password_ui = ResetPasswordEx(self.username, self.phone)
            self.reset_password_ui.setupUi(reset_password_window)
            reset_password_window.show()
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Warning", f"Both Username and Phone must have value!")