# -*- coding: utf-8 -*-

from setuptools import setup

import marktask

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="marktask",
    version=marktask.__version__,
    author="David Scheliga",
    author_email="david.scheliga@gmx.de",
    url="https://gitlab.com/david.scheliga/marktask",
    description="Marking files and folder with task states and list them afterwards.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    keywords="mark, file, folder",
    py_modules=["marktask"],
    python_requires='>=3.6',
)
