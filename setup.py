from setuptools import setup

setup(
    name='OmniBridge',
    version='0.1.0',
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
