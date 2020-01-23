#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Generates real fake sequences of visit actions.
'''

from typing import Iterator, Mapping

from tracking_load_faker.providers import Provider as TrackingProvider


VisitAction = Mapping[str, str]


def visit_action_sequence(
    base_url: str,
    fake: TrackingProvider,
) -> Iterator[VisitAction]:
    '''
    Yields a sequence of user actions in a visit.

    Args:
        base_url: base URL of all internal paths
        faker: a TrackingProvider instance to draw data from
    '''

    action = fake.page_action(base_url, 'page')
    action['new_visit'] = '1'
    prev_url = fake.referrer()
    i = 0

    while True:
        action['urlref'] = prev_url
        if action['type'] == 'page':
            action['pv_id'] = fake.page_view_id()
        yield action.copy()

        if action['type'] != 'page' or i > 10:
            break

        for event in fake.tracking_events():
            event_action = dict(
                action,
                new_visit='0',
                e_c=event.category,
                e_a=event.action,
                e_n=event.name,
            )
            yield event_action

        prev_url = action['url']
        action = fake.page_action(base_url)
        i += 1
