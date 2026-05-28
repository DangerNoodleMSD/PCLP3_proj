import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("database.csv")

X = df.drop(columns=['survived', 'class', 'who', 'deck', 'embark_town', 'alive'], axis=1)  # Caracteristicile (fără coloana 'survived')
y = df['survived']  # Eticheta (variabila țintă)