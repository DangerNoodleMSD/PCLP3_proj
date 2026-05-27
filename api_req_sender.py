import requests
import json

def get_info(id : int) -> bool:
	f = open("response_metadata.json", "w")

	response = requests.get(f'https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{id}.json?expand=details,sensors,floodlevels,datums&units=metric')
	
	resp_json = json.loads(response.text)
	has_MLW = False
	for datum in resp_json["stations"][0]["datums"]["datums"]:
		if datum["name"] == "MLW":
			has_MLW = True
	
	if not has_MLW:
		f.close()
		return False

	if (response.status_code == 200):
		f.write(response.text)
	else:
		f.close()
		return False
	f.close()

	f = open("response_data.csv", "w")

	response = requests.get(f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20260522&end_date=20260527&station={id}&product=water_level&datum=MLW&time_zone=gmt&units=metric&format=csv')
	if (response.status_code == 200):
		f.write(response.text)
	else:
		f.close()
		return False
	f.close()

	return True
