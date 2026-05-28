.PHONY: database_raw, database, train

train: | database.csv
	python3 train.py

database: | database_raw.csv
	python3 clean_database.py

database_raw.csv:
	$(MAKE) database_raw

database_raw:
	python3 database_raw.py
