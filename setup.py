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

"Setup for Theia"

import os
import sys
import setuptools
import numpy as np
from Cython.Build import cythonize

REQUIREMENTS = [
    "qiskit-terra>=0.11",
    "numpy>=1.13",
    "scipy>=1.0",
    "cython >=0.27.1",
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

# Add Cython extensions here
CYTHON_EXTS = ['permute', 'loco']
CYTHON_MODULE = 'theia.cython'
CYTHON_SOURCE_DIR = 'theia/cython'

INCLUDE_DIRS = [np.get_include()]
# Extra link args
LINK_FLAGS = []
# If on Win and not in MSYS2 (i.e. Visual studio compile)
if (sys.platform == 'win32' and os.environ.get('MSYSTEM') is None):
    COMPILER_FLAGS = ['/O2']
# Everything else
else:
    COMPILER_FLAGS = ['-O2', '-funroll-loops', '-std=c++11']
    if sys.platform == 'darwin':
        # These are needed for compiling on OSX 10.14+
        COMPILER_FLAGS.append('-mmacosx-version-min=10.9')
        LINK_FLAGS.append('-mmacosx-version-min=10.9')

EXT_MODULES = []
# Add Cython Extensions
for ext in CYTHON_EXTS:
    mod = setuptools.Extension(CYTHON_MODULE + '.' + ext,
                               sources=[CYTHON_SOURCE_DIR + '/' + ext + '.pyx'],
                               include_dirs=INCLUDE_DIRS,
                               extra_compile_args=COMPILER_FLAGS,
                               extra_link_args=LINK_FLAGS,
                               language='c++')
    EXT_MODULES.append(mod)

setuptools.setup(
    name='theia',
    version=VERSION,
    packages=setuptools.find_namespace_packages(exclude=['test*']),
    cmake_source_dir='.',
    description="Theia - Tools for Qiskit",
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
    ext_modules=cythonize(EXT_MODULES),
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
