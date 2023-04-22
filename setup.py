from setuptools import setup, find_packages
from importlib import util
from os import path
import os

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

spec = util.spec_from_file_location(
    "omnibridge.version", os.path.join("omnibridge", "version.py")
)
mod = util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(mod)  # type: ignore[union-attr]
version = mod.version


setup(
    name='OmniBridge',
    license="Apache License 2.0",
    version=version,
    author='OmniSpective',
    author_email='eliran9692@gmail.com',
    description='Bridging AI models',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/OmniSpective/OmniBridge',
    packages=find_packages(exclude=["cli*", "version*", "main*"]),
    install_requires=[
        'requests',
        'ruff',
        'argparse',
        'huggingface_hub'
    ],
    entry_points={
            "console_scripts": [
                "omnibridge=omnibridge.main:main",
                "obr=omnibridge.main:main",
            ]
        },
)
