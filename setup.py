import os
from distutils.core import setup

REQS_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

with open(REQS_FILENAME) as infile:
    INSTALL_REQUIRES = infile.read().splitlines()

with open("README.md", "r", encoding="utf-8") as infile:
    LONG_DESCRIPTION = infile.read()

GITHUB_URL = "https://github.com/erikmannerfelt/glacier_lengths"

setup(
    name="glacier_lengths",
    version="0.0.2",
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
    install_requires=INSTALL_REQUIRES,
    extras_require={"matplotlib": ["matplotlib"]},
    python_requires=">=3.7",
)
