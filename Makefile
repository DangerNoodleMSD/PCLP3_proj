.PHONY: api_req

train: database.csv
	train.py

database.csv:
	$(MAKE) database

database: | database_raw.csv
	python3 clean_database.py

database_raw.csv:
	$(MAKE) database_raw

database_raw:
	python3 database_raw.py
