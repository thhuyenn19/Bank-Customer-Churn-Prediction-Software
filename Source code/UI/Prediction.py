import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
import mysql.connector


# from Connectors.Connector import Connector
# conn = Connector()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    port=3306,
    password='@Obama123',
    database='bankchurn')

cursor = conn.cursor()

query = "SELECT * FROM Data"
cursor.execute(query)
result = cursor.fetchall()

columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(result, columns=columns)

#---TIỀN XỬ LÍ DỮ LIỆU---
df = df.dropna()
data = df.drop(['customer_id'], axis = 1)

# One-hot encode the categorical columns
data = pd.get_dummies(data, columns=['country', 'gender', 'credit_card', 'active_member'], drop_first=True)
data = data.astype(int)
numerical_columns = ["credit_score", "age", "tenure", "balance", "products_number", "estimated_salary"]
scaler = StandardScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])


X = data.drop(['churn'],axis=1)
y = data['churn']
X_res,y_res = SMOTE().fit_resample(X,y)
X_train, X_test, y_train, y_test = train_test_split(X_res,y_res,test_size=0.2,random_state=42)

# Evaluate XGBoost
model = XGBClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print(accuracy_score(y_test,y_pred))
print(precision_score(y_test,y_pred))
print(recall_score(y_test,y_pred))
print(f1_score(y_test,y_pred))

colors = [(255/255, 192/255, 203/255), (255/255, 160/255, 122/255)]
cmap = LinearSegmentedColormap.from_list("custom_colormap", colors)

# Tạo confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(4, 3))
sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, linecolor="k", linewidths=3)
plt.show()

def predict_churn(customer_data):
    # Ensure the input is in the same format as the training data
    customer_df = pd.DataFrame([customer_data])
    customer_df = pd.get_dummies(customer_df, columns=['country', 'gender', 'credit_card', 'active_member'],
                                 drop_first=True)

    # Add missing columns from the training data one-hot encoding
    for col in X.columns:
        if col not in customer_df.columns:
            customer_df[col] = 0

    # Standardize numerical columns
    customer_df[numerical_columns] = scaler.transform(customer_df[numerical_columns])

    # Predict churn
    prediction = model.predict(customer_df)
    return "Churn" if prediction[0] == 1 else "Not Churn"

# Example usage

conn.close()