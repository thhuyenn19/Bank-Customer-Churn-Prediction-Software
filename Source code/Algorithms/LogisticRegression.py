import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv('dataset/Bank Customer Churn Prediction.csv')
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

# Evaluate LOGISTIC REG
log = LogisticRegression()
log.fit(X_train,y_train)
y_pred1 = log.predict(X_test)
print(classification_report( y_test, y_pred1))

print(accuracy_score(y_test,y_pred1))
print(precision_score(y_test,y_pred1))
print(recall_score(y_test,y_pred1))
print(f1_score(y_test,y_pred1))

colors = [(255/255, 192/255, 203/255), (255/255, 160/255, 122/255)]
cmap = LinearSegmentedColormap.from_list("custom_colormap", colors)
# Tạo confusion matrix
cm = confusion_matrix(y_test, y_pred1)

plt.figure(figsize=(4, 3))
sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, linecolor="k", linewidths=3)
plt.show()