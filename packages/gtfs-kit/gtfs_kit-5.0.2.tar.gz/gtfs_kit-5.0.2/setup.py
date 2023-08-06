# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtfs_kit']

package_data = \
{'': ['*']}

install_requires = \
['folium<1',
 'geopandas<1',
 'json2html<2',
 'pandas<2',
 'pycountry<20',
 'requests>=2.23,<3.0',
 'rtree>=0.8.3',
 'shapely<2',
 'utm<1']

setup_kwargs = {
    'name': 'gtfs-kit',
    'version': '5.0.2',
    'description': 'A Python 3.6.1+ library for analyzing GTFS feeds.',
    'long_description': 'GTFS Kit\n********\n.. image:: https://travis-ci.org/mrcagney/gtfs_kit.svg?branch=master\n    :target: https://travis-ci.org/mrcagney/gtfs_kit\n\nGTFS Kit is a Python 3.6+ kit for analyzing `General Transit Feed Specification (GTFS) <https://en.wikipedia.org/wiki/GTFS>`_ data in memory without a database.\nIt uses Pandas and Shapely to do the heavy lifting.\n\nThis project supersedes `GTFSTK <https://github.com/mrcagney/gtfstk>`_.\n\n\nInstallation\n=============\n``pip install gtfs_kit``.\n\n\nExamples\n========\nExamples are in the Jupyter notebook ``notebooks/examples.ipynb``.\n\n\nAuthors\n=========\n- Alex Raichev, 2019-09\n\n\nDocumentation\n=============\nOn Github Pages `here <https://mrcagney.github.io/gtfs_kit_docs>`_.\n\n\nNotes\n=====\n- Development status is Alpha\n- This project uses semantic versioning\n- Thanks to `MRCagney <http://www.mrcagney.com/>`_ for donating to this project\n- Constructive feedback and code contributions welcome. Please issue pull requests into the ``develop`` branch and include tests.\n',
    'author': 'Alex Raichev',
    'author_email': 'araichev@mrcagney.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrcagney/gtfs_kit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
