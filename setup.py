# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = __import__('gafutils').__version__

setup(
    name = "gaf-django-utils",
    version = version,
    author = 'Gabriel Fournier',
    author_email = 'gabriel@gaftech.fr',
    url = 'http://github.com/fourga38/gaf-django-utils',
    packages = ['gafutils'],
)
