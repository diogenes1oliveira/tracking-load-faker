#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
from urllib.parse import urlparse, urlunparse

HERE = os.path.abspath(os.path.dirname(__file__))
LOCUST_FILE = os.path.join(HERE, 'locustfile.py')


def main():
    parser = argparse.ArgumentParser(
        description='Run Locust against the default locustfile',
        epilog='All arguments after -- are passed to locust',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-f', '--locustfile', default=LOCUST_FILE,
        help='path to the locustfile',
    )
    parser.add_argument(
        '--max-wait-time', type=int, default=90,
        help='Maximum wait time between tasks (ms)',
    )
    parser.add_argument(
        '--min-wait-time', type=int, default=30,
        help='Minimum wait time between tasks (ms)',
    )
    parser.add_argument(
        '-e', '--endpoint', default='http://localhost:8080/matomo.php',
        help='Endpoint to send the requests to',
    )
    parser.add_argument(
        '-d', '--faker-data-dir', default='',
        help='Directory to lookup faker data files',
    )
    parser.add_argument(
        '-s', '--site-id', type=int, default=1,
        help='ID of the simulated site in the Matomo instance',
    )
    parser.add_argument(
        '-u', '--base-url', default='http://example.com/',
        help='Base URL of the site to be simulated',
    )
    parser.add_argument(
        'locust_args', nargs=argparse.REMAINDER,
        help='passed straight to the Locust command',
    )
    args = parser.parse_args()
    locust_args = []

    if args.locust_args and args.locust_args[0] == '--':
        locust_args = args.locust_args[1:]

    cmd_args = ['locust'] + ['-f', args.locustfile] + locust_args
    endpoint_parsed = urlparse(args.endpoint)

    env = dict(
        os.environ,
        FAKER_DATA_DIR=args.faker_data_dir,
        LOCUST_MAX_WAIT=str(args.max_wait_time),
        LOCUST_MIN_WAIT=str(args.max_wait_time),
        MATOMO_SITE_BASE_URL=args.base_url,
        MATOMO_SITE_ID=str(args.site_id),
        MATOMO_REMOTE_HOST=urlunparse((
            endpoint_parsed.scheme,
            endpoint_parsed.netloc,
            '', '', '', '',
        )) + '/',
        MATOMO_TRACKER_SUBPATH=endpoint_parsed.path,
    )

    process = subprocess.run(cmd_args, env=env)
    sys.exit(process.returncode)
