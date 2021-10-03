#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by the NSE analysis contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************

from setuptools import setup, find_packages
import miezepy
import pip
import os

try:
    import simpleplot
except:
    pip.main(['install', 'git+git://github.com/AlexanderSchober/simpleplot_qt.git'])

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

for line in lines:
    pip.main(['install', line])

setup(
    name = 'miezepy',
    version = miezepy.__version__,
    license = 'GPL',
    author = 'Dr. Alexander Schober',
    # install_requires = lines,
#    dependency_links =['https://github.com/AlexanderSchober/simpleplot_qt/tarball/master#egg=SimplePlot-0.1'],
    author_email = 'alex.schober@mac.com',
    description = 'Mieze analysis package',
    packages = find_packages(exclude=['doc','test']),
    package_data = {
        'miezepy': ['RELEASE-VERSION'],
        'miezepy.core.process_modules.defaults': ['*.txt'],
        'miezepy.core.instrument_modules.Reseda': ['*.npy']},
    
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
