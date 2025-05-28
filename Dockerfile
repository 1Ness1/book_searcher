FROM python:3.9-slim

RUN apt-get update && apt-get install -y python3-tk \
    && apt-get clean

RUN pip install requests bs4 flask flask_cors pydantic

WORKDIR /app

COPY . /app

CMD ["python", "app.py"]