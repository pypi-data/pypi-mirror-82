#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


def find_version(*segments):
    root = os.path.abspath(os.path.dirname(__file__))
    abspath = os.path.join(root, *segments)
    with open(abspath, "r") as file:
        content = file.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", content, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string!")


setup(
    author="Richard Davis",
    author_email="crashvb@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    description="A utility that can be used to mirror OpenShift releases between docker registries.",
    entry_points="""
        [console_scripts]
        oc-mirror=oc_mirror.scripts.os_mirror:cli
    """,
    extras_require={
        "dev": [
            "black",
            "docker-compose",
            "lovely-pytest-docker",
            "pylint",
            "pyopenssl",
            "pytest",
            "pytest-asyncio",
            "twine",
            "wheel",
        ]
    },
    include_package_data=True,
    install_requires=[
        "aiofiles",
        "docker-registry-client-async>=0.1.6",
        "docker-sign-verify>=1.0.0",
        "click",
        "gnupg",
    ],
    keywords="integrity mirror oc oc-mirror openshift sign signatures verify",
    license="GNU General Public LIcense v3.0",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    name="oc_mirror",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=[
        "docker-compose",
        "lovely-pytest-docker",
        "pyopenssl",
        "pytest",
        "pytest-asyncio",
        "pytest-docker-registry-fixtures",
    ],
    test_suite="tests",
    url="https://pypi.org/project/oc-mirror/",
    version=find_version("oc_mirror", "__init__.py"),
)
