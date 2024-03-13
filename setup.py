from setuptools import find_packages
from setuptools import setup
import os.path as op

__version__ = "0.1"

with open(op.join(op.dirname(__file__), "requirements.txt"), "r") as fp:
    packages = fp.read()

package_list = packages.split("\n")

setup(
    name="metro_app",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=package_list,
)
