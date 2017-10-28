#!/usr/bin/env python
import os

try:
    from setuptools import setup, find_packages
    packages = find_packages(exclude=['tests'])
except ImportError:
    from distutils.core import setup
    packages = ["hse_ruz"]


setup(
    name="hse_ruz",
    packages=packages,
    version="1.1.0",
    description="Python wrapper for HSE RUZ API",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       "README.rst")).read(),
    author="hell03end",
    author_email="hell03end@outlook.com",
    url="https://github.com/hell03end/hse_ruz",
    keywords="HSE RUZ API",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license="MIT License",
    platforms=["All"],
    python_requires=">=3.3"
)
