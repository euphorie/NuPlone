# coding=utf-8
from setuptools import find_packages
from setuptools import setup

import os


version = '1.6.3'

setup(
    name='NuPlone',
    version=version,
    description='A new user interface for Plone',
    long_description=open('README.rst').read() + '\n' +
    open(os.path.join('docs', 'changes.rst')).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone :: 5.1',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2 :: Only',
    ],
    keywords='',
    author='Cornelis Kolbach and Wichert Akkerman',
    author_email='wichert@wiggy.net',
    url='https://github.com/euphorie/NuPlone',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plonetheme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Plone >=5.1',
        'Zope2 >=2.12.5',
        'five.pt >= 2.2.0',
        'five.grok',
        'plone.api',
        'plone.tiles',
        'plone.z3cform',
        'plone.app.z3cform >=0.4.10dev',
        'z3c.form [extra] >=2.3.4dev',
        'plone.i18n',
        'plone.autoform',
        'plone.supermodel',
        'plone.directives.form',
        'plone.formwidget.namedfile >1.0b4',
        'z3c.appconfig',
        'p01.widget.password',
        'Products.statusmessages',
        'WebHelpers',
        'htmllaundry >=2.0',
        'zope.i18n',
        'plone.api',
        'plone.dexterity',
        'z3c.zrtresource',
    ],
    extras_require={
        'tests': [
            'plone.testing',
            'plone.app.robotframework',
            'plone.app.testing',
        ],
    },
)
