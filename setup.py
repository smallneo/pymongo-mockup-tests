#!/usr/bin/env python

# Copyright 2015 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

mockupdb_link = ('https://github.com/ajdavis/mongo-mockup-db/archive/master.zip'
                 '#egg=mockupdb')

tests_require = ['mockupdb', 'pymongo']
if sys.version_info[:2] == (2, 6):
    tests_require.append('unittest2')

setup(
    name='PyMongo MockupDB tests',
    version='0.1.0',
    description="Test PyMongo with MockupDB.",
    long_description=readme,
    author="A. Jesse Jiryu Davis",
    author_email='jesse@mongodb.com',
    url='https://github.com/ajdavis/pymongo-mockup-tests',
    tests_require=tests_require,
    dependency_links=[mockupdb_link],
    license="Apache License, Version 2.0",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests')
