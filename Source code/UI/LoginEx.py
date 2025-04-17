from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QMainWindow, QApplication
from UI.Login import Ui_MainWindow
from Connectors.Connector import Connector
from UI.MainWindowEx import MainWindowEx
import sys
from UI.ForgotPasswordEx import ForgotPasswordEx

class LoginEx(Ui_MainWindow):
    def __init__(self, connector=None):
        self.connector = Connector()
        self.login_attempts = 0
        self.main_window = None  # Keep a reference to the main window

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButtonLogin.clicked.connect(self.processLogin)
        self.pushButtonForgot.clicked.connect(self.showForgotPasswordWindow)

    def connectDatabase(self):
        self.connector.server = "localhost"
        self.connector.port = 3306
        self.connector.database = "bankchurn"
        self.connector.username = "root"
        self.connector.password = "@Obama123"
        self.connector.connect()

    def processLogin(self):
        username = self.lineEditUserName.text()
        password = self.lineEditPassWord.text()

        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Warning", "Both username and password fields must be filled.")
            return

        self.connectDatabase()
        sql = 'SELECT user_name, pass_word, employee_name FROM account'
        self.account = self.connector.queryDataset(sql)
        user_record = self.account.loc[self.account['user_name'] == username]

        if not user_record.empty and password == user_record['pass_word'].values[0]:
            self.MainWindow.close()
            employeename = user_record['employee_name'].values[0]

            self.main_window = QMainWindow()
            self.Gui = MainWindowEx(employeename)
            self.Gui.setupUi(self.main_window)
            self.main_window.show()
        else:
            self.login_attempts += 1
            self.lineEditPassWord.clear()
            if self.login_attempts >= 3:
                QMessageBox.critical(self.MainWindow, "Error", "You have entered the incorrect password more than 3 times. The application will exit.")
                sys.exit()
            else:
                QMessageBox.warning(self.MainWindow, "Warning", f"Incorrect login information. You have {3 - self.login_attempts} attempts left.")

    def show(self):
        self.MainWindow.show()

    def showForgotPasswordWindow(self):
        self.MainWindow.close()
        self.forgot_password_window = ForgotPasswordEx()
        forgot_password_mainwindow = QMainWindow()
        self.forgot_password_window.setupUi(forgot_password_mainwindow)
        forgot_password_mainwindow.show()

