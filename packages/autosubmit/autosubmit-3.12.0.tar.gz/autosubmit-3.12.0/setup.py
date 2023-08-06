#!/usr/bin/env python

# Copyright 2014 Climate Forecasting Unit, IC3

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

from os import path
from setuptools import setup
from setuptools import find_packages

here = path.abspath(path.dirname(__file__))

# Get the version number from the relevant file
with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='autosubmit',
    license='GNU GPL v3',
    platforms=['GNU/Linux Debian'],
    version=version,
    description='Autosubmit: a versatile tool to manage Weather and Climate Experiments in diverse '
                'Supercomputing Environments',
    author='Daniel Beltran Mora',
    author_email='dbeltran@bsc.es',
    url='http://www.bsc.es/projects/earthscience/autosubmit/',
    download_url='https://earth.bsc.es/wiki/doku.php?id=tools:autosubmit',
    keywords=['climate', 'weather', 'workflow', 'HPC'],
    install_requires=['argparse>=1.2,<2', 'python-dateutil>2', 'pydotplus>=2', 'pyparsing>=2.0.1',
                      'numpy', 'matplotlib', 'paramiko==1.15',
                      'mock>=1.3.0', 'portalocker>=0.5.7', 'networkx', 'bscearth.utils'],
    extras_require={
        'dialog': ["python2-pythondialog>=3.3.0"]
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={'autosubmit': [
        'autosubmit/config/files/autosubmit.conf',
        'autosubmit/config/files/expdef.conf',
        'autosubmit/database/data/autosubmit.sql',
        'README',
        'CHANGELOG',
        'VERSION',
        'LICENSE',
        'docs/autosubmit.pdf'
    ]
    },
    scripts=['bin/autosubmit']
)
