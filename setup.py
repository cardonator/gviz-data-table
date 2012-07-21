#!/usr/bin/python
#
# Copyright (C) 2012 Charlie Clark

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
    doc_requires=requires + ['sphinx', 'repoze.sphinx.autointerface']
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
