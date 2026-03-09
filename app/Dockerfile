FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry --no-cache-dir

COPY app/pyproject.toml app/poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY app/genaidrivenetl /app/genaidrivenetl

EXPOSE 8000

#CMD ["uvicorn", "genaidrivenetl.main:app", "--host", "0.0.0.0", "--port", "8000"]