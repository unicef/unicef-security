#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import codecs
import os
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand

HERE = os.path.abspath(os.path.dirname(__file__))
init = os.path.join(HERE, "src", "unicef_security", "__init__.py")

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_version_re.search(content).group(1)))
    NAME = str(ast.literal_eval(_name_re.search(content).group(1)))


def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(HERE, f), 'r').read()
    return content

setup(
    name=NAME,
    version=VERSION,
    url='https://github.com/unicef/unicef-security',
    author='UNICEF',
    author_email='rapidpro@unicef.org',
    description='',
    long_description=read('README.rst'),
    platforms=['any'],
    license='Apache 2 License',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires = [
        'django',
        'admin-extra-urls',
        'requests',
        'django-countries',
        'django-constance',
        'django-crashlog',
        'social-auth-app-django',
        'django-constance',
        'cryptography',
        'celery'
    ],
    extras_require={
        'test': [
            'vcrpy',
            'mock',
            'factory-boy',
            'pytest',
            'pytest-pythonpath',
            'pytest-cov',
            'pytest-django',
            'pytest-echo',
            'isort',
            'flake8',
        ],
    },
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
