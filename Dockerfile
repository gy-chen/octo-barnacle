FROM python:3

COPY . /data
WORKDIR /data

RUN pip install .

CMD octo-barnacle-collect-mal-recommendation