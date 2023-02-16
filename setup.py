from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in my_apps/__init__.py
from my_apps import __version__ as version

setup(
	name="my_apps",
	version=version,
	description="custom apps",
	author="jake",
	author_email="jake@mail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
