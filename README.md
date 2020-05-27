# tracking-load-faker

Run load tests against tracking services (like Matomo) using Faker to generate
visits

[![Build Status](https://api.travis-ci.org/python/mypy.svg?branch=master)](https://travis-ci.org/python/mypy)
[![codecov](https://codecov.io/gh/diogenes1oliveira/tracking-load-faker/branch/master/graph/badge.svg)](https://codecov.io/gh/diogenes1oliveira/tracking-load-faker)

This project generates fake visits and actions based on the Matomo plugin
[VisitorGenerator](https://github.com/matomo-org/plugin-VisitorGenerator),
sending them to the tracker URL to simulate real users. The requests
are generated via [Locust](https://locust.io/), a tool for programatic
load tests.

## Installing

Install it via [poetry](https://python-poetry.org/) with:

``` sh
$ cd tracking-load-faker/
$ poetry install
```

## Usage

Invoke `locust` pointing to the locustfile in the project:

``` sh
$ locust -f tracking_load_faker/locustfile.py
```

