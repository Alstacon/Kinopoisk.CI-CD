#!/bin/bash
export FLASK_APP=run
export FLASK_ENV=production
python create_tables.py
python load_fixtures.py
exec "$@"