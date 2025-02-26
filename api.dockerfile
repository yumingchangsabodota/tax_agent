FROM python:3.11.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update 

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY agent agent
COPY ai_model ai_model
COPY db db
COPY api api
COPY ui ui

EXPOSE 8086
EXPOSE 80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8086", "--workers", "4", "--log-config=log_config.yaml"]
