import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("database_raw.csv")

df.fillna({"fl_minor": df["fl_minor"].mean()}, inplace=True)
df.fillna({"fl_moderate": df["fl_moderate"].mean()}, inplace=True)
df.fillna({"fl_major": df["fl_major"].mean()}, inplace=True)

# # Converts date in seconds passed from Epoch
# df["Date Time"] = datetime.strptime(df["Date Time"][0], "%Y-%m-%d %H:%M").timestamp()

# Drop redundant column
df.drop(df.columns[0], axis=1, inplace=True)

# Choosing to focus on one specific station
df = df[df["name"] == "Crescent City"]

water_lvl_max = df[' Water Level'].max()

# Normalizing Water Level
scaler = MinMaxScaler()
temp = pd.DataFrame(df[' Water Level'])
df[' Water Level'] = scaler.fit_transform(temp)

# Normalizing fl_minor
df['fl_minor'] = df['fl_minor'] / water_lvl_max

# Normalizing fl_moderate
df['fl_moderate'] = df['fl_moderate'] / water_lvl_max

# Normalizing fl_major
df['fl_major'] = df['fl_major'] / water_lvl_max

pd.DataFrame.to_csv(df, "database.csv")
