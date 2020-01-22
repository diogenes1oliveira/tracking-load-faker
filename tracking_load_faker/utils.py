'''
Utility functions to deal with Faker data
'''

from contextlib import wraps
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import os

import yaml

HERE = os.path.abspath(os.path.dirname(__file__))
FAKER_DATA_DIR = os.path.join(HERE, 'faker-data')


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

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            kwargs = kwargs or {}
            kwargs[arg_name] = get_faker_data(basename, search_path)
            return f(*args, **kwargs)
        return inner
    return decorator


def get_subclasses(cls: type):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


def run_simple_ping_server(port=9999):
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(self.path.encode('utf-8'))

        def log_request(self, *args, **kwargs):
            pass

    server = ThreadingHTTPServer(('', port), RequestHandler)
    server.serve_forever()
