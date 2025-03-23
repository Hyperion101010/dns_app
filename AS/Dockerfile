FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

# Expose port 53533
EXPOSE 53533/udp

# Run the Authoritative Server
CMD ["python", "authoritative_server.py"]