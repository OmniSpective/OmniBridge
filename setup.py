from setuptools import setup
# from importlib import util
from os import path
# import os

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# spec = util.spec_from_file_location(
#     "src.cli.version", os.path.join("src", "cli", "version.py")
# )
# mod = util.module_from_spec(spec)
# spec.loader.exec_module(mod)
# version = mod.version


setup(
    name='OmniBridge',
    license="Apache License 2.0",
    version="0.1.5",
    author='OmniSpective',
    author_email='eliran9692@gmail.com',
    description='Bridging AI models',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tmpOrgName/OmniBridge',
    packages=['src'],
    install_requires=[
        'requests',
        'ruff',
        'argparse'
    ],
)
