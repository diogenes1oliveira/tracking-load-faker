import csv
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from urllib.parse import urljoin


PACKAGE_ROOT = Path(__file__).absolute().parent.parent


def test_server(ping_server):
    with ping_server(timeout=5) as url, TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        args = [
            'locust-tracking-load-faker',
            '--endpoint', urljoin(url, '/ping'),
            '--',
            '--no-web',
            '-c', '1',
            '-t', '1s',
            '--loglevel', 'ERROR',
            '--only-summary',
            '--csv', str(tmp_path / 'cc'),
        ]
        process = subprocess.run(args)
        assert process.returncode == 0

        with open(str(tmp_path / 'cc_stats_history.csv'), newline='') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                assert int(row["# requests"]) > 0
                assert int(row["# failures"]) == 0
