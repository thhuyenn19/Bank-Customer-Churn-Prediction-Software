# Form implementation generated from reading ui file 'D:\2nd\HK4\MACHINE LEARNING\CK\SourceCode\UI\ConnectDatabase.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 479)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/logo_app.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BG1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.BG1.setGeometry(QtCore.QRect(10, 30, 631, 371))
        self.BG1.setStyleSheet("background-color: rgb(2, 139, 200);")
        self.BG1.setObjectName("BG1")
        self.BG2 = QtWidgets.QWidget(parent=self.BG1)
        self.BG2.setGeometry(QtCore.QRect(30, 30, 571, 311))
        self.BG2.setStyleSheet("background-color: rgb(81, 209, 244);")
        self.BG2.setObjectName("BG2")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.BG2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 331, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelConnect = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.labelConnect.setStyleSheet("font: 75 8pt \"Vinhan\";\n"
"color: rgb(129, 179, 120);")
        self.labelConnect.setObjectName("labelConnect")
        self.verticalLayout.addWidget(self.labelConnect)
        self.label_4 = QtWidgets.QLabel(parent=self.BG2)
        self.label_4.setGeometry(QtCore.QRect(330, 0, 241, 311))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/image/connectdatabase.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.formLayoutWidget = QtWidgets.QWidget(parent=self.BG2)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 60, 251, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.labelServer = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.labelServer.setStyleSheet("font: 75 11pt \"Vinhan\";")
        self.labelServer.setObjectName("labelServer")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelServer)
        self.lineEditServer = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Vinhan")
        self.lineEditServer.setFont(font)
        self.lineEditServer.setObjectName("lineEditServer")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditServer)
        self.labelPort = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.labelPort.setStyleSheet("font: 75 11pt \"Vinhan\";")
        self.labelPort.setObjectName("labelPort")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelPort)
        self.lineEditPort = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Vinhan")
        self.lineEditPort.setFont(font)
        self.lineEditPort.setObjectName("lineEditPort")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditPort)
        self.labelDatabase = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.labelDatabase.setStyleSheet("font: 75 11pt \"Vinhan\";")
        self.labelDatabase.setObjectName("labelDatabase")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelDatabase)
        self.lineEditDatabase = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Vinhan")
        self.lineEditDatabase.setFont(font)
        self.lineEditDatabase.setObjectName("lineEditDatabase")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditDatabase)
        self.labelUser = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.labelUser.setStyleSheet("font: 75 11pt \"Vinhan\";\n"
"")
        self.labelUser.setObjectName("labelUser")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelUser)
        self.lineEditUser = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Vinhan")
        self.lineEditUser.setFont(font)
        self.lineEditUser.setObjectName("lineEditUser")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditUser)
        self.labelPassword = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.labelPassword.setStyleSheet("font: 75 11pt \"Vinhan\";")
        self.labelPassword.setObjectName("labelPassword")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelPassword)
        self.lineEditPassword = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Vinhan")
        self.lineEditPassword.setFont(font)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditPassword)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(4, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(8, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem3)
        self.label = QtWidgets.QLabel(parent=self.BG2)
        self.label.setGeometry(QtCore.QRect(30, 60, 16, 21))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/server.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.BG2)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 16, 20))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/port.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.BG2)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 16, 21))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/database.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(parent=self.BG2)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 16, 20))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/user.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.BG2)
        self.label_6.setGeometry(QtCore.QRect(30, 220, 16, 21))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/password.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.BG2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 250, 231, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonConnect = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButtonConnect.setStyleSheet("QPushButton {\n"
"    background-color: rgb(254, 190, 5);\n"
"    color:rgb(255, 255, 255);\n"
"    text-align:center;\n"
"    font: 75 12pt \"Vinhan\";\n"
"    height:30px;\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    border-radius:10px;\n"
"}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/connect.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonConnect.setIcon(icon1)
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.horizontalLayout.addWidget(self.pushButtonConnect)
        self.pushButtonClose = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButtonClose.setStyleSheet("QPushButton {\n"
"    background-color: rgb(254, 190, 5);\n"
"    color:rgb(255, 255, 255);\n"
"    text-align:center;\n"
"    font: 75 12pt \"Vinhan\";\n"
"    height:30px;\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    border-radius:10px;\n"
"}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("D:\\2nd\\HK4\\MACHINE LEARNING\\CK\\SourceCode\\UI\\images/ConnectDatabase/icon/close.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonClose.setIcon(icon2)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout.addWidget(self.pushButtonClose)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButtonClose.clicked.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ChurnCast - ConnectWindow"))
        self.labelConnect.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600; color:#febe05;\">CONNECTION SETTING</span></p></body></html>"))
        self.labelServer.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">Server:</span></p></body></html>"))
        self.lineEditServer.setText(_translate("MainWindow", "localhost"))
        self.labelPort.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">Port:</span></p></body></html>"))
        self.lineEditPort.setText(_translate("MainWindow", "3306"))
        self.labelDatabase.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ffffff;\">Database:</span></p></body></html>"))
        self.lineEditDatabase.setText(_translate("MainWindow", "bankchurn"))
        self.labelUser.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">User:</span></p></body></html>"))
        self.lineEditUser.setText(_translate("MainWindow", "root"))
        self.labelPassword.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ffffff;\">Password:</span></p></body></html>"))
        self.lineEditPassword.setText(_translate("MainWindow", "@Obama123"))
        self.pushButtonConnect.setText(_translate("MainWindow", "Connect"))
        self.pushButtonClose.setText(_translate("MainWindow", "Close"))
