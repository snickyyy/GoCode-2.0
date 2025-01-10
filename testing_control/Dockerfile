FROM python:3.12-alpine

RUN apk update
RUN mkdir /GoCode

WORKDIR /GoCode

RUN python -m pip install --upgrade pip && pip install faststream[rabbit] RestrictedPython redis python-dotenv

CMD ["/bin/sh"]
