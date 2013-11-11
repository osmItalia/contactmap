#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

required = [
    'requests>=1.2.0',
]

setup(
    name='contactmap',
    version='0.1',
    description='Simple library for contacting OpenStreetMap users',
    author='Cristian Consonni',
    author_email='scrinzi@spaziodati.eu',
    url='https://github.com/CristianCantoro/contactmap',
    packages= ['contactmap'],
    install_requires=required,
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
