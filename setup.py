from setuptools import setup, find_packages
import os

version = "1.0rc4"

setup(name="NuPlone",
      version=version,
      description="A new user interface for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "changes.rst")).read(),
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
        ],
      keywords="",
      author="Cornelis Kolbach and Wichert Akkerman",
      author_email="",
      url="http://packages.python.org/NuPlone",
      license="GPL",
      packages=find_packages(exclude=["ez_setup"]),
      namespace_packages=["plonetheme"],
      paster_plugins=["Babel"],
      message_extractors = {"plonetheme": [
            ("**.py",    "chameleon_python", None),
            ("**.pt"  ,  "chameleon_xml", None),
            ]},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "Plone >=4.0dev",
          "Zope2 >=2.12.5",
          "cmf.pt",
          "five.pt >= 1.2",
          "five.grok",
          "z3c.pt >=1.1.2",
          "plone.tiles",
          "plone.z3cform",
          "plone.app.z3cform >=0.4.10dev",
          "z3c.form [extra] >=2.3.4dev",
          "plone.i18n",
          "plone.autoform",
          "plone.supermodel",
          "plone.formwidget.namedfile >1.0b4",
          "z3c.appconfig",
          "p01.widget.password",
          "Products.statusmessages",
      ],
      extras_require = {
          "tests": [ "plone.testing",
                     "plone.app.testing",
                   ],
      },
      )
