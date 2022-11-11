import os
import re

from setuptools import find_packages, setup

requires = ["pydantic", "pytest"]

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")


def get_version() -> str:
    init = open(os.path.join(ROOT, "letxbe", "__init__.py")).read()
    versions = VERSION_RE.search(init)
    return versions.group(1) if versions is not None else ""


setup(
    name="letxbe",
    version=get_version(),
    packages=find_packages(),
    package_data={
        "flow": [
            "py.typed",  # add package stubs https://peps.python.org/pep-0561/#packaging-type-information
        ],
    },
    author_email="unfold@onogone.com",
    description="LetXBe SDK",  # Update this description!
    long_description=open("README.md").read(),
    install_requires=requires,
    include_package_data=True,
    url="https://bitbucket.org/onogone/letxbe/",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
