# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycomply']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pycomply',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Ashutosh Bandiwdekar',
    'author_email': 'ashutoshb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
