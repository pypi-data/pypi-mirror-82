#!/usr/bin/env python3
# -*- coding: utf8 -*-

from __future__ import print_function

import os
from setuptools import setup
try:
    from codemeta.codemeta import CodeMetaCommand
    cmdclass={
        'codemeta': CodeMetaCommand,
    }
except ImportError:
    cmdclass={}

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname),'r',encoding='utf-8').read()

setup(
    name = "CodeMetaPy",
    version = "0.3.5",
    author = "Maarten van Gompel",
    author_email = "proycon@anaproy.nl",
    description = ("Generate CodeMeta metadata for Python packages"),
    license = "GPL",
    keywords = "software metadata codemeta doap pip pypi distutils admssw",
    url = "https://github.com/proycon/codemeta",
    packages=['codemeta'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    zip_safe=False,
    include_package_data=True,
    package_data = { 'codemeta': ['schema/crosswalk.csv', 'schema/codemeta.jsonld'] },
    install_requires=[ 'nameparser','importlib_metadata'  ],
    entry_points = {    'console_scripts': [ 'codemetapy = codemeta.codemeta:main' ] },
    cmdclass=cmdclass
)
