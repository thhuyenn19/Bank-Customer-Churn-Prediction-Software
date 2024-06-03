import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv('Bank Customer Churn Prediction.csv')

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


#--------------------RANDOMIZEDSEARCHCV---------------------------------------
parameter_grid = {
    'learning_rate': [0.1, 0.05, 0.01],
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 4, 5]
}

# Create an instance of the GradientBoostingClassifier
best_model = XGBClassifier()

# Perform random search
random_search = RandomizedSearchCV(model, parameter_grid, n_iter=10, cv=5)
random_search.fit(X_train, y_train)

# Get the best model and its parameters
best_model = random_search.best_estimator_
best_params = random_search.best_params_
print("Best Parameters:", best_params)

# Evaluate the best model on the test set
y_pred1 = best_model.predict(X_test)
print(classification_report(y_test, y_pred1))