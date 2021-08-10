# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update -y
RUN apt-get install -y libzbar0
RUN apt-get install -y poppler-utils
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["sh", "entrypoint.sh"]