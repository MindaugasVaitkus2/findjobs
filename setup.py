from setuptools import setup

with open('./docs/version.txt', 'r') as f:
	version = f.read()

with open('./docs/description.txt', 'r') as f:
	description = f.read()

with open('./docs/description.txt', 'r') as f:
	requirements = []
	for line in f:
		requirements.append(line)

setup(
	name='findjobs',
	version=version,
	description=description,
	url='https://github.com/colin-gall/findjobs',
	author='Colin Gallagher',
	author_email='colin.gall@outlook.com',
	license='GNU AGPLv3',
	packages=find_packages(),
	python_requires='>=3.6.1',
	install_requires=requirements,
	keywords='jobs employment indeed monster linkedin'
)
