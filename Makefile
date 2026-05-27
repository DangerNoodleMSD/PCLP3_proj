.PHONY: api_req

database: | database_raw.csv
	python3 clean_database.py

database_raw:
	python3 database_raw.py
