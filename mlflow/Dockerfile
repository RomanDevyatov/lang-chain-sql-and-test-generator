FROM python:3.10-slim

WORKDIR /mlflow

RUN pip install mlflow>=3.10.0,<4.0.0 \
    psycopg2-binary>=2.9.11,<3.0.0

CMD ["mlflow", "server"]
