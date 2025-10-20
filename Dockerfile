# Dockerfile for Flask app "nuge"
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install flask

EXPOSE 8080

CMD ["python", "nuge.py"]
