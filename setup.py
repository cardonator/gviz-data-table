#!/usr/bin/python
#
# Copyright (C) 2012 Charlie Clark
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python utility module Google Visualization Python API."""

__author__ = "Charlie Clark"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

requires = []
major, minor = sys.version_info[:2]
if major == 2 and minor < 6:
    requires.append('simplejson')

extra = dict(
    setup_requires=requires + ['setuptools'],
    tests_requires=requires + ['nose', 'coverage'],
    doc_requires=requires + ['sphinx']
    )

setup(
    name="data-table",
    version="0.9.0",
    description="Python API for Google Visualization",
    long_description="""
    Date Table maps Python objects to the Google Visualization API

""".strip(),
    author=__author__,
    license="BSD",
    py_modules=["data_table/data_table"],
    test_suite = 'data_table',
    **extra
)
