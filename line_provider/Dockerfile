FROM python:3.8-slim-buster as builder

RUN apt-get update

RUN pip install poetry
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-dev\
    && rm -rf pyproject.toml poetry.lock

WORKDIR /line_provider
COPY . /line_provider
CMD uvicorn main:app --host 0.0.0.0 --port 8000