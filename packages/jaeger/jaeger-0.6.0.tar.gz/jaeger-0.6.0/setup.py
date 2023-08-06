# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['jaeger',
 'jaeger.actor',
 'jaeger.actor.commands',
 'jaeger.commands',
 'jaeger.interfaces',
 'jaeger.utils']

package_data = \
{'': ['*'], 'jaeger': ['etc/*']}

install_requires = \
['Click>=7.0,<8.0',
 'click_default_group>=1.2.2,<2.0.0',
 'daemonocle>=1.0.2,<2.0.0',
 'numpy>=1.15.1,<2.0.0',
 'progressbar2>=3.39.3,<4.0.0',
 'python-can>=3.1.1,<4.0.0',
 'sdss-clu>=0.5.0,<0.6.0',
 'sdss-drift>=0.1.5',
 'sdssdb>=0.4.5',
 'sdsstools>=0.4.2']

extras_require = \
{'docs': ['Sphinx>=3.0,<4.0', 'sphinx-click>=2.3.0,<3.0.0'],
 'serial': ['pyserial>=3.4,<4.0']}

entry_points = \
{'console_scripts': ['jaeger = jaeger.__main__:jaeger']}

setup_kwargs = {
    'name': 'jaeger',
    'version': '0.6.0',
    'description': 'Controllers for the SDSS-V FPS',
    'long_description': '# jaeger\n\n![Versions](https://img.shields.io/badge/python->3.7-blue)\n[![Documentation Status](https://readthedocs.org/projects/jaeger/badge/?version=latest)](https://sdss-jaeger.readthedocs.io/en/latest/?badge=latest)\n[![Build](https://img.shields.io/github/workflow/status/sdss/jaeger/Test)](https://github.com/sdss/jaeger/actions)\n[![codecov](https://codecov.io/gh/sdss/jaeger/branch/master/graph/badge.svg)](https://codecov.io/gh/sdss/jaeger)\n\n[jaeger](http://pacificrim.wikia.com/wiki/Jaeger>) provides high level control for the SDSS-V [Focal Plane System](https://wiki.sdss.org/display/FPS). Some of the features that jaeger provide are:\n\n- Wraps the low level CAN commands for simpler use.\n- Provides a framework that is independent of the CAN interface used (by using the python-can_ library).\n- Interfaces with kaiju_ to provide anticollision path planning for trajectories.\n- Implements status and position update loops.\n- Provides implementations for commonly used tasks (e.g., go to position, send trajectory).\n- Interfaces with the Instrument Electronics Box modbus PLC controller.\n- Provides a TCP/IP interface to send commands and output keywords using the SDSS-standard formatting.\n\nThe code for jaeger is developed in [GitHub](https://github.com/sdss/jaeger) and can be installed using [sdss_install](https://github.com/sdss/sdss_install) or by running\n\n```console\npip install --upgrade sdss-jaeger\n```\n\nTo check out the development version do\n\n```console\ngit clone https://github.com/sdss/jaeger.git\n```\n\njaeger is developed as an [asyncio](https://docs.python.org/3/library/asyncio.html) library and a certain familiarity with asynchronous programming is required. The actor functionality (TCP/IP connection, command parser, inter-actor communication) is built on top of [CLU](https://github.com/sdss/clu).\n\n## A simple jaeger program\n\n```python\nimport asyncio\nfrom jaeger import FPS, log\n\nasync def main():\n\n    # Set logging level to DEBUG\n    log.set_level(0)\n\n    # Initialise the FPS instance.\n    fps = FPS()\n    await fps.initialise()\n\n    # Print the status of positioner 4\n    print(fps[4].status)\n\n    # Send positioner 4 to alpha=90, beta=45\n    await pos.goto(alpha=90, beta=45)\n\n    # Cleanly finish all pending tasks and exit\n    await fps.shutdown()\n\nasyncio.run(main())\n```\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdss/jaeger',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
