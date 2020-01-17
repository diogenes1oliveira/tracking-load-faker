# tracking-load-faker

Run load tests against tracking services (like Matomo) using Faker to generate
visits

[![Build Status](https://api.travis-ci.org/python/mypy.svg?branch=master)](https://travis-ci.org/python/mypy)
[![codecov](https://codecov.io/gh/diogenes1oliveira/tracking-load-faker/branch/master/graph/badge.svg)](https://codecov.io/gh/diogenes1oliveira/tracking-load-faker)

--------

## About

This project generates fake visits and actions based on the Matomo plugin
[VisitorGenerator](https://github.com/matomo-org/plugin-VisitorGenerator),
sending them to the tracker URL to simulate real users.

## Running

Invoke locust with:

```shell
locust -f matomo_locust_test/locustfile.py
```

### Environment Variables

The following environment variables are available for configuration:

| Name                     | Description                                     | Default             |
| ------------------------ | ----------------------------------------------- | ------------------- |
| `FAKER_DATA_DIR`         | Directory to lookup faker data files            | `None`              |
| `LOCUST_MAX_WAIT`        | Maximum wait time (ms)                          | `900`               |
| `LOCUST_MIN_WAIT`        | Minimum wait time (ms)                          | `300`               |
| `MATOMO_SITE_BASE_URL`   | Base URL of the site to be simulated            | http://example.com/ |
| `MATOMO_SITE_ID`         | ID of the simulated site in the Matomo instance | `1`                 |
| `MATOMO_TRACKER_SUBPATH` | Subpath for the tracker JS file                 | `matomo.js`         |
