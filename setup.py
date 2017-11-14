"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

import os
from ezored import __version__
from setuptools import Command, find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        html_path = '{0}'.format(os.path.join(os.getcwd(), "htmlcov"))
        errno = call(['py.test', '--cov=ezored', '--cov-report=term-missing', '--cov-report=html:' + html_path])
        # errno = call(['python3', '-m', 'pytest', '--cov=ezored', '--cov-report=term-missing'])
        # errno = call(['pytest', '--cov=ezored', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='ezored',
    version=__version__,
    description='EzoRed cli tool.',
    long_description=long_description,
    url='https://github.com/ezored/ezored',
    author='Paulo Coutinho',
    author_email='paulo@prsolucoes.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['docopt'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'ezored=ezored.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
