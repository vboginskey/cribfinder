FROM python:3.5-alpine

COPY app/ /app/
COPY s6/ /etc/s6/

RUN apk add --no-cache s6 \
  && pip install -r /app/requirements.txt

VOLUME ["/data"]

CMD ["s6-svscan", "/etc/s6"]
