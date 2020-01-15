import csv
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


PACKAGE_ROOT = Path(__file__).absolute().parent.parent


def test_server(ping_server):
    locust_file = str(PACKAGE_ROOT / 'tracking_load_faker' / 'locustfile.py')

    with ping_server(timeout=5) as url, TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        args = [
            'locust',
            '-f', locust_file,
            '--no-web',
            '-c', '1',
            '-t', '1s',
            '--loglevel', 'ERROR',
            '--only-summary',
            '--csv', str(tmp_path / 'cc'),
        ]
        env = os.environ.copy()
        env.update(MATOMO_REMOTE_HOST=url)
        process = subprocess.run(args, env=env)
        assert process.returncode == 0

        with open(str(tmp_path / 'cc_stats_history.csv'), newline='') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                assert int(row["# requests"]) > 0
                assert int(row["# failures"]) == 0
