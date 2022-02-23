FROM python:3-alpine

WORKDIR /owm_exporter

ADD requirements.txt .
ADD exporter.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "/owm_exporter/exporter.py" ]
