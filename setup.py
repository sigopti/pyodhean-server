#!/usr/bin/env python3
"""PyODHeaN solver server

Optimization of District Heating Networks

This package provides the solver server.
"""

from setuptools import setup, find_packages

# Get the long description from the README file
with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyodhean-server",
    version="1.0.0b4",
    description="Optimization of District Heating Networks",
    long_description=long_description,
    url="https://github.com/sigopti/pyodhean-server",
    author="Nobatek/INEF4",
    author_email="jlafrechoux@nobatek.com",
    license="AGPLv3+",
    keywords=[
        "District",
        "Heating",
        "Network",
        "Optimization",
    ],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        (
            "License :: OSI Approved :: "
            "GNU Affero General Public License v3 or later (AGPLv3+)"
        ),
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyodhean>=1.0.0b1",
        "celery[redis]>=4.4.0,<6.0",
        "werkzeug>=1.0.0",
        "flask>=1.1.0",
        "python-dotenv>=0.9.0",
        "flask-smorest>=0.29.0,<0.30",
        "marshmallow>=3.0.0",
        "flask_httpauth>=4.0.0"
    ],
    packages=find_packages(exclude=["tests*"]),
)
