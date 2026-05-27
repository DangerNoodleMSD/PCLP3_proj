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
	has_GL_LWD = False
	for datum in resp_json["stations"][0]["datums"]["datums"]:
		if datum["name"] == "MLW":
			has_MLW = True
		if datum["name"] == "GL_LWD":
			has_GL_LWD = True
	
	if (not has_MLW) and (not has_GL_LWD):
		f2 = open("anomaly.json", "w")
		f2.write(response.text)
		f2.close()
		print(f"[WARNING] Station with id {id} has no MLW or GL_LWD datum")
		f.close()
		return False

	if has_MLW and has_GL_LWD:
		print(f"[WARNING] Station with id {id} has MLW and GL_LWD datum")
		f.close()
		return False

	f.write(response.text)
	f.close()

	f = open("response_data.csv", "w")

	# Asking for historical water level and writing it in response_data.csv
	if has_MLW:
		response = requests.get(f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20260520&end_date=20260527&station={id}&product=water_level&datum=MLW&time_zone=gmt&units=metric&format=csv')
	if has_GL_LWD:
		response = requests.get(f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20260520&end_date=20260527&station={id}&product=water_level&datum=GL_LWD&time_zone=gmt&units=metric&format=csv')
	if (response.status_code == 200):
		f.write(response.text)
	else:
		print(f"[WARNING] Response status {response.status_code} at data for station {id}")
		f.close()
		return False
	f.close()

	return True
