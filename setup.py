#!/usr/bin/env python3
# -*- coding: utf-8 -*-

VERSION = '0.0.9'

from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

REQUIREMENTS = ['bs4', 'requests', 'uszipcode']

setup(
	name='findjobs',
	version=VERSION,
	description='Job Search Optimization',
	short_description='Search job boards in seconds for listings matching your criteria.',
	long_description=README,
	long_description_content_type="text/markdown",
	url='https://github.com/colin-gall/findjobs',
	author='Colin Gallagher',
	author_email='colin.gall@outlook.com',
	license='GNU AGPLv3',
	classifiers=[
		"License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
		"Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
	packages=find_packages(),
	include_package_data=True,
	install_requires=REQUIREMENTS,
	python_requires='>=3.6.1',
	keywords='jobs search employment indeed monster'
)
