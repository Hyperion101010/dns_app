# Dockerfile for Fibonacci Server (FS)
FROM python:3.9-slim

RUN pip install Flask requests

WORKDIR /usr/src/app

COPY . .

# Expose port 9090 for the Fibonacci Server
EXPOSE 9090

# Run the Fibonacci Server script
CMD ["python", "fibonacci_server.py"]