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
    version="2.0.1",
    description="Python wrapper for HSE RUZ API",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       "README.rst")).read(),
    author="Dmitriy Pchelkin | hell03end",
    author_email="hell03end@outlook.com",
    url="https://github.com/hell03end/hse_ruz",
    keywords="HSE RUZ API",
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Environment :: Plugins",
        # "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        # "Intended Audience :: End Users/Desktop",
        # "Intended Audience :: Financial and Insurance Industry",
        # "Intended Audience :: Healthcare Industry",
        # "Intended Audience :: Information Technology",
        # "Intended Audience :: Legal Industry",
        # "Intended Audience :: Manufacturing",
        # "Intended Audience :: Other Audience",
        # "Intended Audience :: Religion",
        # "Intended Audience :: Science/Research",
        # "Intended Audience :: System Administrators",
        # "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    license="MIT License",
    platforms=["All"],
    python_requires=">=3.5"
)
