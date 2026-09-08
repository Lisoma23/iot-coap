FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir aiocoap

COPY server.py /app/server.py

EXPOSE 5683/udp

CMD ["python", "/app/server.py"]
