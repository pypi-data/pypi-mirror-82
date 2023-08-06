#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setup(
    name="scan-to-paperless",
    version="0.12.0",
    description="Tool to scan and process documents to palerless",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python", "Programming Language :: Python :: 3"],
    author="Stéphane Brunner",
    author_email="stephane.brunner@gmail.com",
    url="https://hub.docker.com/r/sbrunner/scan-to-paperless/",
    packages=find_packages(exclude=["tests.*"]),
    install_requires=["argcomplete", "pyyaml", "scikit-image"],
    entry_points={
        "console_scripts": [
            "scan = scan_to_paperless.scan:main",
            "scan-process-status = scan_to_paperless.scan_process_status:main",
        ],
    },
)
