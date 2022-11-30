FROM python:3.9

ARG KEY
ARG NUMBER_DEVICES

WORKDIR .

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY . .
RUN pip install -r src/requirements.txt

CMD python src/main.py --key ${KEY} --number_devices ${NUMBER_DEVICES} --url ${URL}
