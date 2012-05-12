from setuptools import setup, find_packages
import os
import sys

version = '1.0'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective.conference',
      version=version,
      description="A Conference Management System for Plone",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Plone Conference Organisation Tool',
      author='Andreas Mantke',
      author_email='maand@gmx.de',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.dexterity',
          'plone.principalsource',
          'plone.namedfile',
          'plone.formwidget.namedfile',
          'collective.wtf',
      ],
      extras_require={
          'test':  ['plone.app.testing', 'plone.mocktestcase'],
          # Test relations within datagrid fields.  Some of these do
          # not yet have releases with the changes we need.
          'datagrid': [
              'collective.z3cform.datagridfield>0.5',
              'plone.app.referenceablebehavior',
              'plone.formwidget.contenttree>1.0',
              ],
          'plone3': ['collective.autopermission'],
          },
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
