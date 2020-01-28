FROM python:3.7-alpine3.10 AS builder

ENV POETRY_VIRTUALENVS_CREATE=false PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./

RUN \
  apk add --no-cache --virtual .build-deps \
    g++=8.3.0-r0 \
    libffi-dev=3.2.1-r6 \
    openssl-dev=1.1.1d-r2 \
    python3-dev=3.7.5-r1 \
  && pip install poetry

COPY tracking_load_faker/ ./tracking_load_faker/
COPY test/ ./test/
COPY README.md LICENSE ./
RUN poetry build

FROM python:3.7-alpine3.10
LABEL maintainer 'Diógenes Oliveira <diogenes1oliveira@gmail.com>'

ENV PIP_NO_CACHE_DIR=1

WORKDIR /app/dist
COPY --from=builder /app/dist/*.whl ./
RUN \
  apk add --no-cache --virtual .build-deps \
    g++=8.3.0-r0 \
    libffi-dev=3.2.1-r6 \
    openssl-dev=1.1.1d-r2 \
    python3-dev=3.7.5-r1 \
  && apk add --no-cache \
    libzmq=4.3.2-r1 \
  && pip install *.whl \
  && apk del --purge .build-deps

WORKDIR /app
COPY . .
COPY ./docker-entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "locust-tracking-load-faker" ]
