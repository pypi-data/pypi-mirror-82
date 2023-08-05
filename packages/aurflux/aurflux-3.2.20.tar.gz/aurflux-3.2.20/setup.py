# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurflux',
 'aurflux.cog',
 'aurflux.command',
 'aurflux.context',
 'aurflux.utils']

package_data = \
{'': ['*']}

install_requires = \
['aurcore',
 'discord.py',
 'loguru>=0.5.2,<0.6.0',
 'pyyaml',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'aurflux',
    'version': '3.2.20',
    'description': 'Aurflux!',
    'long_description': None,
    'author': 'Zenith',
    'author_email': 'inbox@zenith.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
