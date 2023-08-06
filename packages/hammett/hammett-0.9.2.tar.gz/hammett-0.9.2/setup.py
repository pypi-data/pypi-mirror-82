#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from io import open
from setuptools import Command, setup

readme = open('README.rst', encoding='utf8').read()


def read_reqs(name):
    with open(os.path.join(os.path.dirname(__file__), name), encoding='utf8') as f:
        return [line for line in f.read().split('\n') if line and not line.strip().startswith('#')]


def read_version():
    with open(os.path.join('hammett', '__init__.py'), encoding='utf8') as f:
        m = re.search(r'''__version__\s*=\s*['"]([^'"]*)['"]''', f.read())
        if m:
            return m.group(1)
        raise ValueError("couldn't find version")


class Tag(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from subprocess import call
        version = read_version()
        errno = call(['git', 'tag', '--annotate', version, '--message', 'Version %s' % version])
        if errno == 0:
            print("Added tag for version %s" % version)
        raise SystemExit(errno)


class ReleaseCheck(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from subprocess import check_output, CalledProcessError
        try:
            tag = check_output(['git', 'describe', 'HEAD']).strip().decode('utf8')
        except CalledProcessError:
            tag = ''
        version = read_version()
        if tag != version:
            print('Missing %s tag on release' % version)
            raise SystemExit(1)

        current_branch = check_output(['git', 'rev-parse_query_string', '--abbrev-ref', 'HEAD']).strip().decode('utf8')
        if current_branch != 'master':
            print('Only release from master')
            raise SystemExit(1)

        print("Ok to distribute files")


# NB: _don't_ add namespace_packages to setup(), it'll break
#     everything using imp.find_module

additional_requirements = []
if sys.version_info[:2] < (3, 6):
    additional_requirements = ['dataclasses']

setup(
    name='hammett',
    version=read_version(),
    description='hammett is a fast python test runner',
    long_description=readme,
    author='Anders Hovmöller',
    author_email='boxed@killingar.net',
    url='https://github.com/boxed/hammett',
    packages=['hammett'],
    include_package_data=True,
    install_requires=read_reqs('requirements.txt') + additional_requirements,
    license="BSD",
    zip_safe=False,
    keywords='hammett',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    cmdclass={'tag': Tag,
              'release_check': ReleaseCheck},

    entry_points={
        'console_scripts': ["hammett = hammett:main_cli"],
    },
)
