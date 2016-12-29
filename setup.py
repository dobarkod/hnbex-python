# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages, Command


class BaseCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class TestCommand(BaseCommand):

    description = "run self-tests"

    def run(self):
        ret = os.system('python tests.py')
        if ret != 0:
            sys.exit(-1)


if sys.version_info.major == 3:
    REQUIRES = ["requests>=2.12.4"]
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ]
else:
    REQUIRES = ["requests>=2.12.4", "mock>=2.0.0"]
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ]

setup(
    name='HNBEX',
    version='0.0.1',
    author='Amalia Souček',
    author_email='amalia.soucek@dobarkod.hr',
    description='A Python package for accessing hnbex.eu service',
    license='MIT',
    url='https://github.com/dobarkod/hnbex-python',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ].extend(classifiers),
    packages=find_packages(),
    install_requires=REQUIRES,
    cmdclass={
        'test': TestCommand,
    }
)