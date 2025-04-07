FROM python:3.9-slim

WORKDIR /usr/src/app

RUN pip install Flask requests

COPY . .

EXPOSE 53533/udp

CMD ["python", "authoritative_server.py"]
