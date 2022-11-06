
## entrypoint.sh
python3.10 create_tables.py
python3.10 load_fixtures.py
flask run -h 0.0.0.0 -p 5000