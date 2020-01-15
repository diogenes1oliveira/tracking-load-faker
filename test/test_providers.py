
from pathlib import Path
import re

import inflection

from tracking_load_faker import providers

# Assuming the structure:
# ROOT
# - tracking_load_faker
#   - faker-data
# - test
#    - test_providers.py

PACKAGE_ROOT = Path(__file__).absolute().parent.parent
FAKER_DATA_DIR = PACKAGE_ROOT / 'tracking_load_faker' / 'faker-data'


def test_providers():
    fake = providers.TrackingFaker()
    all_providers = list(providers.get_all_providers())
    assert len(all_providers)

    for provider in all_providers:
        basename = inflection.underscore(
            re.sub('Provider$', '', provider.__name__),
        )

        fake.seed_instance(42)
        generated1 = getattr(fake, basename)()

        fake.seed_instance(42)
        generated2 = getattr(fake, basename)()

        assert generated1 == generated2
