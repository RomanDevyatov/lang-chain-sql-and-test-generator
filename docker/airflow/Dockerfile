FROM apache/airflow:3.0.6-python3.11

USER airflow

COPY app/ /opt/airflow
COPY db/ /opt/airflow/db
COPY .flake8 /opt/airflow
COPY --chown=airflow:0 scripts/ /opt/airflow/scripts

ENV PATH="/home/airflow/.local/bin:$PATH"

WORKDIR /opt/airflow

RUN pip install --upgrade pip \
    && pip install poetry --no-cache-dir \
    && poetry lock \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction

RUN #poetry self add poetry-plugin-export

RUN #poetry export -f requirements.txt --without-hashes -o requirements.txt

RUN #pip install --upgrade pip \
#    && pip install -r requirements.txt \
#       --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.6/constraints-3.11.txt"
