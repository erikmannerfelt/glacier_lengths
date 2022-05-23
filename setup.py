import os
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as infile:
    LONG_DESCRIPTION = infile.read()

with open("glacier_lengths/__init__.py") as infile:
    for line in infile.read().splitlines():
        if "__version__" not in line:
            continue
        VERSION = line.replace("__version__ = ", "").replace(" ", "").replace("\"", "")
        break

GITHUB_URL = "https://github.com/erikmannerfelt/glacier_lengths"

setup(
    name="glacier_lengths",
    version=VERSION,
    description="Tools to measure glacier lengths statistically",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={
        "Bug Tracker": GITHUB_URL + "/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    author="Erik Schytt Mannerfelt",
    author_email="mannerfelt@vaw.baug.ethz.ch",
    packages=["glacier_lengths"],
    install_requires=["shapely", "numpy"],
    extras_require={"matplotlib": ["matplotlib"]},
    python_requires=">=3.7",
)
