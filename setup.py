import sys

from setuptools import setup, find_packages
setup(
    name="sast",
    version="0.0.1",
    packages=find_packages(exclude=['tests*']),
    install_requires=['asyncio', 'PyYAML'],
    package_data = {
        'sast': ['*.yaml'],
        'sast.codeql': ['*yaml'],
        'sast.codeql.codeql_v2_13_1' :['*yaml'],
        'sast.codeql.codeql_v2_9_2' :['*yaml'],
    }
)

