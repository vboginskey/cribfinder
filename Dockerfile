FROM python:3.5-alpine

COPY . /app/

RUN pip install -r /app/requirements.txt

VOLUME ["/data"]

CMD ["python", "-u", "/app/main.py"]
