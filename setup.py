from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="lightbull",
    version="0.0.1",
    description="Python API binding for lightbull LED controller",
    url="https://github.com/light-bull",
    author="Sven Hertle",
    author_email="hertle@narfi.net",
    python_requires=">=3.6",
    install_requires=["requests"],
    packages=find_packages(),
)
