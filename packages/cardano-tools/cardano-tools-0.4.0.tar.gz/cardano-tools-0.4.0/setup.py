import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cardano-tools",
    version="0.4.0",
    description="Interfaces with the Cardano full-node software.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/viper-staking/cardano-tools",
    author="Viper Staking",
    author_email="viperstakepool@gmail.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["cardano_tools"],
    include_package_data=True,
    install_requires=["fabric", "requests"],
    entry_points={},
)
