"""
LumenQA - The light-speed automation framework
"""
from setuptools import setup, find_packages

setup(
    name="lumenqa",
    version="0.9.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
)
