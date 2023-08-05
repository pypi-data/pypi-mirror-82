# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxbos',
 'pyxbos.drivers',
 'pyxbos.drivers.bacnet',
 'pyxbos.drivers.dark_sky',
 'pyxbos.drivers.hue',
 'pyxbos.drivers.obvius',
 'pyxbos.drivers.parker',
 'pyxbos.drivers.pbc',
 'pyxbos.drivers.system_monitor',
 'pyxbos.drivers.weather_current',
 'pyxbos.drivers.weather_prediction',
 'pyxbos.wave']

package_data = \
{'': ['*'],
 'pyxbos': ['wavemq/*'],
 'pyxbos.drivers.bacnet': ['buildings/orinda-public-library/*']}

install_requires = \
['aiogrpc>=1.6,<2.0',
 'beautifulsoup4>=4.7,<5.0',
 'googleapis-common-protos>=1.5,<2.0',
 'grpcio-tools>=1.18,<2.0',
 'grpcio>=1.18,<2.0',
 'jq>=0.1.6,<0.2.0',
 'tlslite-ng>=0.7.5,<0.8.0',
 'toml>=0.10.0,<0.11.0',
 'xxhash>=1.3,<2.0']

setup_kwargs = {
    'name': 'pyxbos',
    'version': '0.2.33',
    'description': 'Python bindings for XBOS-flavored WAVEMQ and related services',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
