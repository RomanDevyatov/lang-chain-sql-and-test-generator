FROM apache/airflow:2.9.3-python3.10

USER root

RUN pip install --no-cache-dir \
    fastapi>=0.128.0,<0.129.0 \
    python-dotenv>=1.2.1,<2.0.0 \
    openai>=2.16.0,<3.0.0 \
    pytest>=9.0.2,<10.0.0 \
    psycopg[binary]>=3.3.2,<4.0.0 \
    psycopg2-binary>=2.9.11,<3.0.0 \
    pandas<3 \
    sqlparse>=0.5.5,<0.6.0 \
    langchain>=1.2.10,<2.0.0 \
    langchain-openai>=1.1.8,<2.0.0 \
    mlflow>=3.10.0,<4.0.0

USER airflow
