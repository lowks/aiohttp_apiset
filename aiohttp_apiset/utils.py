import collections
import os
import re
from urllib import parse


Route = collections.namedtuple('Route', 'method url handler')


def to_name(name):
    name = name.replace('/', '.')
    name = name.replace('{', '')
    name = name.replace('}', '')
    return name


def find_file(file_path: str, search_dirs: list, *,
              base_file: str=None, base_dir: str=None) -> str:
    if file_path.startswith('/'):
        return file_path

    elif file_path.startswith('.'):
        if not base_dir and base_file:
            base_dir = os.path.dirname(base_file)
        if base_dir:
            f = os.path.join(base_dir, file_path)
            return os.path.normpath(f)

    for base_dir in search_dirs:
        f = os.path.join(base_dir, file_path)
        f = os.path.normpath(f)
        if os.path.exists(f):
            return f
    raise FileNotFoundError(file_path)


def url_normolize(url: str):
    """
    >>> url_normolize('//api/1/../../status')
    '/status'
    >>> url_normolize('//api/1/../../status/')
    '/status/'
    >>> url_normolize('/api/1/../../status/')
    '/status/'
    >>> url_normolize('///api/1/../../status/')
    '/status/'
    """
    u = parse.urljoin('///{}/'.format(url), '.')
    return u if url.endswith('/') else u[:-1]


re_patt = re.compile('\{(\w+):.*?\}')


def re_patt_replacer(m):
    return '{%s}' % m.group(1)


def remove_patterns(url: str):
    """
    >>> remove_patterns('/{w:\d+}x{h:\d+}')
    '/{w}x{h}'
    """
    return re_patt.sub(re_patt_replacer, url)


def sort_key(x):
    """
    >>> sort_key(('name', ('GET', 'URL', 'HANDLER')))
    -3
    """
    name, (m, u, h) = x
    return - len(u) + u.count('}') * 100
