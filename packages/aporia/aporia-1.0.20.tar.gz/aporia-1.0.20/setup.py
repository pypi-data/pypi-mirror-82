# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aporia', 'aporia.api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'simpleflake>=0.1.5,<0.2.0',
 'tenacity>=6.2.0,<7.0.0',
 'ujson==3.2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

setup_kwargs = {
    'name': 'aporia',
    'version': '1.0.20',
    'description': 'Aporia SDK',
    'long_description': '# Aporia SDK',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aporia-ai/sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
