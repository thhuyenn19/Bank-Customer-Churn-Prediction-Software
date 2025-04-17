from PyQt6.QtWidgets import QFileDialog, QMessageBox
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier
from Model.TrainedModel import TrainedModel

import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

class XGBoostPredict:
    def __init__(self, connector=None):
        self.connector = connector
        self.scaler = StandardScaler()
        self.model = None
        self.X = None
        self.numerical_columns = ["credit_score", "age", "tenure", "balance", "products_number", "estimated_salary"]

    def processTrain(self,conn):
        self.cursor = conn.cursor()
        # self.MainWindow = MainWindow
        self.query = "SELECT * FROM Data"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()

        self.columns = [desc[0] for desc in self.cursor.description]
        self.df = pd.DataFrame(self.result, columns=self.columns)

        self.df = self.df.dropna()
        self.data = self.df.drop(['customer_id'], axis=1)

        self.data = pd.get_dummies(self.data, columns=['country', 'gender', 'credit_card', 'active_member'], drop_first=True)
        self.data = self.data.astype(int)
        self.numerical_columns = ["credit_score", "age", "tenure", "balance", "products_number", "estimated_salary"]
        self.scaler = StandardScaler()
        self.data[self.numerical_columns] = self.scaler.fit_transform(self.data[self.numerical_columns])

        self.X = self.data.drop(['churn'], axis=1)
        self.y = self.data['churn']
        self.X_res, self.y_res = SMOTE().fit_resample(self.X, self.y)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X_res, self.y_res, test_size=0.2, random_state=42)
        self.trainedmodel = TrainedModel()
        self.trainedmodel.X_train = self.X_train
        self.trainedmodel.X_test = self.X_test
        self.trainedmodel.y_train = self.y_train
        self.trainedmodel.y_test = self.y_test

        self.model = XGBClassifier(n_estimators=200, random_state=42)
        self.model.fit(self.X_train, self.y_train)
        self.trainedmodel.model = self.model
        self.save_model(self.model)
    def save_model(self, model):
        filename, _ = QFileDialog.getSaveFileName(None, "Save Model", "", "Model files (*.zip)")
        if filename:
            with open(filename, 'wb') as file:
                pickle.dump(model, file)
        else:
            QMessageBox.warning(None, "Warning", "You have not selected a location to save the model")
    def loadTrainedModel(self, conn):
        self.cursor = conn.cursor()

        self.query = "SELECT * FROM Data"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()

        self.columns = [desc[0] for desc in self.cursor.description]
        self.df = pd.DataFrame(self.result, columns=self.columns)

        self.df = self.df.dropna()
        self.data = self.df.drop(['customer_id'], axis=1)

        self.data = pd.get_dummies(self.data, columns=['country', 'gender', 'credit_card', 'active_member'],
                                   drop_first=True)
        self.data = self.data.astype(int)
        self.data[self.numerical_columns] = self.scaler.fit_transform(self.data[self.numerical_columns])

        self.X = self.data.drop(['churn'], axis=1)

        filename = self.load_model()
        trainedmodel = self.model2
        if trainedmodel:
            QMessageBox.warning(None,"Inform","Successfully Loaded Model")
            return filename
        else:
            QMessageBox.warning(None,"Inform","Failed to load Model")
            return

    def load_model(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Load Model", "", "Model files (*.zip)")
        if filename:
            with open(filename, 'rb') as file:
                self.model2 = pickle.load(file)
                return filename
        else:
            self.model2 = None
            QMessageBox.warning(None, "Warning", "You have not selected a model to load")

    def predict(self, customer_data,conn,filename):
        self.cursor = conn.cursor()

        self.query = "SELECT * FROM Data"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()

        self.columns = [desc[0] for desc in self.cursor.description]
        self.df = pd.DataFrame(self.result, columns=self.columns)

        self.df = self.df.dropna()
        self.data = self.df.drop(['customer_id'], axis=1)

        self.data = pd.get_dummies(self.data, columns=['country', 'gender', 'credit_card', 'active_member'],
                                   drop_first=True)
        self.data = self.data.astype(int)
        self.data[self.numerical_columns] = self.scaler.fit_transform(self.data[self.numerical_columns])

        self.X = self.data.drop(['churn'], axis=1)

        modelname = f"{filename}"
        model = pickle.load(open(modelname, "rb"))
        self.customer_df = pd.DataFrame([customer_data])

        self.customer_df = pd.get_dummies(self.customer_df,
                                          columns=['country', 'gender', 'credit_card', 'active_member'],
                                          drop_first=True)

        for col in self.X.columns:
            if col not in self.customer_df.columns:
                self.customer_df[col] = 0

        self.customer_df = self.customer_df[self.X.columns]

        self.customer_df[self.numerical_columns] = self.scaler.transform(self.customer_df[self.numerical_columns])

        self.churn_probability = model.predict_proba(self.customer_df)[:, 1][0]
        self.prediction = model.predict(self.customer_df)[0]

        return self.churn_probability, self.prediction

    def predict_customers(self, customer_file_path):
        customer_df = pd.read_csv(customer_file_path)

        customer_df_output = customer_df.copy()

        customer_df = customer_df.assign(churn=pd.NA, probability=pd.NA)

        customer_ids = customer_df['customer_id']
        customer_df = customer_df.drop(columns=['customer_id'])

        customer_df = pd.get_dummies(customer_df, columns=['country', 'gender', 'credit_card', 'active_member'],
                                     drop_first=True)

        customer_df = customer_df.drop(columns=['churn', 'probability'])

        for col in self.X.columns:
            if col not in customer_df.columns:
                customer_df[col] = 0

        customer_df[self.numerical_columns] = self.scaler.transform(customer_df[self.numerical_columns])

        # Dự đoán cho các khách hàng trong dữ liệu khách hàng
        churn_probabilities = self.model.predict_proba(customer_df)[:, 1]
        churn_predictions = self.model.predict(customer_df)
        churn_probabilities1 = [round(prob, 2) for prob in churn_probabilities]
        churn_predictions1 = [int(pred) for pred in churn_predictions]

        for index, customer_id in enumerate(customer_ids):
            customer_df_output.loc[index, 'churn'] = churn_predictions1[index]
            customer_df_output.loc[index, 'probability'] = churn_probabilities1[index]

        return customer_df_output





