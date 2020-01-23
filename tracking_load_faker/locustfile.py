import os
import time

from locust import between, HttpLocust, TaskSet, task
from requests.packages import urllib3

from tracking_load_faker.providers import TrackingFaker
from tracking_load_faker.visits import visit_action_sequence


urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


class TrackingRequestBehavior(TaskSet):
    def on_start(self):
        self.fake = TrackingFaker()
        self.user_params = self.fake.visitor_params()

    @task
    def track_request(self):
        for action_params in visit_action_sequence(
            base_url=self.locust.base_url,
            fake=self.fake,
        ):
            action_params.update(
                self.user_params,
                idsite=str(self.locust.id_site),
                apiv='1',
                rec='1',
            )
            r = self.client.get(
                self.locust.tracker_subpath,
                params=action_params,
                verify=False,
            )
            time.sleep(0.1)
            r.raise_for_status()


class TrackingRequest(HttpLocust):
    task_set = TrackingRequestBehavior

    host = os.getenv('MATOMO_REMOTE_HOST')
    assert host, 'MATOMO_REMOTE_HOST is empty'

    wait_time = between(
        float(os.getenv('LOCUST_MIN_WAIT', '30')) / 1000.0,
        float(os.getenv('LOCUST_MAX_WAIT', '90')) / 1000.0,
    )

    id_site = int(os.getenv('MATOMO_SITE_ID', '1'))
    assert id_site > 0, f'Invalid MATOMO_SITE_ID={id_site}'

    base_url = os.getenv('MATOMO_SITE_BASE_URL', 'http://example.com/')
    assert base_url, 'Empty MATOMO_SITE_BASE_URL'
    assert base_url.endswith('/'), "MATOMO_SITE_BASE_URL doesn't end with '/'"

    tracker_subpath = os.getenv('MATOMO_TRACKER_SUBPATH', 'matomo.php')
    assert tracker_subpath, 'Empty MATOMO_TRACKER_SUBPATH'
