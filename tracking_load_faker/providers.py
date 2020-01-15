#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Faker providers for tracking request generation
'''

from collections import OrderedDict
from typing import Iterable, Tuple
from urllib.parse import urljoin, quote as urlquote

from faker import Faker
from faker.providers import BaseProvider

from ._utils import get_faker_data, get_subclasses


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


def get_all_providers() -> Iterable[TrackingBaseProvider]:
    '''
    Returns a list with all the providers derived from TrackingBaseProvider.

    If you're not using `TrackingFaker`, you should use this function to manually
    add all providers to your Faker instance, because some are inter-dependent:

    >>> for p in get_all_providers():
    ...     fake.add_provider(p)
    '''
    return get_subclasses(TrackingBaseProvider)


class PageUrlProvider(TrackingBaseProvider):
    '''
    Generates page URLs.

    >>> fake.page_url()
    'http://forums.piwik.org'
    >>> fake.page_url()
    '/docs/update'
    '''
    data = get_faker_data('page_url')

    def page_url(self) -> str:
        return self.random_element(self.data)


class ProductNameProvider(TrackingBaseProvider):
    '''
    Generates product names.

    >>> fake.product_name()
    'My Product'
    >>> fake.product_name()
    'My Awesome Product'
    '''
    data = get_faker_data('product_name')

    def product_name(self) -> str:
        return self.random_element(self.data)


class ResolutionProvider(TrackingBaseProvider):
    '''
    Generates resolution data.

    >>> fake.resolution()
    ('2048', '1152')
    >>> fake.resolution()
    ('800', '600')
    '''
    data = get_faker_data('resolution')

    def resolution(self) -> Tuple[str, str]:
        return self.random_element(self.data)


class GenderProvider(TrackingBaseProvider):
    '''
    Generates genders, including an empty string for non-declared.

    >>> fake.gender()
    'Male'
    >>> fake.gender()
    ''
    '''
    data = get_faker_data('gender')

    def gender(self) -> str:
        return self.random_element(self.data)


class AcceptLanguageProvider(TrackingBaseProvider):
    '''
    Generates Accept-Languages specs, including empty string for non-specified.

    >>> fake.accept_language()
    'el,fi;q=0.5'
    >>> fake.accept_language()
    ''
    '''
    data = get_faker_data('accept_language')

    def accept_language(self) -> str:
        return self.random_element(self.data)


class SearchEngineProvider(TrackingBaseProvider):
    '''
    Generates search engine names, including an empty string for non-specified.

    >>> fake.search_engine()
    'Bing'
    >>> fake.search_engine()
    ''
    '''
    data = get_faker_data('search_engine')

    def search_engine(self) -> str:
        return self.random_element(self.data)


class SearchEngineUrlWithoutKeywordProvider(TrackingBaseProvider):
    '''
    Generates search engine URLs without a keyword specifier.

    >>> fake.search_engine_url_without_keyword()
    'https://www.bing.com/'
    >>> fake.search_engine_url_without_keyword()
    'https://duckduckgo.com/'
    '''
    data = get_faker_data('search_engine_url_without_keyword')

    def search_engine_url_without_keyword(self) -> str:
        return self.random_element(self.data)


class SearchEngineUrlWithKeywordProvider(TrackingBaseProvider):
    '''
    Generates search engine URLs with a keyword specifier (default: 'python')

    >>> fake.search_engine_url_with_keyword()
    'http://www.bing.com/search?q=python'
    >>> fake.search_engine_url_with_keyword('not a dollar to my name')
    'http://search.yahoo.com/search;?p=not%20a%20dollar%20to%20my%20name'
    '''
    data = get_faker_data('search_engine_url_with_keyword')

    def search_engine_url_with_keyword(self, keyword: str = 'python') -> str:
        base = self.random_element(self.data)
        return base + urlquote(keyword)


class ReferrerProvider(TrackingBaseProvider):
    '''
    Generates referrer URLs.

    >>> fake.referrer()
    'https://github.com'
    >>> fake.referrer()
    'http://www.bing.com/search?q=cool%20package'
    '''
    data = get_faker_data('referrer')

    def referrer(self) -> str:
        url_referrer = self.generator.url()
        word = self.generator.word()
        url_keyword = self.generator.search_engine_url_with_keyword(word)
        url_no_keyword = self.generator.search_engine_url_without_keyword()

        # Using the same relative frequencies as in plugin-visitorGenerator
        return self.random_element(
            [''] * 3 +
            [url_referrer] * 9 +
            [url_no_keyword] * 4 +
            [url_keyword] * 9 +
            self.data
        )


class RegionProvider(TrackingBaseProvider):
    '''
    Generates region codes.

    >>> fake.region()
    'CA'
    >>> fake.region()
    'QC'
    '''
    data = get_faker_data('region')

    def region(self):
        return self.random_element(self.data)


class BiasedBoolProvider(TrackingBaseProvider):
    '''
    Generates booleans sampled from a biased distribution.

    >>> fake.biased_bool()
    True
    >>> fake.biased_bool(bias=0.01)
    False
    '''

    def biased_bool(self, bias=0.5):
        return self.random_element(OrderedDict([
            (True, bias),
            (False, 1.0 - bias),
        ]))


class TrackingRequestProvider(TrackingBaseProvider):
    '''
    Generates data for a Matomo tracking request (!).
    '''

    def tracking_request(
        self,
        base_url: str = 'http://example.com/',
        id_site: int = 1,
    ):
        return {
            'action_name': self.generator.sentence(),
            'idsite': str(id_site),
            'rec': '1',
            'apiv': '1',
            'url': urljoin(base_url, self.generator.page_url()),
        }
