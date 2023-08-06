#!/usr/bin/env python3

import channeling as project

from setuptools import setup, find_packages
import os

def here(*path):
    return os.path.join(os.path.dirname(__file__), *path)

def get_file_contents(filename):
    with open(here(filename), 'r', encoding='utf8') as fp:
        return fp.read()

setup(
    name = project.__name__,
    description = project.__doc__.strip(),
    long_description=get_file_contents('README.md'),
    long_description_content_type='text/markdown',
    url = 'https://gitlab.com/nul.one/' + project.__name__,
    download_url = 'https://gitlab.com/nul.one/{1}/-/archive/{0}/{1}-{0}.tar.gz'.format(project.__version__, project.__name__),
    version = project.__version__,
    author = project.__author__,
    author_email = project.__author_email__,
    license = project.__license__,
    packages = [ project.__name__ ],
    entry_points={ 
        'console_scripts': [
            '{0}={0}.__main__:cli'.format(project.__name__),
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: English',
        'Topic :: Communications :: Chat',
        'Topic :: Games/Entertainment',
    ],
    install_requires = [
        'click>=7.1.2',
        'discord.py>=1.4.1',
        'humanize>=3.0.0',
    ],
    python_requires=">=3.6.5",
)

