FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /accounting

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /accounting/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app /accounting/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]