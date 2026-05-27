import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("database_raw.csv")

df.fillna({"fl_minor": df["fl_minor"].mean()}, inplace=True)
df.fillna({"fl_moderate": df["fl_moderate"].mean()}, inplace=True)
df.fillna({"fl_major": df["fl_major"].mean()}, inplace=True)

df["Date Time"] = datetime.strptime(df["Date Time"][0], "%Y-%m-%d %H:%M").timestamp()

df = df[df["name"] == "Crescent City"]

pd.DataFrame.to_csv(df, "database.csv")
