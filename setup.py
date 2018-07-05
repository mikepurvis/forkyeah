import sys
from setuptools import find_packages, setup

install_requires = [
    'setuptools',
    'empy',
    'PyYAML',
]

setup(
    name='forkyeah',
    version='0.0.1',
    packages=['forkyeah'],
    install_requires=install_requires,
    author='Mike Purvis',
    author_email='mpurvis@clearpath.ai',
    maintainer='Mike Purvis',
    maintainer_email='mpurvis@clearpath.ai',
    description='forkyeah is a small tool for managing patches on an upstream git repo.',
    license='Apache 2.0',
    test_suite='test',
    entry_points={
        'console_scripts': [
            'forkyeah = forkyeah.cli:main',
        ]
    }
)
