"""
Install blueprint.
"""
import os

from setuptools import setup

import blueprint


setup(
    name='blueprint',
    version=blueprint.__version__,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],

    author=blueprint.__author__,
    author_email=blueprint.__email__,
    url=blueprint.__url__,

    license=blueprint.__license__,
    platforms='any',
    description="Render templates using Jinja2.",
    long_description=open(os.path.join('README.md')).read(),

    zip_safe=False,

    install_requires=[
        'jinja2==2.8.0',
        'termcolor==1.1.0',
    ],
    entry_points={
        'console_scripts': [
            'blueprint=blueprint.scripts.blueprint:cmdline'
        ]
    }
)
