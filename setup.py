from setuptools import setup, find_packages

from os import path

localDir = path.abspath(path.dirname(__file__))

setup(
    name = 'action_rules',
    version = '0.1.dev1',
    description = 'A framework for Action Rules in Python',
    url = 'https://github.com/GrantDaly/ActionRules',
    author = 'Grant Daly',
    license = 'MIT',
    packages = find_packages()
    )
