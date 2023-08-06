# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['twitter_blocklist']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'progressbar2>=3.51.3,<4.0.0',
 'python-twitter>=3.5,<4.0',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'test': ['pytest>=5.4.3,<6.0.0', 'nbval>=0.9.6,<0.10.0']}

entry_points = \
{'console_scripts': ['twitter_blocklist = twitter_blocklist.console:main']}

setup_kwargs = {
    'name': 'twitter-blocklist',
    'version': '0.6.0',
    'description': 'Export and import Twitter blocklists',
    'long_description': "![Python package](https://github.com/zonca/twitter_blocklist/workflows/Python%20package/badge.svg)\n[![PyPI version](https://badge.fury.io/py/twitter-blocklist.svg)](https://badge.fury.io/py/twitter-blocklist)\n\n# `twitter_blocklist`\n\nExport and import Twitter blocklists.\n\n## Execute on Google Colaboratory\n\nIt can also be used in the Google Colaboratory Notebook without installing anything\nin the local machine, this also includes the documentation:\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zonca/twitter_blocklist/blob/master/run_twitter_blocklist.ipynb)\n\n\n## Documentation and execution\n\nIt can also be executed from a Notebook, which also includes instructions\nfor setting it up and step-by-step explanation, see:\n\n* <`run_twitter_blocklist.ipynb`>\n\n\n## Quick reference\n\n`twitter_blocklist` provides a command-line tool to export a list of all\nthe accounts you block to a text file:\n\n    $ twitter_blocklist --export my_blocks.csv\n\nor import a list from someone else, or downloaded from <https://blocktogether.org>:\n\n    $ twitter_blocklist list_to_import.csv\n\nor block all member of a Twitter list:\n\n    $ twitter_blocklist --list <list_id>\n\nundo blocking with the --unblock flag:\n\n    $ twitter_blocklist --unblock --list <list_id>\n    $ twitter_blocklist --unblock list_to_unblock.csv\n\nConsider that Twitter rate-limits their APIs, I have setup the client to automatically\nsleep in case of a rate-limiting error, in case that happens, just leave the script\nrunning and it will complete at some point. For example exporting the blocks needs\nto make 1 request every 5000 blocked IDs, so you could hit the limit of 15 requests\nevery 15 minutes, in that case the script will sleep for 15 minutes and then resume.\n\n## Install\n\n    $ pip install twitter_blocklist\n\n## Initial setup\n\nCreate a Twitter app following the [instructions from the `python-twitter` project](https://python-twitter.readthedocs.io/en/latest/getting_started.html)\n\nCreate a text file named `twitter_keys.toml` with this format:\n\n```\nconsumer_key='xxxxxxxxxxxxxxxxxxxxxxxxx'\nconsumer_secret='xxxxxxxxxxxxxxxxxxxxxxxxx'\naccess_token_key='xxxxxxxxxxxxxxxxxxxxxxxxx'\naccess_token_secret='xxxxxxxxxxxxxxxxxxxxxxxxx'\n```\n\nMake sure you have the single quotes.\n\nFrom the same folder where you have `twitter_keys.toml`, run the tool as shown above.\n",
    'author': 'Andrea Zonca',
    'author_email': 'code@andreazonca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zonca/twitter_blocklist',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
