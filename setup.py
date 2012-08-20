from setuptools import setup, find_packages
import os

version = '0.4.2'

setup(name='plone.app.referenceablebehavior',
      version=version,
      description="Referenceable dexterity type behavior",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
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
          'plone.behavior',
          'plone.dexterity',
          'plone.directives.form',
          'plone.indexer',
          'plone.uuid',
          'Products.Archetypes',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
