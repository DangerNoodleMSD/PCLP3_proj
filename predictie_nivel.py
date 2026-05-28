import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#============================================= Doar incarcare ==============================================
# Mi-ai bagat un spatiu inainte de Water Level si am fost obligat sa afisez capul de tabel ca sa vad cum se numeste coloana. 
#df = pd.read_csv("database_raw.csv")
#print(df.columns.tolist())
# ['Unnamed: 0', 'Date Time', ' Water Level', ' Sigma', 'name', 'fl_minor', 'fl_moderate', 'fl_major', 'lat', 'long', 'Pacific', 'Atlantic']


# incarcă doar coloanele necesare pentru filtrare + cele dorite
df = pd.read_csv(
    "database_raw.csv",
    usecols=["Date Time", " Water Level", "name"],
    parse_dates=["Date Time"],
    index_col="Date Time"
)


# pastrează doar Crescent City
df = df[df["name"].str.strip() == "Crescent City"]

# elimin coloana name dacă nu mai ai nevoie de ea
df = df[[" Water Level"]]

print(df.head())

#============================================= Doar afisare ==============================================
# creare plot
"""
plt.figure(figsize=(14, 6))
plt.plot(df.index, df[' Water Level'], linewidth=0.8, color='steelblue', label='Water level')

# trend line
z = np.polyfit(range(len(df)), df[' Water Level'], 1)
p = np.poly1d(z)
plt.plot(df.index, p(range(len(df))), "r--", linewidth=2, label='Linear Trend', alpha=0.7)

# medie pe o saptamana (168 ore)
# rolling_mean = df[' Water Level'].rolling(window=168, center=True).mean()
# plt.plot(df.index, rolling_mean, linewidth=2, color='orange', label='1 Week Mean', alpha=0.8)

# medie pe o zi (24 ore)
rolling_mean = df[' Water Level'].rolling(window=24, center=True).mean()
plt.plot(df.index, rolling_mean, linewidth=2, color='orange', label='1 Week Mean', alpha=0.8)

# Formatting
plt.title('Simple Line Plot - Water Level', fontsize=14, fontweight='bold')
plt.xlabel('Hours', fontsize=12)
plt.ylabel('Water Level', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)

plt.tight_layout()
# plt.savefig('simple_line_plot.png', dpi=300, bbox_inches='tight')
plt.show()
"""
#============================================= Trasaturi ==============================================
# TRASATURI: luna, ziua, ora
# convertire index to DatetimeIndex ca sa pot extrage usor luna, ziua, ora
df.index = pd.to_datetime(df.index)

df['month'] = df.index.month
df['day']   = df.index.day
df['hour']  = df.index.hour

#TRASATURI: lag-uri de 1, 2, 3, 4, 5 ore
for lag in range(1, 6):
    df[f'lag_{lag}'] = df[' Water Level'].shift(lag)

#TRASATURI: medie pe 24 de ore + deviatie standard pe 24 de ore + val. max. pe 24 de ore
#Ii zice modelului nivelul mediu al apei in ultimele 24 de ore (un fel de baseline in jurul caruia sa isi bazeze estimarea)
df['mean_24h'] = df[' Water Level'].shift(1).rolling(window=24).mean()
#Ii zice modelului cat de "agresive" sunt schimbarile mareei (o furtuna poate face schimbari mari posibile)
df['std_24h']  = df[' Water Level'].shift(1).rolling(window=24).std()
#Ii da modelului un maxim dupa care sa se ia, ca sa nu urce extrem de mult peste maximul din ultimele 24 de ore
df['max_24h']  = df[' Water Level'].shift(1).rolling(window=24).max()

print(df.head())

#TRASATURI: sin + cos pentru ora (pentru a capta periodicitatea zilnica)
def add_SinCos_terms(df, perioada, n_terms):
    for i in range(1, n_terms + 1):
        df[f'sin_{perioada}_{i}'] = np.sin(2 * np.pi * i * df['hour'] / perioada)
        df[f'cos_{perioada}_{i}'] = np.cos(2 * np.pi * i * df['hour'] / perioada)
    return df

db_alg_brut = add_SinCos_terms(df, perioada=24, n_terms=2)
db_alg = db_alg_brut.dropna()  # elimin randurile cu valori NaN generate de lag-uri, medie, std, max, etc.

#print(db_alg.head())

#=============================== Creez seturi de antrenare/testare =================================
# 80 antrenare - 20 testare

# calculez punct imparire in seg
split_idx = int(len(db_alg) * 0.8)

train = db_alg.iloc[:split_idx]
test  = db_alg.iloc[split_idx:]

X_train, y_train = train.drop (columns=[' Water Level']), train[' Water Level']
X_test, y_test   = test.drop  (columns=[' Water Level']), test[' Water Level']

# pentru antrenare: X_train, y_train
print(X_train.head())   # intrarea random forest
print(y_train.head())   # dorit random forest

# pentru testare: X_test, y_test => aici o sa fac predictia si o sa compar cu y_test

print(" ")
print(f"Training observations: {len(X_train)}")
print(f"Testing observations: {len(X_test)}")


#=============================== functii de evaluare =================================
def get_metrics(y_true, y_pred, y_train, sp=24):
    # date orare, probabil sp=24 (sezonalitate zilnică), dar poate fi ajustat 
    # de exemplu, sp=168 pentru sezonalitate saptamanala)
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    # metrici de baza
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    # R^2 - coeficient de determinare
    r2 = r2_score(y_true, y_pred)

    # MASE - Mean Absolute Scaled Error 
    naive_seasonal_errors = np.abs(y_train.values[sp:] - y_train.values[:-sp])
    mae_seasonal_naive = np.mean(naive_seasonal_errors)

    mase = mae / mae_seasonal_naive
    return mae, rmse, r2, mase

#=============================== aici este partea frumoasa =================================

def random_forest_antrenare(X_train, y_train, X_test, y_test,
                                  window_size=100, step_size=1) -> np.ndarray:
    """
    Args:
        X_train: antrenare intrare (trasaturi de intrare)
        y_train: antrrenare dorit (valoarea de prezis)
        X_test: test intrare (trasaturi de intrare pentru test)
        y_test: test dorit (valoarea de prezis pentru test)
        window_size: Dimensiunea inițială a ferestrei de antrenament
        step_size: pe cati pasi se face predictia (daca e 1, se face pe o ora inainte)

    Returns:
        predictions: vector predictii
        actual: reale
    """
    from sklearn.ensemble import RandomForestRegressor
    print(f"Random Forest parametri:")
    print(f"  Fereastra initiala: {window_size}")
    print(f"  Valori de test: {len(X_test)}")
    print(f"  Pasul de test: {step_size}\n")

    predictions = []
    actuals = []

    # Combinare X_train și X_test pentru a avea o singură serie temporală
    X_full = pd.concat([X_train, X_test])
    y_full = pd.concat([y_train, y_test])

    # Pornire de la punct in comun dintre train si test
    start_idx = len(X_train)

    for i in range(0, len(X_test), step_size):
        # Define training window (expanding window)
        train_start = max(0, start_idx + i - window_size)
        train_end = start_idx + i

        # Get training data for this window
        X_window = X_full.iloc[train_start:train_end]
        y_window = y_full.iloc[train_start:train_end]

        # ia valori de test pentru pasul curent
        test_start = start_idx + i
        test_end = min(start_idx + i + step_size, len(X_full))
        X_pred = X_full.iloc[test_start:test_end]
        y_actual = y_full.iloc[test_start:test_end]

        if len(X_pred) == 0:
            break

        # Antrenare model Random Forest pe fereastra curenta
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_window, y_window)

        # Predictie pentru pasul curent
        pred = rf.predict(X_pred)

        predictions.extend(pred)
        actuals.extend(y_actual.values)

        if (i // step_size) % 20 == 0:
            print(f"  Iteration {i//step_size}: Train[{train_start}:{train_end}], Predict[{test_start}:{test_end}]")

    return np.array(predictions), np.array(actuals)

preds_rf, actuals_rf = random_forest_antrenare(
      X_train, y_train, X_test, y_test,
      window_size=200,  # fereastra initiala de antrenament (200 ore)
      step_size=1       # Prediction la fiecare pas (1 ora inainte)
  )

mae, rmse, R2, mase = get_metrics(y_test, preds_rf, y_train)

print(" ")
print(f"Mean Absolute Error is: {mae}\n")
print(f"Root of Mean Squared Error is: {rmse}\n")
print(f"R^2 Score is: {R2}\n")
print(f"Mean Absolute Scaled Error is: {mase}\n")
print(" ")

#=============================== acum afisare rezultate================================

# Historical Data
plt.figure(figsize=(14, 6))
#plt.plot(X_train.index, y_train, color='black')
plt.plot(X_test.index, y_test, label='History', color='blue')
# Random Forest Forecasting
plt.plot(y_test.index, preds_rf, label='Random Forest', linestyle='--', color='red')

plt.title('Random Forest Forecasting - Water Level', fontsize=14, fontweight='bold')
plt.ylabel('Water Level', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.show()
plt.savefig('foo.png')