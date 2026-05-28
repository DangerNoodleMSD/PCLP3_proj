import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearnex import patch_sklearn
patch_sklearn()

def error_calc(type:str, y_test, y_pred):
	rmse = np.sqrt(mean_squared_error(y_test, y_pred))
	print(f"{type} (RMSE):", rmse)
	mae = mean_absolute_error(y_test, y_pred)
	print(f"{type} (MAE):", mae)
	r2 = r2_score(y_test, y_pred)
	print(f"{type} (R2):", r2)
	plt.scatter(y_test, y_pred)
	plt.savefig(f'{type}.png')
	plt.clf()

df = pd.read_csv("database.csv", usecols=["Date Time", " Water Level", "name"], index_col="Date Time")

df = df[[' Water Level']]
print(df.head())

df.index = pd.to_datetime(df.index)
print(df.head())

df['month'] = df.index.month
df['day'] = df.index.day
df['hour'] = df.index.hour

for i in range(1, 6):
	df[f'Ant{i}'] = df[' Water Level'].shift(i)

df['mean'] = df[' Water Level'].shift(1).rolling(window=24).mean()
df['max'] = df[' Water Level'].shift(1).rolling(window=24).max()
df['std'] = df[' Water Level'].shift(1).rolling(window=24).std()
print(df.head())

def add_sin_cos(df : pd.DataFrame, period : float, hours : float) -> pd.DataFrame:
	df[f'sin{period}'] = np.sin(2 * np.pi * hours / period)
	df[f'cos{period}'] = np.cos(2 * np.pi * hours / period)
	return df

hours = df.index.year * 8760 + df.index.month * 732 + df.index.day * 24 + df.index.hour
df = add_sin_cos(df, 12, hours)
df = add_sin_cos(df, 24, hours)
# Spring/Neap tide cycle
df = add_sin_cos(df, 354, hours)
# Lunar cycle
df = add_sin_cos(df, 708, hours)

df.dropna(inplace=True)

print(df.head())


# Split training, test
split_id = int(len(df) * 0.8)
train = df.iloc[:split_id]
test = df.iloc[split_id:]

X_train = train.drop(columns=[' Water Level'])
y_train = train[' Water Level']

X_test = test.drop(columns=[' Water Level'])
y_test = test[' Water Level']


print("")
print(f"Training len {len(train)}")
print(f"Test len {len(train)}")

def make_graph(type : str, y_test, pred):
	plt.clf()
	plt.figure(figsize=(14, 6))
	plt.plot(y_test.index, y_test, label='History', color='blue')
	plt.plot(y_test.index, pred, label=f'{type}', linestyle='--', color='red')
	plt.savefig(f"{type}_graph.png")
	plt.clf()

def train_model(X_train, y_train, X_test, y_test, window_size, step_size):
	predictions = []
	ground_truth = []

	X = pd.concat([X_train, X_test])
	y = pd.concat([y_train, y_test])

	start_id = len(X_train)

	for i in range(0, len(X_test), step_size):
		train_id_end = start_id + i
		train_id_begin = max(0, train_id_end - window_size)
		X_window = X.iloc[0:train_id_end]
		y_window = y.iloc[0:train_id_end]

		model = LinearRegression()
		model.fit(X_window, y_window)

		test_id_begin = train_id_end
		test_id_end = min(test_id_begin + step_size, len(X))
		X_pred = X[test_id_begin:test_id_end]
		y_ground_truth = y[test_id_begin:test_id_end]

		if (len(X_pred) == 0):
			break

		pred = model.predict(X_pred)

		predictions.extend(pred)
		ground_truth.extend(y_ground_truth)

		if i % 20 == 0:
			print(f"Iteration {i}")
	
	return predictions, ground_truth


pred, ground_truth = train_model(X_train, y_train, X_test, y_test, 200, 1)

error_calc("LinearRegression", ground_truth, pred)
make_graph("LinearRegression", y_test, pred)

def train_model(X_train, y_train, X_test, y_test, window_size, step_size):
	predictions = []
	ground_truth = []

	X = pd.concat([X_train, X_test])
	y = pd.concat([y_train, y_test])

	start_id = len(X_train)

	for i in range(0, len(X_test), step_size):
		train_id_end = start_id + i
		train_id_begin = max(0, train_id_end - window_size)
		X_window = X.iloc[0:train_id_end]
		y_window = y.iloc[0:train_id_end]

		model = LinearRegression()
		model.fit(X_window, y_window)

		test_id_begin = train_id_end
		test_id_end = min(test_id_begin + step_size, len(X))
		X_pred = X[test_id_begin:test_id_end]
		y_ground_truth = y[test_id_begin:test_id_end]

		if (len(X_pred) == 0):
			break

		pred = model.predict(X_pred)

		predictions.extend(pred)
		ground_truth.extend(y_ground_truth)

		if i % 20 == 0:
			print(f"Iteration {i}")
	
	return predictions, ground_truth


pred, ground_truth = train_model(X_train, y_train, X_test, y_test, 200, 1)

error_calc("LinearRegression", ground_truth, pred)
make_graph("LinearRegression", y_test, pred)


# split_idx = int(len(df) * 0.8)
# train = df.iloc[:split_idx]
# test = df.iloc[split_idx:]
# X_train = train.drop(columns=[' Water Level','Date Time',' Sigma','name','fl_minor','fl_moderate','fl_major','lat','long','Pacific','Atlantic'])
# y_train = train[' Water Level']
# X_test = test.drop(columns=[' Water Level','Date Time',' Sigma','name','fl_minor','fl_moderate','fl_major','lat','long','Pacific','Atlantic'])
# y_test = test[' Water Level']

# # Logistic Regression
# model = LinearRegression()
# model = model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# error_calc('Linear Regression', y_test, y_pred)

# # Ridge Regression
# model = Ridge()
# model = model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# error_calc('Ridge Regression', y_test, y_pred)

# # Support Vector Regression
# model = SVR()
# model = model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# error_calc('SVR', y_test, y_pred)

# # Random Forest Regressor
# model = RandomForestRegressor()
# model = model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# error_calc('Random Forest Regressor', y_test, y_pred)