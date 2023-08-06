from setuptools import setup, find_packages

classifiers = [
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Education',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3'
]

setup(
	name='martinsimplecalculator',
	version='0.0.2',
	description='a basic calculator',
	long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	long_description_content_type='text/plain',
	url='',
	author='Martin Husby',
	author_email='martin.husby.dev@gmail.com',
	license='MIT',
	classifiers=classifiers,
	keywords='calculator',
	packages=find_packages(),
	install_requires=['']

)