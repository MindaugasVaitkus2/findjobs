from setuptools import setup

VERSION = '0.0.8'

REQUIREMENTS = ['bs4', 'requests', 'uszipcode']

setup(
	name='findjobs',
	version=VERSION,
	description='Job Search Optimization',
	long_description='Search job boards in seconds for listings matching your criteria.',
	url='https://github.com/colin-gall/findjobs',
	author='Colin Gallagher',
	author_email='colin.gall@outlook.com',
	license='GNU AGPLv3',
	packages=find_packages(),
	python_requires='>=3.6.1',
	install_requires=REQUIREMENTS,
	keywords='jobs search employment indeed monster')
