import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

def error_calc(type:str, y_test, y_pred):
	rmse = np.sqrt(mean_squared_error(y_test, y_pred))
	print(f"{type} (RMSE):", rmse)
	mae = mean_absolute_error(y_test, y_pred)
	print(f"{type} (MAE):", mae)
	r2 = r2_score(y_test, y_pred)
	print(f"{type} (R2):", r2)

df = pd.read_csv("database.csv")

X = df.drop(columns=[' Water Level','Date Time',' Sigma','name','fl_minor','fl_moderate','fl_major','lat','long','Pacific','Atlantic'])
y = df[' Water Level']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=11)

# Logistic Regression
model = LinearRegression()
model = model.fit(X_train, y_train)
y_pred = model.predict(X_test)
error_calc('Linear Regression', y_test, y_pred)

# Ridge Regression
model = Ridge()
model = model.fit(X_train, y_train)
y_pred = model.predict(X_test)
error_calc('Ridge Regression', y_test, y_pred)

# Support Vector Regression
model = SVR()
model = model.fit(X_train, y_train)
y_pred = model.predict(X_test)
error_calc('SVR', y_test, y_pred)

# Random Forest Regressor
model = RandomForestRegressor()
model = model.fit(X_train, y_train)
y_pred = model.predict(X_test)
error_calc('Random Forest Regressor', y_test, y_pred)