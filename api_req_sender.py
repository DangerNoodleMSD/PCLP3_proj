import requests

#url = 'https://api.tidesandcurrents.noaa.gov/api'
# data = {'station=': '9419750',
# 	 	'date=': 'latest',
# 		'product=' : 'water_level',
# 		'datum=' : 'MTL',
# 		'units=' : 'metric',
# 		'time_zone=' : 'gmt',
# 		}
#response = requests.post(url, json=data)

response = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=9419750&product=water_level&datum=MTL&time_zone=gmt&units=metric&format=xml')

print(response.text)

# Check if the request was successful
# if response.status_code == 200:
# 		# Parse the JSON response into a dictionary
# 	data = response.json()
# 	print(f"Successfully fetched data for user: {data['login']}")
# 	print(f"Public repos: {data['public_repos']}")
# else:
# 	print(f"Error: Received status code {response.status_code}")
