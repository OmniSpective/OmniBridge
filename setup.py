from setuptools import setup
from src.cli.version import version
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='OmniBridge',
    version=version,
    author='OmniSpective',
    author_email='eliran9692@gmail.com',
    description='Bridging AI models',
    long_description=long_description,
    url='https://github.com/tmpOrgName/OmniBridge',
    packages=['src'],
    install_requires=[
        'requests',
        'ruff',
        'argparse'
    ],
)
