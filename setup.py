#!/usr/bin/python
#
# Copyright (C) 2012 Charlie Clark

"""Python utility module Google Visualization Python API."""

__author__ = "Charlie Clark"

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

requires = ['setuptools']
if sys.version_info < (2, 7):
    requires.append('ordereddict')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

extra = dict(
    docs=requires + ['sphinx', 'repoze.sphinx.autointerface']
    )

setup(
    name = "gviz_data_table",
    version = "1.0.0",
    description = "Python API for Google Visualization",
    long_description = """
    Date Table maps Python objects to the Google Visualization API
""".strip(),
    author = __author__,
    author_email = 'charlie.clark@clark-consulting.eu',
    license = "BSD",
    url = "https://bitbucket.org/charlie_x/gviz-data-table",
    packages = find_packages(),
    install_requires = requires,
    tests_require = ['coverage', 'pytest', 'pytest-cov'],
    test_suite ='gviz_data_table',
    extras_require = extra,
    cmdclass = {'test': PyTest},
)
