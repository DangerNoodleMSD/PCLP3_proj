import requests

f = open("response_metadata.json", "w")

response = requests.get('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9419750.json?units=english')
if (response.status_code == 200):
	f.write(response.text)
f.close()

f = open("response_data.csv", "w")

response = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=9419750&product=water_level&datum=MTL&time_zone=gmt&units=metric&format=csv')
if (response.status_code == 200):
	f.write(response.text)
f.close()
