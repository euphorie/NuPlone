# coding=utf-8
from setuptools import find_packages
from setuptools import setup

import os


version = "2.1.4"

setup(
    name="NuPlone",
    version=version,
    description="A new user interface for Plone",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "changes.rst")).read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="web zope plone theme",
    author="Cornelis Kolbach, Wichert Akkerman and Syslab.com",
    author_email="info@syslab.com",
    url="https://github.com/euphorie/NuPlone",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["plonetheme"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Plone >=5.2",
        "Products.statusmessages",
        "plone.api",
        "plone.app.z3cform",
        "plone.autoform",
        "plone.dexterity",
        "plone.formwidget.namedfile",
        "plone.i18n",
        "plone.supermodel",
        "plone.tiles",
        "plone.z3cform",
        "z3c.form [extra]",
        "zope.i18n",
    ],
    extras_require={
        "tests": [
            "plone.app.robotframework",
            "plone.app.testing",
            "plone.testing",
        ],
    },
)
