FROM python:3.10-slim

WORKDIR /opt/movies

ENV FLASK_APP=run.py \
    FLASK_ENV=production


RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /vat/tmp/*

COPY requirements.txt .

RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]