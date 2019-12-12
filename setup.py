# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import os
import sys
import inspect
import setuptools

if not hasattr(setuptools,
               'find_namespace_packages') or not inspect.ismethod(
                   setuptools.find_namespace_packages):
    print("Your setuptools version:'{}' does not support PEP 420 "
          "(find_namespace_packages). Upgrade it to version >='40.1.0' and "
          "repeat install.".format(setuptools.__version__))
    sys.exit(1)

REQUIREMENTS = [
    "qiskit-terra>=0.11",
    "numpy>=1.13",
    "scipy>=1.0",
    'matplotlib>=3.0',
    'ipywidgets>=7.3.0',
    "seaborn>=0.9.0",
    "plotly>=4.1",
    "ipyvuetify>=1.1",
    "pyperclip>=1.7"
]

VERSION_PATH = os.path.abspath(
    os.path.join(os.path.join(os.path.dirname(__file__), 'theia', 'VERSION.txt')))
with open(VERSION_PATH, 'r') as fd:
    VERSION = fd.read().rstrip()

setuptools.setup(
    name='theia',
    version=VERSION,
    packages=setuptools.find_namespace_packages(exclude=['test*']),
    cmake_source_dir='.',
    description="Theia - Interactive elements for Qiskit",
    url="",
    author="Theia Development Team",
    author_email="qiskit@us.ibm.com",
    license="Apache 2.0",
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=REQUIREMENTS,
    keywords="qiskit jupyter quantum widgets",
    include_package_data=True,
    zip_safe=False
)
SAVING = """\
==============================================================================
Saving interactive plots as static images requires Orca:

>> conda config --append channels plotly
>> conda install plotly-orca

or see:

https://github.com/plotly/orca
==============================================================================
`"""
print(SAVING)
