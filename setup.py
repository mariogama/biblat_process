#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="biblatprocess",
    version='0.0',
    description="Proceso de archivos en formato ALEPH secuencial a mongoDB",
    author="DGB Sistemas",
    author_email="sistemasintegralesdgb@dgb.unam.mx",
    license="GPL-3.0",
    url="https://github.com/dgb-sistemas/biblat_process",
    packages=find_packages(),
    keywords='biblat process aleph marc mongo',
    maintainer_email='sistemasintegralesdgb@dgb.unam.mx',
    download_url='',
    classifiers=[],
    install_requires=[],
    tests_require=[],
    dependency_links=[],
    test_suite='tests.discover_suite',
    entry_points={
        'console_scripts': [
        'claper_dump=biblat_process.marc_dump:main',
        ],
    },
)
