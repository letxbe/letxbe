import os
import re

from setuptools import find_packages, setup

requires = [
    "requests",
    "pydantic",
    "setuptools==63.4.3",  # see https://github.com/python/mypy/issues/13392
]

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
README_PATH = "README.md"


def get_version() -> str:
    init = open(os.path.join(ROOT, "letxbe", "__init__.py")).read()
    versions = VERSION_RE.search(init)
    return versions.group(1) if versions is not None else ""


setup(
    name="letxbe",
    version=get_version(),
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    package_data={
        "letxbe": [
            "py.typed",  # add package stubs https://peps.python.org/pep-0561/#packaging-type-information
        ],
    },
    python_requires=">=3.7",
    author="LetXBe developers",
    author_email="team@letxbe.ai",
    description="Python API to connect and control LXB services",
    long_description=open(README_PATH).read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/onogone/letxbe/",  # TODO to be changed
    license="MIT",
    project_urls={
        "Source": "https://github.com/letxbeai/letxbe",  # TODO to be validated
        "Tracker": "https://github.com/letxbeai/letxbe/issues",  # TODO to be validated
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ],
)
