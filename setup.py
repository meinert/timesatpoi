# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Times at POI',
    version='0.1.0',
    description='Very simple python script that count the number of times you have been at a point and generates a list of when you have been at the point.',
    long_description=readme.md,
    author='Peter Poulsen',
    author_email='ppoulsen@gmail.com',
    url='https://github.com/meinert',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

