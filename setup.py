from setuptools import setup, find_packages

setup(
    name="corp-plus-plus",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "corp=corp.cli.main:main",
        ],
    },
)
