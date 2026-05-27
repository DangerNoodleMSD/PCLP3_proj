import requests
import json

def get_info(id : int) -> bool:
	f = open("response_metadata.json", "w")

	# Asking for metadata of station {id}
	response = requests.get(f'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{id}.json?expand=details,sensors,floodlevels,datums&units=metric')

	# Writing the metadata in response_metadata.json file
	if (not response.status_code == 200):
		print(f"[WARNING] Response status {response.status_code} at metadata for station {id}")
		f.close()
		return False

	# Check if it has MLW or LWD datum, otherwise we won't use this station
	resp_json = json.loads(response.text)
	has_MLW = False
	for datum in resp_json["stations"][0]["datums"]["datums"]:
		if datum["name"] == "MLW":
			has_MLW = True
	
	if not has_MLW:
		print(f"[WARNING] Station with id {id} has no MLW datum")
		f.close()
		return False

	f.write(response.text)
	f.close()

	f = open("response_data.csv", "w")

	# Asking for historical water level and writing it in response_data.csv
	response = requests.get(f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20251101&end_date=20260430&station={id}&product=hourly_height&datum=MLW&time_zone=gmt&units=metric&format=csv')
	if (response.status_code == 200):
		f.write(response.text)
	else:
		print(f"[WARNING] Response status {response.status_code} at data for station {id}")
		f.close()
		return False
	f.close()

	return True
