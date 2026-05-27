import api_req_sender
import json

ids = [9419750, 8570283, 8447435, 8452660, 8454000, 8461490, 8467150, 8518750, 8510560, 8534720, 8551910, 8548989, 8570283, 8632200, 8571892, 8574680, 8635750, 8594900, 8635750, 8638610, 8652587, 8658163, 8670870, 8724580, 8729210, 8766072, 8775296, 8779770, 9410230, 9412110, 9414523, 9416841, 9418767, 9432780, 9439040, 9443090, 9449424]

for id in ids:
	valid = api_req_sender.get_info(id)

	if valid:
		with open('response_metadata.json', 'r') as file:
			read = file.read().replace('\n', '')
			metadata = json.loads(read)
			print(metadata["stations"][0]["name"])
	else:
		print("Doesn't have MLW, or error occured!")
