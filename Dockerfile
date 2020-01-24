FROM python:3.7-alpine3.10 AS wheel

ENV POETRY_VIRTUALENVS_CREATE=false PIP_NO_CACHE_DIR=1

RUN \
  apk add --no-cache --virtual .build-deps \
    g++=8.3.0-r0 \
    libffi-dev=3.2.1-r6 \
    openssl-dev=1.1.1d-r2 \
  && pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .
RUN poetry build

FROM python:3.7-alpine3.10
LABEL maintainer 'Diógenes Oliveira <diogenes1oliveira@gmail.com>'

ENV PIP_NO_CACHE_DIR=1

WORKDIR /app/dist
COPY --from=wheel /app/dist/*.whl ./
RUN \
  apk add --no-cache --virtual .build-deps \
    g++=8.3.0-r0 \
    libffi-dev=3.2.1-r6 \
    openssl-dev=1.1.1d-r2 \
  && pip install *.whl \
  && apk del .build-deps

WORKDIR /app

COPY docker-entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "locust-tracking-load-faker" ]
