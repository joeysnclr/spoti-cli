import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="spoti-cli",
    version="1.0.0",
    description="Terminal based Spotify client designed to use Vim keybindings.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/joeysnclr/spoti-cli",
    author="Joseph Sinclair",
    author_email="joey.sinclair02@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["wheel", "beautifulsoup4", "blessed", "Flask", "requests"],
    entry_points={
        "console_scripts": [
            "spoticli=spoticli.__main__:main",
        ]
    },
) 
