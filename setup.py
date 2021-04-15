import os
from distutils.core import setup

REQS_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

with open(REQS_FILENAME) as infile:
    INSTALL_REQUIRES = infile.read().splitlines()

setup(
    name="glacier_lengths",
    version="0.0.1",
    description="Tools to measure glacier lengths statistically",
    url="https://github.com/erikmannerfelt/glacier_lengths.git",
    author="Erik Schytt Mannerfelt",
    author_email="mannerfelt@vaw.baug.ethz.ch",
    packages=["glacier_lengths"],
    install_requires=INSTALL_REQUIRES,
    extras_require={"matplotlib": ["matplotlib"]},
)
