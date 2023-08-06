import setuptools

with open('README.md', 'r') as fh: long_description = fh.read()

setuptools.setup(
	name='loggaby',
	version='1.0',
	author='TorchedSammy',
	author_email='torchedsammy@gmail.com',
	description='📝 A minimal and simplistic logger with no bloat.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Loggaby/Loggaby-py',
	packages=setuptools.find_packages(),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: System :: Logging'
	]
)