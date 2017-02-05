# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.7.7'

setup(
    name='plone.app.referenceablebehavior',
    version=version,
    description="Referenceable dexterity type behavior",
    long_description=(open("README.rst").read() + "\n\n" +
                      open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.6',
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='dexterity referenceable plone',
    author='Plone Foundation',
    author_email='mailto:dexterity-development@googlegroups.com',
    url='http://plone.org/products/dexterity',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
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
