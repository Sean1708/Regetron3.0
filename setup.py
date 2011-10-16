try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
 'description': 'regetron is a simple shell for playing with regular expressions',
 'author': 'Zed A. Shaw',
 'url': 'https://gitorious.org/regetron/regetron',
 'download_url': 'http://pypi.python.org/pypi/regetron',
 'author_email': 'zedshaw@zedshaw.com',
 'version': '1.0',
 'install_requires': [],
 'packages': ['regetron'],
 'scripts': ['bin/regetron'],
 'name': 'regetron'
}
setup(**config)

