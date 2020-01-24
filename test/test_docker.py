from pathlib import Path
import subprocess
from uuid import uuid4

PACKAGE_ROOT = str(Path(__file__).absolute().parent.parent)


def test_docker_image():
    tag = 'tracking-load-faker-' + uuid4().hex
    subprocess.run([
        'docker', 'build', '-t', tag, '.',
    ], cwd=PACKAGE_ROOT, check=True, capture_output=True)

    process = subprocess.run([
        'docker', 'run', '--rm', tag,
        '--help',
    ], cwd=PACKAGE_ROOT, capture_output=True, text=True)
    assert process.returncode == 0
    assert 'usage: locust-tracking-load-faker' in process.stdout
