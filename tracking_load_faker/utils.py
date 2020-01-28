'''
Utility functions to deal with Faker data
'''

from contextlib import wraps
import os
from typing import Iterable

import yaml

HERE = os.path.abspath(os.path.dirname(__file__))
FAKER_DATA_DIR = os.path.join(HERE, 'faker_data')


def get_faker_data(basename: str, search_path: str = None):
    f'''
    Returns the contents of the Faker data YAML file with the given basename.

    Args:
        basename: name of the file without the '.yaml' extension
        search_path: where to look up the file. Defaults to the value of the
            environment variable FAKER_DATA_DIR or the package directory
            in {FAKER_DATA_DIR}
    '''
    search_path = search_path or os.getenv('FAKER_DATA_DIR') or FAKER_DATA_DIR
    file_path = os.path.join(search_path, basename + '.yaml')
    with open(file_path) as fp:
        return yaml.load(fp, Loader=yaml.SafeLoader)


def faker_data(basename, search_path: str = None, arg_name: str = 'data'):
    f'''
    Decorator to inject the Faker data as an argument to the function.

    Args:
        basename: name of the file without the '.yaml' extension
        search_path: where to look up the file. Defaults to the value of the
            environment variable FAKER_DATA_DIR or the package directory
            in {FAKER_DATA_DIR}
        arg_name: name of the argument to be injected. Defaults to 'data'
    '''
    data = get_faker_data(basename, search_path)

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            kwargs = kwargs or {}
            kwargs[arg_name] = data
            return f(*args, **kwargs)
        return inner
    return decorator


def get_subclasses(cls: type) -> Iterable[type]:
    '''
    Iterates through the subclasses of the given class
    '''
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass
