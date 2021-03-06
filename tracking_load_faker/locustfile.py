import os
from urllib3.exceptions import InsecureRequestWarning

from locust import between, HttpLocust, TaskSet, task
import requests

from tracking_load_faker.providers import TrackingFaker


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class TrackingRequestBehavior(TaskSet):
    def on_start(self):
        self.faker = TrackingFaker()

    @task
    def track_request(self):
        params = self.faker.tracking_request(
            id_site=self.locust.id_site,
            base_url=self.locust.base_url,
        )
        r = self.client.get(
            self.locust.tracker_subpath,
            params=params,
            verify=False,
        )
        r.raise_for_status()


class TrackingRequest(HttpLocust):
    task_set = TrackingRequestBehavior

    host = os.getenv('MATOMO_REMOTE_HOST')
    assert host, 'MATOMO_REMOTE_HOST is empty'

    wait_time = between(
        float(os.getenv('LOCUST_MIN_WAIT', '30')) / 100.0,
        float(os.getenv('LOCUST_MAX_WAIT', '90')) / 100.0,
    )

    id_site = int(os.getenv('MATOMO_SITE_ID', '1'))
    assert id_site > 0, f'Invalid MATOMO_SITE_ID={id_site}'

    base_url = os.getenv('MATOMO_SITE_BASE_URL', 'http://example.com/')
    assert base_url, 'Empty MATOMO_SITE_BASE_URL'
    assert base_url.endswith('/'), "MATOMO_SITE_BASE_URL doesn't end with '/'"

    tracker_subpath = os.getenv('MATOMO_TRACKER_SUBPATH', 'matomo.php')
    assert tracker_subpath, 'Empty MATOMO_TRACKER_SUBPATH'
