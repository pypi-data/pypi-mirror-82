#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of addfips.
# http://github.com/fitnr/addfips

# Licensed under the GPL-v3.0 license:
# http://opensource.org/licenses/GPL-3.0
# Copyright (c) 2016, Neil Freeman <contact@fakeisthenewreal.org>

from setuptools import setup

try:
    README = open('README.md').read()
except:
    README = ''

setup(
    name='addfips',
    version='0.3.1',
    description='Add county FIPS to tabular data',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='csv census usa data',
    author='Neil Freeman',
    author_email='contact@fakeisthenewreal.org',
    url='http://github.com/fitnr/addfips',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=['addfips'],
    package_dir={'': 'src'},
    package_data={'addfips': ['data/*.csv']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'addfips=addfips.__main__:main',
        ],
    },
    zip_safe=False,
    test_suite='tests',
    install_requires=[
        "importlib_resources>=2.0.1"
    ],
    python_requires='>=3.6.0',
)
