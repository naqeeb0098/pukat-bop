from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bop/__init__.py
from bop import __version__ as version

setup(
	name="bop",
	version=version,
	description="App for the customizations required by Bank of Punjab",
	author="Pukat Digital",
	author_email="mavee.shah@hotmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
