FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /hr_department
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /hr_department/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /hr_department/
# EXPOSE 8000