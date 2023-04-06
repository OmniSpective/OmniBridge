from setuptools import setup
from src.cli.version import version

setup(
    name='OmniBridge',
    version=version,
    author='OmniSpective',
    author_email='eliran9692@gmail.com',
    description='Bridging AI models',
    url='https://github.com/tmpOrgName/OmniBridge',
    packages=['src'],
    install_requires=[
        'requests',
        'ruff',
        'argparse'
    ],
)
