from setuptools import setup, find_packages
import os

version = "1.0"

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
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "Plone >=4.0dev",
          "five.grok",
          "zope.tales",
          "zope.app.pagetemplate",
          "plone.tiles",
      ],
      entry_points="""
      """,
      )
