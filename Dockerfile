FROM python:3.11-slim-bullseye as base
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
EXPOSE 8080

FROM base as local

FROM base as prod
COPY ./ ./
