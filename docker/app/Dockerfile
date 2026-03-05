FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY app/pyproject.toml app/poetry.lock* /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY app /app

CMD ["python", "main.py"]
