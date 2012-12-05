config = {
 'description': 'regetron is a simple shell for playing with regular expressions',
 'author': 'Zed A. Shaw',
 'url': 'https://gitorious.org/regetron/regetron',
 'download_url': 'http://pypi.python.org/pypi/regetron',
 'author_email': 'zedshaw@zedshaw.com',
 'version': '1.4',
 'install_requires': [],
 'packages': ['regetron'],
 'name': 'regetron'
}

try:
    from setuptools import setup

    config['entry_points'] = {
            'console_scripts' : [
                'regetron = regetron.cmdline:main'
            ],
    }

except ImportError:
    from distutils.core import setup

    config['scripts'] = ['bin/regetron', 'bin/regetron.bat']

setup(**config)

