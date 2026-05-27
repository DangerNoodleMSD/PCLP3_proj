import pandas as pd

df = pd.read_csv("database_raw.csv")

df.fillna({"fl_minor": df["fl_minor"].mean()}, inplace=True)
df.fillna({"fl_moderate": df["fl_moderate"].mean()}, inplace=True)
df.fillna({"fl_major": df["fl_major"].mean()}, inplace=True)

df = df[df["name"] == "Crescent City"]

pd.DataFrame.to_csv(df, "database.csv")
