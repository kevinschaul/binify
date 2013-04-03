#!/usr/bin/env python

from setuptools import setup

setup(
    name='binify',
    version='0.1.0',
    author='Kevin Schaul',
    author_email='kevin.schaul@gmail.com',
    url='http://www.kevinschaul.com',
    description='Create a binned shapefile from a point shapefile.',
    long_description='Check out the project on GitHub for the latest information <http://github.com/kevinschaul/binify>',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    packages=[
        'binify',
    ],
    entry_points = {
        'console_scripts': [
            'binify = binify.cli:main',
        ],
    },
)

