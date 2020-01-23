from unittest.mock import Mock

from tracking_load_faker.providers import EventInfo, Provider, TrackingFaker
from tracking_load_faker.visits import visit_action_sequence


def test_visit_action_sequence(monkeypatch):

    base_url = 'http://example.com/'
    actions = [
        TrackingFaker().page_action(base_url, 'page'),
        TrackingFaker().page_action(base_url, 'file'),
    ]

    def fake_page_action(*_, **__):
        return actions.pop(0)

    event = EventInfo('Song', 'play', 'The Sound Of Silence')
    monkeypatch.setattr(Provider, 'tracking_events',
                        Mock(return_value=[event]))
    monkeypatch.setattr(Provider, 'page_action', fake_page_action)

    fake = TrackingFaker()
    sequence = list(visit_action_sequence(base_url, fake))

    assert len(sequence) == 3

    assert sequence[0]['type'] == 'page'
    assert sequence[0]['new_visit'] == '1'

    assert sequence[1]['type'] == 'page'
    assert sequence[1]['new_visit'] != '1'
    assert sequence[2]['type'] == 'download'
