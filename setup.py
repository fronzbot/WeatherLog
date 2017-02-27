from setuptools import setup
from WeatherLog import constants

setup(
  name='WeatherLog',
  version=constants.VERSION,
  description='Weather Logging Utility',
  packages=['WeatherLog'],
  author='Kevin Fronczak',
  author_email='kfronczak@gmail.com',
  install_requires=['pyowm'],
  license='MIT')