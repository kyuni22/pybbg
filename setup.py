# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='pybbg',
      version='1.0.0',
      description='Bloomberg Open API with pandas',
      url='https://github.com/kyuni22/pybbg',
      author='kyuni22',
      author_email='kyuni22@gmail.com',
      license='MIT',
      packages=['pybbg'],
      requires=['dateutil', 'six'],
      zip_safe=False)