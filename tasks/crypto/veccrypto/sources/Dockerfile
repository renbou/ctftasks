FROM python:3-alpine

MAINTAINER tg: @renbou

WORKDIR /app

ADD ./app /app

RUN apk add --no-cache socat
RUN chmod +x /app/run.sh /app/server.py

ENTRYPOINT [ "sh", "run.sh" ]
