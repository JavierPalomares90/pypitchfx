from setuptools import setup

setup(name='pypitchfx',
      version='1.0',
      description='Tool for parsing mlb gameday data',
      url='http://github.com/JavierPalomares90/pypitchfx',
      author='Javier Palomares',
      author_email='javier.palomares.90@gmail.com',
      license='MIT',
      packages=['pypitchfx'],
      install_requires=[
          'beautifulsoup4',
          'lxml',
	  'sqlalchemy'
      ],
      zip_safe=False)
