

# Dockerfile for User Server (US)
FROM python:3.9-slim

RUN pip install Flask requests

WORKDIR /usr/src/app

COPY . .

# Expose port 8080 for the User Server
EXPOSE 8080

# Run the User Server script
CMD ["python", "user_server.py"]