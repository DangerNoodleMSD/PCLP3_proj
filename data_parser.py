import pandas as pd
from proj_classes import attributes_t

def parse_data(attributes : attributes_t) -> pd.DataFrame:
	df = pd.read_csv("response_data.csv")
	df["name"] = attributes.name
	df["great_lake"] = attributes.great_lake
	df["flood_level"] = attributes.flood_level
	df["lat"] = attributes.lat
	df["long"] = attributes.long
	return df