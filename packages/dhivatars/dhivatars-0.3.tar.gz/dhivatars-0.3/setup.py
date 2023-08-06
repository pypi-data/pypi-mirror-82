#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='dhivatars',
    version='0.3',
    author="Mohamed Aruham",
    author_email="aruham@baivaru.net",
    description="Generates avatars from dhivehi names or strings",
    long_description=open('README.md').read(),
    packages=find_packages(),
    package_data={'': ['*.otf', 'data/*.otf']},
    include_package_data=True,
    install_requires=['pillow'],
    url='https://github.com/phoenixatom/dhivehi-avatar',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    license="GPLv3",
)