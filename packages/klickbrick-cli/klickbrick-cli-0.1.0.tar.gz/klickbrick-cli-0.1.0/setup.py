# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['klickbrick_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'klickbrick-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marcel van den Brink',
    'author_email': 'm.vandenbrink@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
