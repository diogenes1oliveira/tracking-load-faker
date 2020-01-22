
from pathlib import Path

import pytest

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

    basenames = (
        'page_action',
        'product_name',
        'resolution',
        'gender',
        'accept_language',
        'search_engine',
        'search_engine_url_without_keyword',
        'search_engine_url_with_keyword',
        'referrer',
        'region',
        'biased_bool',
        'tracking_events',
    )

    for basename in basenames:
        fake.seed_instance(42)
        generated1 = getattr(fake, basename)()

        fake.seed_instance(42)
        generated2 = getattr(fake, basename)()

        assert generated1 is not None
        assert generated2 is not None
        assert generated1 == generated2


def test_provider_page_action():
    fake = providers.TrackingFaker()

    with pytest.raises(ValueError):
        fake.page_action(action_type='INVALID ACTION')

    for action_type in ('file', 'link', 'page'):
        fake.seed_instance(42)
        generated1 = fake.page_action(action_type=action_type)

        fake.seed_instance(42)
        generated2 = fake.page_action(action_type=action_type)

        assert generated1 is not None
        assert generated2 is not None
        assert generated1 == generated2


def test_provider_page_view():
    fake = providers.TrackingFaker()

    with pytest.raises(ValueError):
        fake.page_action(action_type='INVALID ACTION')

    for action_type in ('file', 'link', 'page'):
        fake.seed_instance(42)
        generated1 = fake.page_view(
            base_url='http://my/',
            action_type=action_type,
        )

        fake.seed_instance(42)
        generated2 = fake.page_view(
            base_url='http://my/',
            action_type=action_type,
        )

        assert generated1 is not None
        assert generated2 is not None
        assert generated1 == generated2
