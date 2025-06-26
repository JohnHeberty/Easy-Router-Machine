FROM python:3.11-slim

WORKDIR /api

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    build-essential \
    libpq-dev \
    gcc \
    g++ \
    curl \
    gnupg2 \
    libsqlite3-mod-spatialite \
  && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY main_api.py .
COPY src src

EXPOSE 8010

CMD ["fastapi", "run", "main_api.py", "--host", "0.0.0.0", "--port", "8010"]
