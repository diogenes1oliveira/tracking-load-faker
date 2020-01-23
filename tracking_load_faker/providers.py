#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Faker providers for tracking request generation
'''

from collections import OrderedDict
import string
from typing import Any, Iterable, List, Mapping, NamedTuple, Tuple
from urllib.parse import urljoin, quote as urlquote

from faker import Faker
from faker.providers import BaseProvider

from tracking_load_faker.utils import faker_data, get_subclasses


class TrackingBaseProvider(BaseProvider):
    '''
    Base class for all providers in this module.
    '''


class TrackingFaker(Faker):
    '''
    An otherwise normal `Faker` instance that registers all providers at
    init time.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Obs: all arguments are forwarded to the Faker() constructor.
        '''
        super().__init__(*args, **kwargs)
        for p in get_all_providers():
            self.add_provider(p)


class EventInfo(NamedTuple):
    category: str
    action: str
    name: str


def get_all_providers() -> Iterable[TrackingBaseProvider]:
    '''
    Returns a list with all the providers derived from TrackingBaseProvider.

    If you're not using `TrackingFaker`, you should use this function to
    manually add all providers to your Faker instance, because some are
    inter-dependent:

    >>> for p in get_all_providers():
    ...     fake.add_provider(p)
    '''
    return get_subclasses(TrackingBaseProvider)


class Provider(TrackingBaseProvider):
    @faker_data('external_url', arg_name='link_data')
    @faker_data('internal_page', arg_name='page_data')
    @faker_data('internal_file', arg_name='file_data')
    def page_action(
        self,
        base_url: str = '',
        action_type: str = '',
        link_data: List[str] = None,
        page_data: Mapping[str, str] = None,
        file_data: List[str] = None,
    ) -> Mapping[str, str]:
        '''
        Generates page actions.

        Arguments:
            base_url: URL to be used as a prefix for the internal paths
            action_type: type of action to be generated, from 'link', 'page' or
            'file'. By defaults picks one randomly

        >>> fake.page_action()
        {'type': 'link', 'url': 'http://forums.piwik.org'}
        >>> fake.page_action()
        {'title': 'Blog', 'type': 'page', 'url': '/blog'}
        '''
        action_type = action_type or self.random_element(OrderedDict([
            ('link', len(link_data)),
            ('page', len(page_data)),
            ('file', len(file_data)),
        ]))
        if action_type == 'page':
            page = self.random_element(page_data)
            return {
                'action_name': page['title'],
                'type': 'page',
                'url': urljoin(base_url, page['path']),
            }
        elif action_type == 'file':
            file_link = self.random_element(file_data)
            url = urljoin(base_url, file_link)
            return {
                'action_name': '',
                'type': 'download',
                'url': url,
                'download': url,
            }
        elif action_type == 'link':
            url = self.random_element(link_data)
            return {
                'action_name': '',
                'type': 'link',
                'url': url,
                'link': url,
            }
        else:
            raise ValueError('Unrecognized action type: %r' % action_type)

    @faker_data('product_name')
    def product_name(self, data: List[str] = None) -> str:
        '''
        Generates product names.

        >>> fake.product_name()
        'My Product'
        >>> fake.product_name()
        'My Awesome Product'
        '''
        return self.random_element(data)

    @faker_data('resolution')
    def resolution(self, data: List[str] = None) -> Tuple[str, str]:
        '''
        Generates resolution data.

        >>> fake.resolution()
        ('2048', '1152')
        >>> fake.resolution()
        ('800', '600')
        '''
        return self.random_element(data)

    @faker_data('gender')
    def gender(self, data: List[str] = None) -> str:
        '''
        Generates genders, including an empty string for non-declared.

        >>> fake.gender()
        'Male'
        >>> fake.gender()
        ''
        '''
        return self.random_element(data)

    @faker_data('accept_language')
    def accept_language(self, data: List[str] = None) -> str:
        '''
        Generates Accept-Languages specs, including empty string for
        non-specified.

        >>> fake.accept_language()
        'el,fi;q=0.5'
        >>> fake.accept_language()
        ''
        '''
        return self.random_element(data)

    @faker_data('search_engine')
    def search_engine(self, data: List[str] = None) -> str:
        '''
        Generates search engine names, including an empty string for
        non-specified.

        >>> fake.search_engine()
        'Bing'
        >>> fake.search_engine()
        ''
        '''
        return self.random_element(data)

    @faker_data('search_engine_url_without_keyword')
    def search_engine_url_without_keyword(
        self,
        data: List[str] = None,
    ) -> str:
        '''
        Generates search engine URLs without a keyword specifier.

        >>> fake.search_engine_url_without_keyword()
        'https://www.bing.com/'
        >>> fake.search_engine_url_without_keyword()
        'https://duckduckgo.com/'
        '''
        return self.random_element(data)

    @faker_data('search_engine_url_with_keyword')
    def search_engine_url_with_keyword(
        self,
        keyword: str = 'python',
        data: List[str] = None,
    ) -> str:
        '''
        Generates search engine URLs with a keyword specifier
        (default: 'python')

        >>> fake.search_engine_url_with_keyword()
        'http://www.bing.com/search?q=python'
        >>> fake.search_engine_url_with_keyword('not a dollar to my name')
        'http://search.yahoo.com/search;?p=not%20a%20dollar%20to%20my%20name'
        '''
        base = self.random_element(data)
        return base + urlquote(keyword)

    @faker_data('referrer')
    def referrer(
        self,
        base_url='',
        data: List[str] = None,
    ) -> str:
        '''
        Generates referrer URLs.

        >>> fake.referrer()
        'https://github.com'
        >>> fake.referrer()
        'http://www.bing.com/search?q=cool%20package'
        '''
        url_referrer = self.generator.url()
        word = self.generator.word()
        url_keyword = self.generator.search_engine_url_with_keyword(word)
        url_no_keyword = self.generator.search_engine_url_without_keyword()

        # Using the same relative frequencies as in plugin-visitorGenerator
        url = self.random_element(
            [''] * 3 +
            [url_referrer] * 9 +
            [url_no_keyword] * 4 +
            [url_keyword] * 9 +
            data
        )
        return urljoin(base_url, url)

    @faker_data('region')
    def region(self, data: List[str] = None) -> str:
        '''
        Generates region codes.

        >>> fake.region()
        'CA'
        >>> fake.region()
        'QC'
        '''
        return self.random_element(data)

    def biased_bool(self, bias: float = 0.5) -> bool:
        '''
        Generates booleans sampled from a biased distribution.

        >>> fake.biased_bool()
        True
        >>> fake.biased_bool(bias=0.01)
        False
        '''
        return self.random_element(OrderedDict([
            (True, bias),
            (False, 1.0 - bias),
        ]))

    def page_view_id(self):
        '''
        Generates identifiers for actions in a single page view.
        '''
        return self.generator.pystr_format(
            string_format='{{random_letter}}' * 6,
            letters=string.ascii_letters + string.digits,
        )

    def tracking_events(self) -> List[EventInfo]:
        '''
        Generates a list of tracking events for one page view.

        >>> fake.tracking_events()
        [
            EventInfo('Movie', 'play', 'A Good Movie'),
            EventInfo('Movie', 'stop', 'A Good Movie'),
            EventInfo('Movie', 'play', 'A Bad Movie'),
        ]
        >>> fake.tracking_events()
        []
        '''
        events = []

        if self.generator.biased_bool(0.10):
            events += [EventInfo('Movie', 'play', 'A Good Movie')]
            if self.generator.biased_bool(0.50):
                events += [EventInfo('Movie', 'pause', 'A Good Movie')]

        if self.generator.biased_bool(0.10):
            events += [EventInfo('Movie', 'play', 'A Bad Movie')]
            if self.generator.biased_bool(0.50):
                events += [EventInfo('Movie', 'stop', 'A Bad Movie')]

        return events

    def page_view(
        self,
        user_id: str = '',
        action_type: str = '',
        base_url: str = 'http://example.com/',
        id_site: int = 1,
    ) -> Mapping[str, Any]:
        '''
        Generates data for a Matomo page view (!).
        '''
        base_params = {
            'urlref': self.generator.referrer(base_url),
            'ua': self.generator.user_agent(),
            'lang': self.generator.accept_language(),
            'res': 'x'.join(self.generator.resolution()),
            'uid': user_id,
            'idsite': str(id_site),
            'rec': '1',
            'apiv': '1',
        }

        action = self.generator.page_action(
            base_url=base_url,
            action_type=action_type,
        )

        request_action = generate_tracking_request(
            action,
            action['type'] == 'page' and self.generator.biased_bool(0.10),
            params=base_params,
        )
        requests = [request_action]

        if action['type'] == 'page':
            base_params.update({
                'pv_id': self.generator.pystr_format(
                    string_format='{{random_letter}}' * 6,
                    letters=string.ascii_letters + string.digits,
                ),
            })
            requests += [
                generate_tracking_request(
                    action,
                    new_visit=False,
                    event=e,
                    params=base_params,
                )
                for e in self.generator.tracking_events()
            ]

        return requests


def generate_tracking_request(
    action,
    new_visit=False,
    event=None,
    params=None,
):
    action_data = {}
    if action['type'] in ('link', 'download'):
        action_data.update({action['type']: action['url']})

    if event:
        action_data['e_c'] = event.category
        action_data['e_n'] = event.name
        action_data['e_a'] = event.action

    return {
        'url': action['url'],
        **action_data,
        **(params or {}),
    }
