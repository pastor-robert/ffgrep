from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'grep utility that searches only a subset of files'

setup(
		name ='ffgrep',
		version ='0.1.0',
		author ='Rob Adams',
		author_email ='rob@rob-adams.us',
		url ='https://github.com/pastor-robert/ffgrep',
		description ='grep for source code tree',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='Unlicense',
		packages = find_packages(),
		entry_points = {
			'console_scripts': [
				'ffgrep = ffgrep.ffgrep:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: The Unlicense",
			"Operating System :: OS Independent",
		),
		keywords ='grep python package pastor-robert',
		install_requires = requirements,
		zip_safe = False
)

