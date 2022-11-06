FROM python:3.10-slim

# set work directory
WORKDIR /code

# set environment variables
ENV FLASK_APP=run.py

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

# run flask
CMD ["sh", "entrypoint.sh"]
