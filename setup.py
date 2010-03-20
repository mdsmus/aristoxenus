from distutils.core import setup

setup(
    name='xenophilus',
    version='0.1.0',
    description='Library for music data',
    author='Pedro Kroger',
    author_email='pedro.kroger@gmail.com',
    url='http://github.com/kroger/xenophilus',
    packages=['xenophilus', 'xenophilus.test'],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
)
