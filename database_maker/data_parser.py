import pandas as pd
from database_maker.proj_classes import attributes_t

def parse_data(attributes : attributes_t) -> pd.DataFrame:
	df = pd.read_csv("response_data.csv")
	df["name"] = attributes.name
	df["great_lake"] = attributes.great_lake

	df["fl_minor"] = attributes.flood_level["minor"]
	df["fl_moderate"] = attributes.flood_level["moderate"]
	df["fl_major"] = attributes.flood_level["major"]

	df["lat"] = attributes.lat
	df["long"] = attributes.long
	#df.drop(' O or I (for verified)', axis=1, inplace=True)
	#df.drop(' F', axis=1, inplace=True)
	#df.drop(' R', axis=1, inplace=True)
	#df.drop(' L', axis=1, inplace=True)
	#df.drop(' Quality ', axis=1, inplace=True)
	df.drop(' I', axis=1, inplace=True)
	df.drop(' L ', axis=1, inplace=True)
	df.drop('great_lake', axis=1, inplace=True)
	df["Pacific"] = (df["long"] < -105).astype(int)
	df["Atlantic"] = (df["long"] > -105).astype(int)
	return df