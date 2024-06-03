import csv

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
import traceback
from UI.DatabaseConnectEx import DatabaseConnectEx
from UI.MainWindow import Ui_MainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from UI.ChartHandle import ChartHandle
from Model.XGB import XGBoostPredict

class MainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, employeename):
        super().__init__()
        self.databaseConnectEx = DatabaseConnectEx()
        self.databaseConnectEx.parent = self
        self.connector = None  # Ensure connector is initialized to None
        self.login_window = None
        self.XGBModel = XGBoostPredict()
        self.last_name = self.get_last_name(employeename)
        self.current_file_path = None
        self.stateLoad = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButtonView.clicked.connect(self.switch_to_ViewData)
        self.pushButtonViewIcon.clicked.connect(self.switch_to_ViewData)
        self.pushButtonPredict.clicked.connect(self.switch_to_Predict)
        self.pushButtonPredictIcon.clicked.connect(self.switch_to_Predict)
        self.pushButtonChart.clicked.connect(self.switch_to_Chart)
        self.pushButtonChartIcon.clicked.connect(self.switch_to_Chart)
        self.pushButtonGeneral.clicked.connect(self.switch_to_General)
        self.pushButtonGeneralicon.clicked.connect(self.switch_to_General)
        self.actionConnect_Database.triggered.connect(self.openDatabaseConnectUI)
        self.checkEnableWidget(False)
        self.pushButtonViewData.clicked.connect(self.viewData)
        self.checkBoxAll.stateChanged.connect(self.checkAll)
        self.pushButtonLogOut.clicked.connect(self.logout)
        self.pushButtonLogOutIcon.clicked.connect(self.logout)
        # General
        self.pushButtonImport.clicked.connect(self.openFileDialog)
        self.pushButtonPredictcsv.clicked.connect(self.trainAndDisplayPredictions)
        self.pushButtonSave.clicked.connect(self.saveTableWidgetDataToCSV)

        # Predict
        self.actionSave_New_Train_Model.triggered.connect(self.trainNewModel)
        self.actionLoad_Trained_Model.triggered.connect(self.loadTrainedModel)
        self.pushButtonResultPredict.clicked.connect(self.predictResult)
        self.plainTextEditResult.setPlainText("RESULT WILL DISPLAY HERE")
        self.plainTextEditResult.setReadOnly(True)
        self.pushButtonResultClear.clicked.connect(self.clearInfo)
        # View Chart
        self.setupPlot()
        self.pushButtonCreditScore.clicked.connect(self.showCreditScore)
        self.pushButtonCountry.clicked.connect(self.showCountry)
        self.pushButtonChurnByGender.clicked.connect(self.showGender)
        self.pushButtonAge.clicked.connect(self.showAge)
        self.pushButtonTenure.clicked.connect(self.showTenure)
        self.pushButtonChurnByProductsNumber.clicked.connect(self.showProduct)
        self.pushButtonChurnByCreditCard.clicked.connect(self.showCredictCard)
        self.pushButtonChurnByActiveMember.clicked.connect(self.showActive)
        self.pushButtonChurn.clicked.connect(self.showChurn)

        self.label_3.setText(f"Hello {self.last_name}")

    def get_last_name(self, full_name):
        return full_name.split()[-1]

    def switch_to_ViewData(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_Predict(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_Chart(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_General(self):
        self.stackedWidget.setCurrentIndex(3)

    def checkEnableWidget(self, enable):
        # View Data
        self.checkBoxAll.setEnabled(enable)
        # self.pushButtonViewData.setEnabled(enable)
        self.checkBoxCusID.setEnabled(enable)
        self.checkBoxCreCard.setEnabled(enable)
        self.checkBoxCountry.setEnabled(enable)
        self.checkBoxGender.setEnabled(enable)
        self.checkBoxAge.setEnabled(enable)
        self.checkBoxTenure.setEnabled(enable)
        self.checkBoxBalance.setEnabled(enable)
        self.checkBoxProNumber.setEnabled(enable)
        self.checkBoxCreScore.setEnabled(enable)
        self.checkBoxActive.setEnabled(enable)
        self.checkBoxSalary.setEnabled(enable)
        self.checkBoxChurn.setEnabled(enable)
        # Predict
        self.lineEditCreditScore.setEnabled(enable)
        self.comboBoxCountry.setEnabled(enable)
        self.comboBoxGender.setEnabled(enable)
        self.lineEditAge.setEnabled(enable)
        self.lineEditTenure.setEnabled(enable)
        self.lineEditBalance.setEnabled(enable)
        self.lineEditProductsNumber.setEnabled(enable)
        self.comboBoxCreditCard.setEnabled(enable)
        self.comboBoxActive.setEnabled(enable)
        self.lineEditSalary.setEnabled(enable)
        # View Chart
        # self.pushButtonCreditScore.setEnabled(enable)
        # self.pushButtonCountry.setEnabled(enable)
        # self.pushButtonChurnByGender.setEnabled(enable)
        # self.pushButtonAge.setEnabled(enable)
        # self.pushButtonTenure.setEnabled(enable)
        # self.pushButtonChurnByProductsNumber.setEnabled(enable)
        # self.pushButtonChurnByCreditCard.setEnabled(enable)
        # self.pushButtonChurnByActiveMember.setEnabled(enable)
        # self.pushButtonChurn.setEnabled(enable)
        # system
        self.actionSave_New_Train_Model.setEnabled(enable)
        self.actionLoad_Trained_Model.setEnabled(enable)
        if enable:
            self.label_12.setText("Database Connected!")
        else:
            self.label_12.setText("No Database Connection!")
    def openDatabaseConnectUI(self):
        dbwindow = QMainWindow()
        self.databaseConnectEx.setupUi(dbwindow)
        self.databaseConnectEx.show()

    def set_connector(self, connector):
        self.connector = connector

    def checkAll(self, state):
        checkboxes = [
            self.checkBoxCusID, self.checkBoxCreCard, self.checkBoxCountry, self.checkBoxGender, self.checkBoxAge,
            self.checkBoxTenure, self.checkBoxBalance, self.checkBoxProNumber, self.checkBoxCreScore,
            self.checkBoxActive, self.checkBoxSalary, self.checkBoxChurn
        ]
        if state == Qt.CheckState.Checked:
            for checkbox in checkboxes:
                checkbox.setChecked(True)

    def viewData(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return

        selected_columns = []
        if self.checkBoxCusID.isChecked():
            selected_columns.append("customer_id")
        if self.checkBoxCreCard.isChecked():
            selected_columns.append("credit_card")
        if self.checkBoxCountry.isChecked():
            selected_columns.append("country")
        if self.checkBoxGender.isChecked():
            selected_columns.append("gender")
        if self.checkBoxAge.isChecked():
            selected_columns.append("age")
        if self.checkBoxTenure.isChecked():
            selected_columns.append("tenure")
        if self.checkBoxBalance.isChecked():
            selected_columns.append("balance")
        if self.checkBoxProNumber.isChecked():
            selected_columns.append("products_number")
        if self.checkBoxCreScore.isChecked():
            selected_columns.append("credit_score")
        if self.checkBoxActive.isChecked():
            selected_columns.append("active_member")
        if self.checkBoxSalary.isChecked():
            selected_columns.append("estimated_salary")
        if self.checkBoxChurn.isChecked():
            selected_columns.append("churn")

        if self.checkBoxAll.isChecked():
            if len(selected_columns) > 0:
                QMessageBox.warning(self.MainWindow, "Selection Error", "You have selected 'All columns'. Please deselect other columns.")
                return
            selected_columns = ["customer_id", "credit_card", "country", "gender", "age", "tenure", "balance",
                                "products_number", "credit_score", "active_member", "estimated_salary", "churn"]

        if not selected_columns:
            QMessageBox.warning(self.MainWindow, "No selection", "Please select at least one column.")
            return

        query = f"SELECT {', '.join(selected_columns)} FROM Data"

        try:
            self.connector.connect()
            df = self.connector.queryDataset(query)
            if df is not None:
                self.tableWidgetViewData.setRowCount(0)
                self.tableWidgetViewData.setColumnCount(len(df.columns))
                self.tableWidgetViewData.setHorizontalHeaderLabels(df.columns)

                for row_number, row_data in df.iterrows():
                    self.tableWidgetViewData.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidgetViewData.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Database Error", str(e))
            traceback.print_exc()

    def logout(self):
        self.MainWindow.close()
        self.showLogin()

    def showLogin(self):
        if not self.login_window:
            from UI.LoginEx import LoginEx
            self.login_window = LoginEx()
            self.login_window.setupUi(self.MainWindow)
        self.login_window.show()

# Predict
    def getPredictText(self):
        if not self.lineEditCreditScore.text() or not self.lineEditAge.text() or not self.lineEditTenure.text() or not self.lineEditBalance.text() or not self.lineEditProductsNumber.text() or not self.lineEditSalary.text():
            QMessageBox.warning(self, "Warning", "Please fill in all the information ")
            return
        try:
            self.credit_score = int(self.lineEditCreditScore.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Credit Score must be an integer!")
            return None
        self.country = self.comboBoxCountry.currentText()
        self.gender = self.comboBoxGender.currentText()
        try:
            self.age = int(self.lineEditAge.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Age must be an integer!")
            return None
        try:
            self.tenure = int(self.lineEditTenure.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Tenure must be an integer!")
            return None
        try:
            self.balance = float(self.lineEditBalance.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Balance must be a float!")
            return None
        try:
            self.products_number = int(self.lineEditProductsNumber.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Products Number must be an integer!")
            return None
        self.credit_card = 1 if self.comboBoxCreditCard.currentText() == 'Yes' else 0
        self.active_member = 1 if self.comboBoxActive.currentText() == 'Yes' else 0
        try:
            self.estimated_salary = float(self.lineEditSalary.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Estimated Salary must be a float")
            return None
        self.customer = {"credit_score":self.credit_score, "country": self.country, "gender": self.gender, "age": self.age, "tenure":self.tenure, "balance":self.balance,"products_number":self.products_number,"credit_card": self.credit_card, "active_member":self.active_member, "estimated_salary":self.estimated_salary}
        return self.customer

    def predictResult(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        if self.stateLoad is None:
            QMessageBox.warning(self.MainWindow, "Error", "No model loaded")
            return
        self.XGBModel = XGBoostPredict(self.connector)
        conn = self.connector.connect()
        # if self.filename is not None:
        customer_data = self.getPredictText()
        if not customer_data:
            return
        churn,pred = self.XGBModel.predict(customer_data,conn,self.filename)
        self.plainTextEditResult.setPlainText(f"""
        Customer Data: ({self.credit_score};{self.country};{self.gender};{self.age};{self.tenure};{self.balance};{self.products_number};{self.credit_card};{self.active_member};{self.estimated_salary})
        Predict Result: This customer may {'CHURN' if pred == 1 else 'NOT CHURN'}
        Probability of customers churn: {churn*100:.2f}%
        """)

    def clearInfo(self):
        self.lineEditCreditScore.clear()
        self.lineEditAge.clear()
        self.lineEditTenure.clear()
        self.lineEditBalance.clear()
        self.lineEditProductsNumber.clear()
        self.lineEditSalary.clear()

        self.comboBoxCountry.setCurrentIndex(0)
        self.comboBoxGender.setCurrentIndex(0)
        self.comboBoxCreditCard.setCurrentIndex(0)
        self.comboBoxActive.setCurrentIndex(0)

        self.plainTextEditResult.clear()

    def trainNewModel(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        conn = self.connector.connect()
        self.XGBModel.processTrain(conn)

    def loadTrainedModel(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        conn = self.connector.connect()
        self.filename = self.XGBModel.loadTrainedModel(conn)
        if self.filename is not None:
            self.stateLoad = "Okay"

# View Chart
    def setupPlot(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)
        # adding tool bar to the layout
        self.verticalLayout_7.addWidget(self.toolbar)
        # adding canvas to the layout
        self.verticalLayout_7.addWidget(self.canvas)

    def clearFigure(self):
        self.figure.clear()

    def showDataIntoTableWidget(self, df):
        # Xóa dữ liệu cũ trong tableWidget
        self.clearTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(df.columns))

        # Đặt tiêu đề cho các cột
        for i, column_name in enumerate(df.columns):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(column_name))

        # Thêm dữ liệu vào tableWidget
        for index, row_data in df.iterrows():
            row_number = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_number)
            for j, value in enumerate(row_data):
                self.tableWidget.setItem(row_number, j, QTableWidgetItem(str(value)))

    def clearTableWidget(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

# showCreditScore
    def showCreditScore(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            score_counts = self.connector.queryDataset(
                'SELECT credit_score, COUNT(*) AS count FROM bankchurn.data GROUP BY credit_score ORDER BY credit_score')
        except Exception as e:
            return None

        if score_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(score_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartCreditScore(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# Show Country
    def showCountry(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            country_counts = self.connector.queryDataset('SELECT country, COUNT(*) AS count FROM bankchurn.data GROUP BY country ORDER BY country')
        except Exception as e:
            return None

        if country_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(country_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartCountry(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# ShowGender
    def showGender(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            gender_counts = self.connector.queryDataset('SELECT gender, COUNT(*) AS count FROM bankchurn.data GROUP BY gender ORDER BY gender')
        except Exception as e:
            return None

        if gender_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(gender_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartGender(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# ShowAge
    def showAge(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            age_counts = self.connector.queryDataset('SELECT age, COUNT(*) AS count FROM bankchurn.data GROUP BY age ORDER BY age')
        except Exception as e:
            return None

        if age_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(age_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartAge(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()

# ShowTenure
    def showTenure(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            tenure_counts = self.connector.queryDataset('SELECT tenure, COUNT(*) AS count FROM bankchurn.data GROUP BY tenure ORDER BY tenure')
        except Exception as e:
            return None

        if tenure_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(tenure_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartTenure(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# ShowProduct
    def showProduct(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            products_number_counts = self.connector.queryDataset('SELECT products_number, COUNT(*) AS count FROM bankchurn.data GROUP BY products_number ORDER BY products_number')
        except Exception as e:
            return None

        if products_number_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(products_number_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartProduct(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# ShowCreditCard
    def showCredictCard(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            credit_card_counts = self.connector.queryDataset('SELECT credit_card, COUNT(*) AS count FROM bankchurn.data GROUP BY credit_card ORDER BY credit_card')
        except Exception as e:
            return None

        if credit_card_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(credit_card_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartCreditCard(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# ShowActive
    def showActive(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            active_member_counts = self.connector.queryDataset('SELECT active_member, COUNT(*) AS count FROM bankchurn.data GROUP BY active_member ORDER BY active_member')
        except Exception as e:
            return None

        if active_member_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(active_member_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartActive(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# Show Churn
    def showChurn(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            # Thử kết nối đến cơ sở dữ liệu
            self.connector.connect()
            # Thực hiện truy vấn để lấy dữ liệu
            df = self.connector.queryDataset('SELECT * FROM bankchurn.data')
            # Nếu có dữ liệu, xử lý và trả về kết quả
            churn_counts = self.connector.queryDataset('SELECT churn, COUNT(*) AS count FROM bankchurn.data GROUP BY churn ORDER BY churn')
        except Exception as e:
            return None

        if churn_counts is not None:
            # Xóa biểu đồ cũ trước khi vẽ biểu đồ mới
            self.clearFigure()
            # Hiển thị dữ liệu trong tableWidget
            self.showDataIntoTableWidget(churn_counts)
            # Tạo biểu đồ từ dữ liệu và hiển thị trên figure
            chartHandle = ChartHandle(df)
            chartHandle.showChartChurn(self.figure)
            # Vẽ biểu đồ trên canvas để hiển thị
            self.canvas.draw()
# General
    def openFileDialog(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        filters = "CSV files (*.csv);;All files(*)"
        filename, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Open CSV File",
            "",
            filters
        )
        if filename:
            self.current_file_path = filename
            self.loadDataFromFile(filename)
        else:
            QMessageBox.critical(self, "Error", "Choose a File!")

    def loadDataFromFile(self, file_path):
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            if df is not None:
                self.tableWidgetView.setRowCount(0)
                self.tableWidgetView.setColumnCount(len(df.columns))
                self.tableWidgetView.setHorizontalHeaderLabels(df.columns)

                for row_number, row_data in df.iterrows():
                    self.tableWidgetView.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidgetView.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.critical(self, "File Error", str(e))
            traceback.print_exc()

    def trainAndDisplayPredictions(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        try:
            if not self.current_file_path:
                QMessageBox.warning(self, "File Error", "No file selected.")
                return
            if self.connector is None:
                QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
                return

            conn = self.connector.connect()
            self.XGBModel.processTrain(conn)
            predictions_df = self.XGBModel.predict_customers(self.current_file_path)
            # customer_df = pd.read_csv(self.current_file_path)
            if predictions_df is not None:
                self.clearTableWidget()
                self.tableWidgetView.setRowCount(0)
                self.tableWidgetView.setColumnCount(len(predictions_df.columns))
                self.tableWidgetView.setHorizontalHeaderLabels(predictions_df.columns)

                for row_number, row_data in predictions_df.iterrows():
                    self.tableWidgetView.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        item = QTableWidgetItem()
                        if isinstance(data, float):
                            item.setData(Qt.ItemDataRole.DisplayRole, "{:.2f}".format(data))
                        else:
                            # Chuyển đổi dữ liệu thành chuỗi
                            item.setData(Qt.ItemDataRole.DisplayRole, str(data))
                        self.tableWidgetView.setItem(row_number, column_number, item)

            QMessageBox.information(self.MainWindow, "Information", "Train successfull!")

        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", str(e))
            traceback.print_exc()

    def saveTableWidgetDataToCSV(self):
        if self.connector is None:
            QMessageBox.warning(self.MainWindow, "Error", "No database connection.")
            return
        # Lấy đường dẫn file để lưu từ hộp thoại
        filters = "CSV files (*.csv);;All files(*)"
        filename, selected_filter = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save Table Data",
            "",
            filters
        )

        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                headers = []
                for column in range(self.tableWidgetView.columnCount()):
                    headers.append(self.tableWidgetView.horizontalHeaderItem(column).text())
                writer.writerow(headers)


                for row in range(self.tableWidgetView.rowCount()):
                    rowData = []
                    for column in range(self.tableWidgetView.columnCount()):
                        item = self.tableWidgetView.item(row, column)
                        if item is not None:
                            rowData.append(item.text())
                        else:
                            rowData.append('')
                    writer.writerow(rowData)
                QMessageBox.information(self.MainWindow, "Save Successful", "Data has been save successfully!")

    def show(self):
        self.MainWindow.show()
