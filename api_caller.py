import api_req_sender
import data_parser
from proj_classes import attributes_t
import pandas as pd
import json

# Station IDs of stations from around the USA
ids = [9419750, 8570283, 8447435, 8452660, 8454000, 8461490, 8467150, 8518750, 8510560, 8534720, 8551910, 8548989, 8570283, 8632200, 8571892, 8574680, 8635750, 8594900, 8635750, 8638610, 8652587, 8658163, 8670870, 8724580, 8729210, 8766072, 8775296, 8779770, 9410230, 9412110, 9414523, 9416841, 9418767, 9432780, 9439040, 9443090, 9449424]
# Smaller sample for testing purposes
# +-----------------------------------------+
# |		DO NOT FORGET TO CHANGE THE INPUT	|
# +-----------------------------------------+
ids_test = [9419750, 8570283, 8447435, 8452660, 8454000, 8461490, 8467150, 8518750]


# Making a list with all the dataframes to concatenate them at the end
df_list = []

for id in ids_test:
	valid = api_req_sender.get_info(id)

	# Checking if the server responded or if the station has MLW datum
	if valid:
		# Reading the metadata
		name = ""
		great_lake = False
		flood_level = {"minor" : 0, "moderate" : 0, "major" : 0}
		lat = 0
		long = 0
		with open('response_metadata.json', 'r') as file:
			read = file.read().replace('\n', '')
			metadata = json.loads(read)
			name = metadata["stations"][0]["name"]
			great_lake = metadata["stations"][0]["greatlakes"]
			flood_level["minor"] = metadata["stations"][0]["floodlevels"]["nos_minor"]
			flood_level["moderate"] = metadata["stations"][0]["floodlevels"]["nos_moderate"]
			flood_level["major"] = metadata["stations"][0]["floodlevels"]["nos_major"]
			lat = metadata["stations"][0]["lat"]
			long = metadata["stations"][0]["lng"]
		
		attributes = attributes_t(name, great_lake, flood_level, lat, long)
			
		print(f"{name}: \t{lat},\t{long}")
		
		df_list.append(data_parser.parse_data(attributes))

	else:
		print(f"[WARNING] Ignoring station {id}", end="\n\n")

	final_df = pd.concat(df_list)
	pd.DataFrame.to_csv(final_df, "database.csv")
