from Connectors.Connector import Connector
from PyQt6.QtWidgets import QMessageBox, QMainWindow

from UI.ResetPassword import Ui_MainWindow


class ResetPasswordEx(Ui_MainWindow):
    def __init__(self, username, phone, connector=None):
        super().__init__()
        self.connector = Connector()
        self.username = username
        self.phone = phone

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButtonResetPassword.clicked.connect(self.resetPassword)

    def connectDatabase(self):
        self.connector.server = "localhost"
        self.connector.port = 3306
        self.connector.database = "bankchurn"
        self.connector.username = "root"
        self.connector.password = "@Obama123"
        self.connector.connect()


    def show(self):
        self.MainWindow.show()

    def resetPassword(self):
        new_password = self.lineEditNewPassword.text()
        confirm_password = self.lineEditConfirmPassword.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self.MainWindow, "Error", "Please fill in both New Password and Confirm Password fields.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self.MainWindow, "Error", "New Password and Confirm Password do not match.")
            return

        self.connectDatabase()
        update_sql = f"UPDATE account SET pass_word = '{new_password}' WHERE user_name = '{self.username}' AND phone = '{self.phone}'"
        self.connector.queryDataset(update_sql)
        self.connector.commit()
        QMessageBox.information(self.MainWindow, "Success", "Password has been reset successfully.")

        self.closeWindow()

    def showLogin(self):
        from UI.LoginEx import LoginEx
        self.login_window = QMainWindow()
        self.login_ui = LoginEx()
        self.login_ui.setupUi(self.login_window)
        self.login_window.show()

    def closeWindow(self):
        self.showLogin()
        self.MainWindow.close()
