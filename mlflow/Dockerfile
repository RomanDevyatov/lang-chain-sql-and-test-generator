FROM python:3.10-slim

WORKDIR /mlflow

RUN pip install --no-cache-dir mlflow psycopg2-binary

CMD ["mlflow", "server"]
