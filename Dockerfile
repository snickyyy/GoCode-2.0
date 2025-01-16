FROM python:3.12-alpine

RUN apk update
RUN mkdir /GoCode

WORKDIR /GoCode

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY .env ./.env
COPY ./commands ./commands

RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt

CMD ["/bin/sh"]

