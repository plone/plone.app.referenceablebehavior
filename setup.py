# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import sys


if sys.version_info[0] != 2:
    # Prevent creating or installing a distribution with Python 3.
    raise ValueError("plone.app.referenceablebehavior is based on Archetypes, which is Python 2 only.")

version = '0.7.9'

setup(
    name='plone.app.referenceablebehavior',
    version=version,
    description="Referenceable dexterity type behavior",
    long_description=(open("README.rst").read() + "\n\n" +
                      open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.6',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='dexterity referenceable plone',
    author='Plone Foundation',
    author_email='mailto:dexterity-development@googlegroups.com',
    url='http://plone.org/products/dexterity',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    python_requires='==2.7.*',
    install_requires=[
        'setuptools',
        'plone.app.locales >= 4.3.9',
        'plone.behavior',
        'plone.dexterity >= 1.1',
        'plone.indexer',
        'plone.uuid',
        'Products.Archetypes',
    ],
    extras_require={
      'test': ['Products.CMFPlone',
               'Products.Archetypes',
               'plone.app.testing',
               'plone.app.dexterity'],
    },
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
