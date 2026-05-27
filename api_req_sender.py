import requests

f = open("response.txt", "w")

response = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=9419750&product=water_level&datum=MTL&time_zone=gmt&units=metric&format=xml')

if (response.status_code == 200):
	f.write(response.text)

print(response.text)
