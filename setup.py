#! /usr/bin/env python3

from pivvy import __VERSION__

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependencies = [x.split("=")[0].strip()
                for x in open("requirements.txt").readlines()]

setup(
    name="pivvy",
    version=".".join(str(x) for x in __VERSION__),
    description="Python framework for painless development of vim plugins",
    long_description=open("README.md").read(),
    url="",
    license="BSD 2-Clause",
    author="Dennis Hedback",
    author_email="d.hedback@gmail.com",
    install_requires=dependencies,
    packages=["pivvy", ],
    scripts=["bin/pivvy-startproject.sh"],
    entry_points={
        "console_scripts": [
            "pivvy=pivvy.cli:main",
        ]
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD 2-Clause',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ),
    include_package_data=True,
)
