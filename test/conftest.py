import requests
from contextlib import contextmanager
import multiprocessing
import time

from pytest import fixture
from pytest_cov.embed import cleanup_on_sigterm

from tracking_load_faker.utils import run_simple_ping_server

cleanup_on_sigterm()


@fixture(scope='session')
def ping_server():
    @contextmanager
    def run_ping_server(port=9999, timeout=5):
        p = multiprocessing.Process(
            target=run_simple_ping_server,
            args=(port,),
        )
        p.start()
        try:
            url = f'http://127.0.0.1:{port}/ping'
            t0 = time.time()

            while time.time() - t0 < timeout:
                try:
                    r = requests.get(url, verify=False)
                except requests.exceptions.RequestException:
                    time.sleep(.500)
                else:
                    if r.ok:
                        break
            else:
                raise RuntimeError(
                    f'Server took longer than {timeout}s to start')

            yield url
        finally:
            p.terminate()
            p.join()

    return run_ping_server
